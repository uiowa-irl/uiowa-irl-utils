import setuptools

with open("ui-irl-utils/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ui-irl-utils",
    version="0.0.1",
    author="The University of Iowa Internet Research Lab",
    author_email="john-cook@uiowa.edu",
    description="A set of useful utilities",
    long_description_content_type="text/markdown",
    url="https://github.com/uiowa-irl/uiowa-irl-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]

)