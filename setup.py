#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name='pygments_portugol',
    version='0.2.0',
    description='Pygments lexer for Portugol Studio.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='pygments portugol studio lexer',
    license='GPLv3',

    author='Heliton Martins Reis Filho',
    author_email='helitonmrf@gmail.com',

    url='https://github.com/hellmrf/pygments-portugol',

    packages=find_packages(),
    install_requires=['pygments >= 2.0'],

    entry_points='''[pygments.lexers]
                    portugolstudio=pygments_portugol:PortugolStudioLexer''',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: Portuguese (Brazilian)',
    ],
)
