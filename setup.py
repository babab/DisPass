# vim: set et ts=4 sw=4 sts=4 ai:

from setuptools import setup
import dispass.dispass

setup(
    name='DisPass',
    version=dispass.dispass.__version__,
    description=dispass.dispass.__doc__,
    author=dispass.dispass.__author__,
    author_email='benjamin@althu.es',
    url='http://dispass.org/',
    download_url='http://pypi.python.org/pypi/DisPass/',
    packages=['dispass', 'dispass.commands'],
    license='ISC',
    long_description=open('README.rst').read(),
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
    scripts=['bin/dispass', 'bin/gdispass'],
    install_requires=['pycommand']
    )
