from setuptools import setup, find_packages

setup(
    name='pyjan26',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Jinja2>=3.1.3',
        'jinja2_markdown>=0.0.3'
    ],
)