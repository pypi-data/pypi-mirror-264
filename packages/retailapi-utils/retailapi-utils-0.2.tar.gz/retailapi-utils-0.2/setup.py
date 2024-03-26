from setuptools import setup, find_packages

setup(
    name='retailapi-utils',
    version='0.2',
    packages=find_packages(),
    description='RetailCRM API utility library',
    author='Ilya Charauko',
    author_email='ilyacharauko@gmail.com',
    url='https://github.com/MirrSs/retailcrm-api-utils',
    install_requires=[
        'httpx'
    ]
)