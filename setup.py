# vim: set et ts=4 sw=4 sts=4 ai:

from distutils.core import setup

from dispass import __version__

long_desc = '''
DisPass is a cross-platform password generator you can use to create 
unique passwords for logging in to websites, servers
or any other kind of thing that requires login.

It doesn't keep your passwords in a database but rather lets you generate
a unique password formed from a label, an optional salt and a master password.
'''

setup(
    name='DisPass',
    version=__version__,
    description='Generate and disperse/dispell passwords',
    author='Benjamin Althues',
    author_email='benjamin@babab.nl',
    url='http://babab.nl/projects/dispass/',
    download_url='http://bitbucket.org/babab/dispass',
    packages=['dispass'],
    license='ISC',
    long_description=long_desc,
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: Dutch',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications',
        'Topic :: Internet',
        'Topic :: Office/Business',
        'Topic :: Security :: Cryptography',
        'Topic :: Utilities',
    ],
    scripts=['scripts/dispass', 'scripts/gdispass'],
    )
