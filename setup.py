import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="irlutils",
    version="0.0.7",
    author="The University of Iowa Internet Research Lab",
    author_email="john-cook@uiowa.edu",
    description="IRL Utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/uiowa-irl/uiowa-irl-utils.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]

)
