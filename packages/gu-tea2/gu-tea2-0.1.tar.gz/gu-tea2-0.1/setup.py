from setuptools import setup

setup(
    author='CryptoGu',
    author_email='kriptoairdrop9@gmail.com',
     name='gu-tea2',
    version='0.1',
    description='Project 2 with no external dependencies.',
    url='https://github.com/CryptoGu1/gu-tea2.git',
    project_urls={
        'Homepage': 'https://github.com/CryptoGu1/gu-tea2.git',
        'Source': 'https://github.com/CryptoGu1/gu-tea2.git',
        },
    py_modules=['hello_world_api1'],
     install_requires=[
        'requests>=2.20.0',
        'Gu-tea'
    ]
)