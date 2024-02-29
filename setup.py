from setuptools import setup, find_packages

setup(
    name='pyjan26',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'Jinja2>=3.1.3',
        'jinja2_markdown>=0.0.3'
    ],
    author='Josnin',
    license='MIT',
    description='PyJan26 is a static site generator written in Python. It allows you to generate static websites from templates and content files, with support for pagination, custom pages, custom filters, and custom collections.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    project_urls={
        'Source': 'https://github.com/josnin/pyjan26',
    }
)
