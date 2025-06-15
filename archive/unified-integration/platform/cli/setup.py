#!/usr/bin/env python3
"""
Setup script for Sora CLI
"""

from setuptools import setup, find_packages

setup(
    name='ai-platform-cli',
    version='1.0.0',
    description='AI Platform CLI - Maintenance tool for Generic AI Simulator Platform',
    author='AI Platform Team',
    python_requires='>=3.8',
    install_requires=[
        'click>=8.0',
        'rich>=13.0',
        'aiohttp>=3.8',
        'asyncio',
        'python-dateutil',
    ],
    entry_points={
        'console_scripts': [
            'aiplatform=platform_cli:cli',
            'aip=platform_cli:cli',  # Short alias
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)