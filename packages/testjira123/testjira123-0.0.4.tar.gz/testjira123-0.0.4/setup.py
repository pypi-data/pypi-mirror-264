import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="testjira123",
    version="0.0.4",
    author="Alexandre Blanchet",
    author_email="alexandreblanchet@upidev.fr",
    description=(
        "One command once. BashMemo memorises commands for you."
        "Access it from anywhere logging with your github account"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blancheta/bashmemo",
    project_urls={
        "Bug Tracker": "https://github.com/blancheta/bashmemo/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests", "rich==12.5.1"],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "bmm = main:run",
        ]
    }
)
