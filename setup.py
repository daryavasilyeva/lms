#!/usr/bin/env python3

"""Setup script."""

from setuptools import setup

setup(
    name="lms",
    version="0.0.0",
    author="Darya Vasilyeva",
    author_email="darya.vasilyeva@phystech.edu",
    url="https://github.com/daryavasilyeva/lms",
    license="MIT",
    packages=[
        "app",
    ],
    install_requires=[
      "flask",
      "flask_login",
      "flask-sqlalchemy",
      "flask-migrate",
      "flask_wtf",
      "python_dotenv"
    ],
    setup_requires=[
        "pytest-runner",
        "pytest-pylint",
        "pytest-pycodestyle",
        "pytest-pep257",
        "pytest-cov",
    ],
    tests_require=[
        "pytest",
        "pylint",
        "pycodestyle",
        "pep257",
        "tests",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ]
)
