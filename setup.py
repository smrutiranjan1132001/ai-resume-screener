# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-resume-screener",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit",
        "openai",
        "PyMuPDF",
        "sqlite-utils",
        "python-dotenv",
        "together"
    ],
    author="Smruti Ranjan Bhuyan",
    author_email="smruti1132001@email.com",
    description="AI-powered resume screening tool using LLMs and Streamlit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smrutiranjan1132001/ai-resume-screener",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)
