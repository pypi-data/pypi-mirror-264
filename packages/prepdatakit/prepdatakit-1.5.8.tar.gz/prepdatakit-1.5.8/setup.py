from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIREMENTS = [i.strip() for i in open("./requirements.txt").readlines()]



setup(
    name="prepdatakit",
    version="1.5.8",
    
    author="Abdulaziz Mofid",
    author_email="abdulaziz.mofid@gmail.com",
    description="A comprehensive toolkit for preprocessing datasets, including data reading, data summary generation, handling missing values, and categorical data encoding.",
    long_description=long_description,  # Assigning the long description
    long_description_content_type="text/markdown",  # Indicating markdown format
    packages=["prepdatakit"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=REQUIREMENTS,
)
