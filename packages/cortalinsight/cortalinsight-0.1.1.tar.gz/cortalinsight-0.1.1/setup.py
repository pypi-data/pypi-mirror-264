from setuptools import setup, find_packages

# Read the contents of your requirements file
def read_requirements():
    with open('requirements.txt') as req:
        return req.read().splitlines()

# Read the contents of your README file
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# Import the version from your package
from cortalinsight.cli import __version__

setup(
    name='cortalinsight',
    version=__version__,
    packages=find_packages(),
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'cortalinsight=cortalinsight.cli:main',
        ],
    },
    
    # Metadata
    author='Preetham',
    author_email='developer@cortalinsight.com',
    description='A command line tool to interact with Cortal Insight API',
    keywords='cortal insight cli api',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Assuming your README.md is in Markdown format
    url='http://cortalinsight.com',  
    project_urls={
        'Source Code': 'https://github.com/cortal-insight/cortal-insight-python-client',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
