Downloading/Installing
**********************

Python 3.4 or higher is required for running DisPass. The last version
that supports Python 2.7 is DisPass 0.3.0


Using pip to download from the Python Package Index
===================================================

The recommended way is to download and install the latest stable version
directly from the PyPI repository using pip:

.. code:: console

   pip install --user dispass

This will install the dispass package in $HOME/.local.
You can now use dispass by running the ``dispass`` and/or ``gdispass``
executables.


Upgrade or uninstall with pip
==============================================================================

You can easily upgrade to newer versions using pip:

.. code:: console

   pip install --user -U dispass

If you have installed dispass using pip, you can easily uninstall at
any moment by running:

.. code:: console

   pip uninstall dispass

Zsh completion, freedesktop configuration and logo's
====================================================

It is recommended to also install the zsh completion, desktop
configuration and logo files. These files are not directly supported in
a Windows environment, but can be used under Cygwin.

You can downloading an archive from
`PyPI <https://pypi.org/project/DisPass/#files>`_ or
`Github <https://github.com/babab/DisPass/releases>`_.

Extract the archive and change directory.

.. hint::

   Depending on the type of system, you may have to change some path
   locations. See the top of the Makefile. You can override them by
   creating a ``config.mk`` file.

Then unpack it and install (as root):

.. code:: console

   sudo make install-metafiles
