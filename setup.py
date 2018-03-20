from setuptools import setup, find_packages

setup(
    name='chainsync',
    version='0.1.6',
    description='Utility to stream and sync blocks into other data sources',
    url='http://github.com/aaroncox/chainsync',
    author='Aaron Cox',
    author_email='aaron@greymass.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['jsonrpcclient', 'requests'],
    zip_safe=False
)
