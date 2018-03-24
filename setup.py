from setuptools import setup, find_packages

TEST_REQUIRED = [
    'pep8',
    'pytest',
    'pytest-pylint',
    'pytest-xdist',
    'pytest-runner',
    'pytest-pep8',
    'pytest-cov',
    'yapf',
    'autopep8'
]

extras = {
    'test': TEST_REQUIRED,
}

setup(
    name='chainsync',
    version='0.3.2',
    description='Utility to stream and sync blocks into other data sources',
    url='http://github.com/aaroncox/chainsync',
    author='Aaron Cox',
    author_email='aaron@greymass.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['jsonrpcclient', 'requests'],
    setup_requires=['pytest-runner'],
    tests_require=TEST_REQUIRED,
    extras_require=extras,
    zip_safe=False
)
