import sys
from setuptools import setup, find_packages

# Numpy is not available under python2.4 or 3.0 to 3.1
# Install the package 'daruma-py2compt' for python2 from python2.4 to 2.7

python_version = sys.version_info
if python_version < (2, 4):
    raise ValueError("This package does not support Python versions less than 2.4 or between 3.0 and 3.1.")

elif python_version < (3, 0):
        setup(
        name='daruma-py2compt',
        version='0.0.1',
        packages=['daruma_py2compt'],
        entry_points={
            'console_scripts': [
                'daruma=daruma_py2compt.daruma_module:main',
            ],
        },
        install_requires=[
            'numpy<=1.16.6', 
        ],
        include_package_data=True,
        package_data={'daruma-py2compt': ['daruma_py2compt/data/AAindex553-Normal-X0.feature','daruma_py2compt/data/CV5.weight']},
    )

elif python_version < (3, 1):
    raise ValueError("This package does not support Python versions less than 2.4 or between 3.0 and 3.1.")

elif python_version >= (3, 1):
    setup(
        name='daruma',
        version='0.0.2',
        packages=['daruma'],
        entry_points={
            'console_scripts': [
                'daruma=daruma.daruma_module:main',
            ],
        },
        install_requires=[
            'numpy',
        ],
        include_package_data=True,
        package_data={'daruma': ['daruma/data/AAindex553-Normal-X0.feature','daruma/data/CV5.weight']},
    )

