import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="corgibrowser",
    version="0.0.1",
    author="Jose Enriquez",
    author_email="joseaenriqueza@hotmail.com",
    description="Corgi Browser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/j-enriquez/corgibrowser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)