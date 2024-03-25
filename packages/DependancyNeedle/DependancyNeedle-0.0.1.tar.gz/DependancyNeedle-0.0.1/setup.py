from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Dependancy Injection Container'
LONG_DESCRIPTION = ('Dependancy injection container used to'
                    ' register and build dependancies.')

setup(
    name="DependancyNeedle",
    version=VERSION,
    author="Abdelrahman Torky",
    author_email="24torky@email.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=['python', 'Dependancy Injection',
              'Dependancy Injection Container',
              'Inversion of Control', 'Clean Architecture'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
    ]
)
