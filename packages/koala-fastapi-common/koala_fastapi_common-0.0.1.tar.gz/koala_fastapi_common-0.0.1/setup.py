from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r" , encoding="utf-8") as f:
    long_description = f.read()
    setup(
        name='koala_fastapi_common',
        version='0.0.1',
        description="A package for koala's project",
        long_description=long_description,
        author='phailin',
        author_email='phailin791@hotmail.com',
        url='https://github.com/phailin/koala_fastapi_common',
        install_requires=[
            "mysql-connector-python",
            "SQLAlchemy",
            "python-jose",
            "pydantic",
            "pydantic_core",
            "loguru",
            "bcrypt",
        ],
        license='MIT',
        packages=find_packages(),
        platforms=["all"],
        classifiers=[
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Natural Language :: Chinese (Simplified)',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Topic :: Software Development :: Libraries'
        ],
    )