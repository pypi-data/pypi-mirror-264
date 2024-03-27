#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name="wtu-mlflow",
    version="0.0.1",
    author="hbjs",
    author_email="hbjs97@naver.com",
    description="W-Train Utils for MLflow",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
    packages=find_packages(exclude=("tests", "tests.*")),
    install_requires=[
        "mlflow>=2.2.1,<3.0",
        "numpy>=1.22.0",
        "boto3>=1.34.0",
        "numpy",
        "pika",
        "onnx",
        "onnxruntime",
    ],
)
