#!/usr/bin/env python3
"""
Setup script for SCORM-Maker.
"""

from setuptools import setup, find_packages
import os

# Get the long description from the README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get the version from scorm_maker/__init__.py
with open(os.path.join(os.path.dirname(__file__), 'scorm_maker', '__init__.py'), encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip("'").strip('"')
            break
    else:
        version = '0.1.0'

setup(
    name='scorm-maker',
    version=version,
    description='Automated SCORM Package Generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='SCORM-Maker Team',
    author_email='info@example.com',
    url='https://github.com/example/scorm-maker',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'scorm_maker': ['templates/*'],
    },
    entry_points={
        'console_scripts': [
            'scorm-maker=scorm_maker.cli:main',
        ],
    },
    install_requires=[
        'PyYAML>=6.0',
        'Jinja2>=3.1.2',
        'Pillow>=9.0.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Education',
    ],
    python_requires='>=3.8',
)
