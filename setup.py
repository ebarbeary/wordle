from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='wordle-ebarbeary',
    version="0.0.1",
    author="Elliot Barbeary",
    author_email="e.barbeary@outlook.com",
    description="A suite of tools to build, test and run algorithms that solve the popular web-game 'Wordle'",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ebarbeary/wordle",
    project_urls={
        "Bug Tracker": "https://github.com/ebarbeary/wordle/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3"
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        "Operating System :: OS Independent"
        "Development Status :: 2 - Pre-Alpha"
        "Natural Language :: English"
    ],
    package_dir={"": "wordle"},
    packages=find_packages(where="wordle"),
    include_package_data=True,
    python_requires=">=3.6"
    )