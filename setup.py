from setuptools import setup

VERSION = '0.1.0'
REPO = 'https://github.com/bitlang/flexicon'

setup(
    name='flexicon',
    packages=['flexicon'],
    version=VERSION,
    description='A lightweight regex-based lexing framework',
    author='Josh Junon',
    author_email='josh@junon.me',
    url=REPO,
    download_url='{}/archive/{}.tar.gz'.format(REPO, VERSION),
    keywords=['lexer', 'lexing', 'tokenizer', 'regex', 'parsing', 'ast'],
    classifiers=[],
    install_requires=['regex']
)
