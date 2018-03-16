from setuptools import setup, find_packages

setup(name='blocksync',
      version='0.1.0',
      description='Utility to stream and sync blocks into other data sources',
      url='http://github.com/aaroncox/blocksync',
      author='Aaron Cox',
      author_email='aaron@greymass.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False)
