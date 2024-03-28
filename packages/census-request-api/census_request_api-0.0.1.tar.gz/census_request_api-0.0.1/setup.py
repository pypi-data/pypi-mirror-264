from setuptools import setup, find_packages

setup(
    name='census_request_api',
    version='0.0.1',
    author="lennon0926",
    author_email="<onnelle.lugo@upr.edu>",
    packages=find_packages(),
    install_requires=[
        'requests', 
        'pandas'
        ],
)