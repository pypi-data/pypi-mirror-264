from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="pseudoservice",
    version="0.1.0",
    author="Manbehindthemadness",
    author_email="manbehindthemadness@gmail.com",
    description="A simple threaded task launcher that emulates unix service-unit style behavior",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manbehindthemadness/pseudoservice",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
)
