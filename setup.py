#!/usr/bin/env python3
"""
Setup script for Colab Bridge - Universal Google Colab Integration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="colab-bridge",
    version="1.0.0",
    author="sundeepg98",
    author_email="sundeepg8@gmail.com",
    description="Universal Google Colab integration for any IDE or coding tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sundeepg98/colab-bridge",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "google-auth>=2.0.0",
        "google-auth-oauthlib>=1.0.0",
        "google-auth-httplib2>=0.1.0",
        "google-api-python-client>=2.0.0",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.910",
        ],
    },
    entry_points={
        "console_scripts": [
            "colab-bridge=colab_integration.cli:main",
            "colab-execute=colab_integration.cli:execute_command",
            "colab-setup=colab_integration.cli:setup_command",
        ],
    },
    keywords="google colab integration ide extension python",
    project_urls={
        "Bug Reports": "https://github.com/sundeepg98/colab-bridge/issues",
        "Source": "https://github.com/sundeepg98/colab-bridge",
        "Documentation": "https://github.com/sundeepg98/colab-bridge#readme",
    },
)