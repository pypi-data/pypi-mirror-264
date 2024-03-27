from setuptools import setup, find_packages

setup(
    name='froster_publish_pypi',
    version='0.3.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'froster_publish_pypi = froster_publish_pypi:hello'
        ]
    }
)