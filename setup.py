from setuptools import setup, find_packages

setup(
    name='pyjan26',
    version='0.11',
    python_requires='>=3.6',
    setup_requires=['setuptools>=38.6.0', 'wheel'],
    packages=find_packages(),
    package_data={'pyjan26': ['project_structure/_content/*.md', 'project_structure/_templates/*.html']},
    install_requires=[
        'Jinja2>=3.1.3',
        'jinja2_markdown>=0.0.3',
        'python-frontmatter==1.1.0'
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
