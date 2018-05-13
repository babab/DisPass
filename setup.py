# vim: set et ts=4 sw=4 sts=4 ai:

from setuptools import setup

setup(
    name='DisPass',
    version='0.4.0.dev0',
    description=(
        'Disperse and dispell passwords with a free alternative manager.'
    ),
    author='Benjamin Althues',
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
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
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
