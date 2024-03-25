#!/usr/bin/env python
"""The setup script."""

from setuptools import setup, find_packages
import prebuild.secret_code as secret_code


# readme = Path("README.en.md").read_text("utf8")


requirements = ["nicegui>=1.4.0"]

test_requirements = []

setup(
    author="carson_jia",
    author_email="568166495@qq.com",
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
    ],
    description="...",
    entry_points={},
    install_requires=requirements,
    license="MIT license",
    # long_description=readme,
    long_description_content_type="text/markdown",
    keywords=[],
    name="secret_code",
    packages=find_packages(where="./prebuild"),
    package_dir={"secret_code": "./prebuild/secret_code"},
    package_data={"": ["*.pyd", "*.pem"], "ui": ["*.*"]},
    # include_package_data=True,
    # data_files=[("ui", ["ui/c01.txt"])],
    test_suite="__tests",
    tests_require=test_requirements,
    url="",
    version=secret_code.__version__,
    zip_safe=False,
)
