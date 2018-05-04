Downloading/Installing
**********************

Python 3.4 or higher is required for running DisPass.


Using pip to download from the Python Package Index
===================================================

The recommended way is to download and install directly from the PyPI
repository using pip:

.. code:: console

   sudo pip install -U dispass

This will install the dispass package in python's dist-packages folder.
You can now use dispass by running the ``dispass`` and/or ``gdispass``
executables.

It is recommended to also install the manpage, info documentation, zsh
completion, desktop configuration and logo files. You can do so by
downloading the tarball from
https://pypi.python.org/packages/source/D/DisPass/DisPass-0.4.0.tar.gz

.. code:: console

   wget https://pypi.python.org/packages/source/D/DisPass/DisPass-0.4.0.tar.gz

Then unpack it and install via make:

.. code:: console

   tar -xf DisPass-0.4.0.tar.gz
   cd DisPass-0.4.0
   sudo make install-metafiles


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

2. Install manually through pip, and install manpage, info
   documentation, zsh completion, desktop configuration and logo files:

   .. code:: console

      sudo pip install -r requirements.txt
      sudo pip install .
      gzip -c dispass.1 > dispass.1.gz
      gzip -c dispass.info > dispass.info.gz
      sudo install -Dm644 dispass.1.gz /usr/share/man/man1/dispass.1.gz
      sudo install -Dm644 dispass.info.gz /usr/share/info/dispass.info.gz
      sudo install -Dm644 zsh/_dispass /usr/share/zsh/site-functions/_dispass
      sudo install -Dm644 etc/dispass.desktop /usr/share/applications/dispass.desktop
      sudo install -Dm644 logo/logo24.png /usr/share/icons/hicolor/24x24/apps/dispass.png
      sudo install -Dm644 logo/logo32.png /usr/share/icons/hicolor/32x32/apps/dispass.png
      sudo install -Dm644 logo/logo64.png /usr/share/icons/hicolor/64x64/apps/dispass.png
      sudo install -Dm644 logo/logo128.png /usr/share/icons/hicolor/128x128/apps/dispass.png
      sudo install -Dm644 logo/logo256.png /usr/share/icons/hicolor/256x256/apps/dispass.png
      sudo install -Dm644 logo/logo512.png /usr/share/icons/hicolor/512x512/apps/dispass.png


3. Install manually (no manpage):

   .. code:: console

      sudo python setup.py install


Upgrade or uninstall with pip
==============================================================================

You can easily upgrade to newer versions using pip:

.. code:: console

   sudo pip install -U dispass

If you have installed dispass using pip, you can easily uninstall at
any moment by running:

.. code:: console

   sudo pip uninstall dispass
