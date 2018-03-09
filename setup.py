from setuptools import setup

setup(name='blocksync',
      version='0.1.0',
      description='Utility to stream and sync blocks into other data sources',
      url='http://github.com/aaroncox/blocksync',
      author='Aaron Cox',
      author_email='aaron@greymass.com',
      license='MIT',
      packages=['blocksync', 'adapters'],
      zip_safe=False)
