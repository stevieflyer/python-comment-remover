from setuptools import setup, find_packages


def read_requirements():
    with open("requirements.txt", "r") as f:
        requirements = f.readlines()
    return [
        req.strip() for req in requirements if req.strip() and not req.startswith("#")
    ]


setup(
    name="chinese-comment-remover",
    version="0.0.0.1",
    packages=find_packages(exclude=["test", "test.*"]),
    include_package_data=True,
    install_requires=read_requirements(),
    author="steveflyer",
    author_email="steveflyer7@gmail.com",
    description="A tool to remove comments [with Chinese] characters from Python files.",
    long_description=open("./README.md").read(),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "remove-comment=scripts.remove_comment:main",
        ],
    },
)

# To build:
# python setup.py sdist bdist_wheel
# To upload to pypi:
# twine upload dist/*
