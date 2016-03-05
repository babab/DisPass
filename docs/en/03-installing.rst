Downloading/Installing
**********************

Python 2.7 is required for running dispass.

If you are using Archlinux, it is advised to install dispass
`from the AUR <https://aur.archlinux.org/packages.php?K=dispass>`_.


Using pip to download from the Python Package Index
===================================================

The recommended way is to download and install directly from the PyPI
repository using pip:

.. code:: console

   sudo pip install dispass

This will install the dispass module in python's dist-packages folder.
You can now use dispass by executing the ``dispass`` and/or ``gdispass``
scripts placed under '/usr/local/bin/' or '/usr/bin/'.

The PyPI project page is at http://pypi.python.org/pypi/DisPass/


Latest (development) version
============================

Clone git repo:

.. code:: console

   git clone git://github.com/dispass/dispass.git
   cd dispass

Then you can either (in order of my personal preference):

1. Install using the Makefile, this will perform all the steps in
   option 2 (below):

.. code:: console

   sudo make install

2. Install manually through pip, and install manpage:

.. code:: console

   python setup.py sdist
   sudo pip install dist/DisPass-<version>.tar.gz
   sudo gzip -c dispass.1 > dispass.1.gz
   sudo mv dispass.1.gz /usr/share/man/man1/

3. Install manually (no manpage):

.. code:: console

   sudo python setup.py install


Upgrade or uninstall with pip
==============================================================================

You can easily upgrade to newer versions using pip:

.. code:: console

   sudo pip install --upgrade dispass

If you have installed dispass using pip, you can easily uninstall at
any moment by running:

.. code:: console

   sudo pip uninstall dispass
