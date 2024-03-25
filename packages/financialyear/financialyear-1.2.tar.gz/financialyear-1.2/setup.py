from setuptools import setup, find_packages

# with open("README.md", 'r') as f:
#     description = f.read()

setup(
    name='financialyear',
    version='1.02',
    packages=find_packages(),
    install_requires=[],
    description='It Calculate financial year related dates',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/piidus/FinancialYear',
    author='Sudiip',
    author_email='sudiipkumarbasu@gmail.com',
    keywords=['financial year', 'fin year'],
    entry_point={'comsole_scripts': ['financialyear = src:main:main']}
)
