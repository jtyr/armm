#!/usr/bin/env python

from distutils.core import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='armm',
    version='1.0',
    description='Android Repo Manifest Management tool',
    author='Jiri Tyr',
    author_email='jiri.tyr@gmail.com',
    url='http://github.com/jtyr/armm',
    license='MIT',
    keywords='android repo manifest',
    platforms=['any'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Text Processing :: Markup :: XML'
    ],
    long_description=long_description,
    packages=['armm'],
    package_dir={'armm': 'src/armm'},
    scripts=['scripts/armm'],
    install_requires=['docopt', 'json', 'lxml', 'yaml'],
    data_files=[
        ('share/doc/armm', ['LICENSE', 'README.md'])
    ]
)
