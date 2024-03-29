from setuptools import setup, find_packages

REQUIREMENTS = [i.strip() for i in open("./requirements.txt").readlines()]

setup(
    name="prepdatakit",
    version="1.5.6",
    
    author="Abdulaziz Mofid",
    author_email="abdulaziz.mofid@gmail.com",
    description="A comprehensive toolkit for preprocessing datasets, including data reading, data summary generation, handling missing values, and categorical data encoding.",
    packages=["prepdatakit"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=REQUIREMENTS,
)
