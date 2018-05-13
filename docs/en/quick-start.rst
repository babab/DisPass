Quick start
==============================================================================

These are quick instructions for the impatient, just wanting to check
out DisPass. For full user documentation browse to the next sections.

Download
--------

Download DisPass from the Python Package Index with pip:

.. code:: console

   pip install --user dispass


Using DisPass for the first time
--------------------------------

For this example we will create a passphrase to use for a google account.

1. Create and save a label ``google`` to the labelfile:

   .. code:: console

       dispass add google

2. Generate the passphrase for the first time. Since you will need to
   register the passphrase with google we pass the ``--verify`` flag
   or simply ``-v`` so DisPass asks us to verify the password and we
   can avoid typing errors in the input password while creating the
   resulting passphrase for the first time:

   .. code:: console

       dispass generate --verify google


Mini screencast
---------------

Checkout the following mini screencast. In this demo the label is added
interactively.

.. raw:: html

   <script type="text/javascript" src="https://asciinema.org/a/38378.js" id="asciicast-38378" async></script>
