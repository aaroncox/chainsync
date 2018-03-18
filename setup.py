from setuptools import setup, find_packages

setup(name='blocksync',
      version='0.1.2',
      description='Utility to stream and sync blocks into other data sources',
      url='http://github.com/aaroncox/blocksync',
      author='Aaron Cox',
      author_email='aaron@greymass.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'jsonrpcclient',
      ],
      zip_safe=False)
