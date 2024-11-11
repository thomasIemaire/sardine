from setuptools import setup, find_packages

setup(
    name="Sardine",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "numpy",
        "PyMuPDF",
    ],
    author="Lemaire Thomas",
    author_email="thomas.lmre14@gmail.com",
    description="A library for processing PDF images and extracting boxes.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/thomasIemaire/sardine",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)