Quick start
==============================================================================

These are quick instructions for the impatient, just wanting to check
out DisPass. For full user documentation browse to the next sections.

Download
--------

Download DisPass from the Python Package Index with pip. As root (using
sudo), do the following:

.. code:: console

   sudo pip install dispass


If you are using Archlinux, it is advised to install dispass
`from the AUR <https://aur.archlinux.org/packages.php?K=dispass>`_.


Using DisPass for the first time
--------------------------------

For this example we will create a passphrase to use for a google account.

Create and save a label ``google`` to the labelfile:

.. code:: console

    dispass add google

Generate the passphrase for the first time. Since you will need to
register the passphrase with google we pass the ``--verify`` flag
or simply ``-v`` to avoid typing errors in the input password while
creating the resulting passphrase for the first time:

.. code:: console

    dispass generate --verify google


Mini screencast
---------------

Checkout the following mini screencast. In this demo the label is added
interactively.

.. image:: ../../dispass-mini-screencast.gif
