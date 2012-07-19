# vim: set et ts=4 sw=4 sts=4 ai:

from distutils.core import setup
import dispass.dispass

long_desc = '''DisPass is a passphrase generator for GNU/Linux, \*BSD, MacOS X
and Windows.
It enables you to generate unique passphrases formed from a master password
and a label, helping you get rid of the bad habit of using a single password
for multiple websites. When using a different passphrase for every website,
the chance of abuse of your password on other sites (when a website leaks it)
is eliminated.
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
    scripts=['scripts/dispass', 'scripts/gdispass', 'scripts/dispass-label'],
    )
