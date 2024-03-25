from setuptools import find_packages, setup

with open("README.md") as readme:
        description = readme.read()

setup(
    name='simple_sarif',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        'jsonschema>=4.21.1',
    ],
    python_requires='>=3.8',
    description="A library for creating and managing SARIF files.",
    license='Apache License 2.0',
    long_description=description,
    long_description_content_type="text/markdown",
    #url='https://github.com/scribe-security/simple-sarif',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
