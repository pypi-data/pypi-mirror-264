# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name='all_tools_on_blockchain',
    version='0.0.1',
    author='th35tr0n9',
    author_email='shawn@hxzy.me',
    url='https://shawnxu.me',
    description=u'All-in-one toolset for blockchain.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=['all_tools_on_blockchain'],
    install_requires=[
        'requests',
        'prettytable',
        'web3>=6.0.0'
    ],
    entry_points={
        'console_scripts': [
            'read=all_tools_on_blockchain:read_contract'
        ]
    }
)