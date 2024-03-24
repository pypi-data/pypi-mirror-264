from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="build-settings",
    version="0.1.6",
    author="Manbehindthemadness",
    author_email="manbehindthemadness@gmail.com",
    description="An extension of configparser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manbehindthemadness/build-settings",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "psutil",
    ],
    extras_require={
        "testing": ["unittest-mock"],
    },
)
