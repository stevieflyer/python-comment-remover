import os
import sys
import pathlib
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from chinese_comment_remover.remove import (
    remove_comment_for_dir,
    remove_comment_for_file,
)


def get_parser():
    parser = argparse.ArgumentParser(
        description="Remove comments for Python files or Python Projects."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The path of the input file or directory.",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="If specified, remove comments for all the Python files in the directory recursively.",
    )
    parser.add_argument(
        "-c",
        "--chinese-only",
        action="store_true",
        help="If specified, only remove the comment containing Chinese characters.",
    )
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    path = pathlib.Path(args.path)
    recursive = args.recursive
    chinese_only = args.chinese_only
    warn_prompt = " in CHINESE" if chinese_only else " in ALL language"

    if not path.exists():
        raise FileNotFoundError(f"Path: {path} does not exist.")
    if recursive:
        if path.is_file():
            raise ValueError("Please specify a directory for -r.")
        user_reponse = input(
            f"Are you sure to remove comments{warn_prompt} for all the Python files in the directory: {path}? (y/n)"
        )
        if user_reponse.lower() == "y":
            remove_comment_for_dir(path, chinese_only=chinese_only)
        else:
            print("Operation cancelled.")
    else:
        if path.is_dir():
            raise ValueError("Please specify -r for directory.")
        user_reponse = input(
            f"Are you sure to remove comments{warn_prompt} for the Python file: {path}? (y/n)"
        )
        if user_reponse.lower() == "y":
            remove_comment_for_file(path, chinese_only=chinese_only)
        else:
            print("Operation cancelled.")


# Example Usage:
# python remove_comment.py -r /path/to/project
# python remove_comment.py /path/to/file.py
if __name__ == "__main__":
    main()
