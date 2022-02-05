import os
import re
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def read(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    if sys.version < "3":
        return open(path).read()
    return open(path, encoding="utf-8").read()


README = read("README.rst")
CHANGES = read("CHANGES.rst")


version = ""

with open("src/page_components/__init__.py") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("Cannot find version information")


setup(
    name="django-page-components",
    packages=find_packages("src"),
    package_dir={"": "src"},
    version=version,
    author="Andrey Fedoseev",
    author_email="andrey.fedoseev@gmail.com",
    url="https://github.com/andreyfedoseev/django-page-components",
    description="Mini-framework for creating re-usable UI components for Django",
    long_description="\n\n".join([README, CHANGES]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords=[
        "django",
    ],
    python_requires=">=3.6",
    install_requires=[
        "Django>=2.0",
        "django-asset-definitions>=1.0.0",
    ],
    tests_require=[
        "pytest",
    ],
    cmdclass={"test": PyTest},
)
