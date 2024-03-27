# setup.py

from setuptools import setup, find_packages

setup(
    name='pvp-backend-api',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        pvp-api=pvp_api:cli
    ''',
    author='Sachin Raghav',
    author_email='sraghav872@gmail.com',
    description='A Python package to generate a PVP API template',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/pvp-api-package',
)
