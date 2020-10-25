"""
# django-rest-durin

Per API client token authentication Module for django rest framework.

## Docs & Example Usage: https://github.com/eshaan7/django-rest-durin
"""
from setuptools import find_packages, setup

# Get the long description from the relevant file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

GITHUB_URL = "https://github.com/eshaan7/django-rest-durin"

setup(
    name="django-rest-durin",
    url=GITHUB_URL,
    version="0.1.0",
    license="MIT",
    description="""
    Per API client token authentication Module for django rest framework.
    """,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Eshaan Bansal",
    author_email="eshaan7bansal@gmail.com",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 5 - Production/Stable",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Session",
        "Environment :: Web Environment",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="django rest authentication login token client auth",
    packages=find_packages(exclude=[".github", "docs", "tests", "example_project"]),
    install_requires=["django>=2.2", "djangorestframework>=3.7.0", "humanize"],
    project_urls={
        "Documentation": "https://django-rest-durin.readthedocs.io/",
        "Funding": "https://www.paypal.me/eshaanbansal",
        "Source": GITHUB_URL,
        "Tracker": "{}/issues".format(GITHUB_URL),
    },
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        "dev": ["black==20.8b1", "flake8", "django-nose", "django-memoize", "isort"],
        "test": ["black==20.8b1", "flake8", "django-nose", "django-memoize", "isort"],
    },
)
