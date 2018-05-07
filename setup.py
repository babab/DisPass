# vim: set et ts=4 sw=4 sts=4 ai:

from setuptools import setup
import dispass.dispass

setup(
    name='DisPass',
    version=dispass.dispass.__version__,
    description=dispass.dispass.__doc__,
    author=dispass.dispass.__author__,
    author_email='benjamin@babab.nl',
    url='http://dispass.org/',
    download_url='http://pypi.python.org/pypi/DisPass/',
    packages=['dispass', 'dispass.commands', 'dispass.commands.decorators'],
    python_requires='>=3.4',
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
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only'
        'Programming Language :: Python :: 3.4'
        'Programming Language :: Python :: 3.5'
        'Programming Language :: Python :: 3.6'
        'Topic :: Security :: Cryptography',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'dispass = dispass.main:console',
        ],
        'gui_scripts': [
            'gdispass = dispass.main:gui',
        ]
    },
    install_requires=['pycommand']
    )
