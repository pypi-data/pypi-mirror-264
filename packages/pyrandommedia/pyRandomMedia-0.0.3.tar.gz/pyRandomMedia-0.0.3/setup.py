import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "pyRandomMedia",
    version = "0.0.3",
    author = "Stan, Nicholas, Benson, Sangely",
    description = "A package used to generate random media for website testing. This includes songs, movies, news and Tv shows.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/software-students-spring2024/3-python-package-exercise-team-kiwi",
    project_urls = {
        "Github Repo": "https://github.com/software-students-spring2024/3-python-package-exercise-team-kiwi",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    install_requires=[
        "feedparser",
        "pandas"
    ],
    python_requires = ">=3.6"
)