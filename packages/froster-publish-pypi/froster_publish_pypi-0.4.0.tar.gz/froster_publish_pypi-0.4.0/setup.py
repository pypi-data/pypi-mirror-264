from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='froster_publish_pypi',
    version='0.4.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'froster_publish_pypi = froster_publish_pypi:hello'
        ]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)
