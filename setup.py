# vim: set et ts=4 sw=4 sts=4 ai:

from distutils.core import setup
import dispass.dispass

long_desc = '''DisPass is a password manager for GNU/Linux, \*BSD, MacOS X and
Windows. It can be used as any traditional password manager, but has one key
difference. DisPass does not store your passwords anywhere, so you can never
lose them.

It creates strong and unique passphrases formed from a master password and a
label (and some optional parameters), helping you get rid of the bad habit of
using a single password for multiple websites.

Dispass is a console application, but also has a simple graphical interface.
'''

setup(
    name='DisPass',
    version=dispass.dispass.__version__,
    description=dispass.dispass.__doc__,
    author=dispass.dispass.__author__,
    author_email='benjamin@babab.nl',
    url='http://dispass.babab.nl/',
    download_url='http://pypi.python.org/pypi/DisPass/',
    packages = ['dispass'],
    license='ISC',
    long_description=long_desc,
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications',
        'Topic :: Internet',
        'Topic :: Office/Business',
        'Topic :: Security :: Cryptography',
        'Topic :: Utilities',
    ],
    scripts=['scripts/dispass', 'scripts/gdispass', 'scripts/dispass-label'],
    )
