import os
import re
import token
import pathlib
import tokenize
import subprocess
from typing import Optional


chinese_char_pattern = re.compile(r"[\u4e00-\u9fff]+")


def remove_comment_for_file(
    src_fp: pathlib.Path,
    chinese_only: Optional[bool] = False,
) -> str:
    """Remove the comment from a single file.

    Args:
        src_fp (pathlib.Path): The path of the input file.
        chinese_only (Optional[bool], optional): If True, only remove the comment containing Chinese characters. Defaults to False.

    Returns:
        (str) The file content after removing the comment.
    """
    src_fp = pathlib.Path(src_fp)
    if not src_fp.exists() or src_fp.is_dir() or src_fp.suffix != ".py":
        raise FileNotFoundError(
            f"Source file path: {src_fp} does not exist or is a directory. Please specify a valid source file path."
        )

    output_content = ""
    with open(src_fp, "r") as src:
        prev_toktype = token.INDENT
        last_lineno = -1
        last_col = 0

        tokgen = tokenize.generate_tokens(src.readline)
        for toktype, ttext, (slineno, scol), (elineno, ecol), ltext in tokgen:
            if slineno > last_lineno:
                last_col = 0
            if scol > last_col:
                output_content += " " * (scol - last_col)
            if toktype == token.STRING and prev_toktype == token.INDENT:
                if chinese_only and not chinese_char_pattern.search(ttext):
                    output_content += ttext
            elif toktype == tokenize.COMMENT:
                if chinese_only and not chinese_char_pattern.search(ttext):
                    output_content += ttext
            else:
                output_content += ttext
            prev_toktype = toktype
            last_col = ecol
            last_lineno = elineno

    with open(src_fp, "w") as src:
        src.write(output_content)
    subprocess.run(["black", src_fp])

    return output_content


def remove_comment_for_dir(
    src_dir: pathlib.Path,
    chinese_only: Optional[bool] = False,
) -> None:
    """Remove the comment from all the Python files in a directory.

    Args:
        src_dir (pathlib.Path): The path of the input directory.
        chinese_only (Optional[bool], optional): If True, only remove the comment containing Chinese characters. Defaults to False.
    """
    src_dir = pathlib.Path(src_dir)
    if not src_dir.exists() or not src_dir.is_dir():
        raise FileNotFoundError(
            f"Source directory path: {src_dir} does not exist or is not a directory. Please specify a valid source directory path."
        )

    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py"):
                src_fp = pathlib.Path(root) / file
                remove_comment_for_file(src_fp, chinese_only=chinese_only)
        for dir in dirs:
            remove_comment_for_dir(pathlib.Path(root) / dir, chinese_only=chinese_only)


__all__ = [
    "remove_comment_for_dir",
    "remove_comment_for_file",
]
