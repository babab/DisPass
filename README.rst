DisPass
******************************************************************************

DisPass is a password manager for GNU/Linux, \*BSD, MacOS X and Windows.
It can be used as any traditional password manager, but has one key
difference. DisPass does not store your passwords anywhere, so you
can never lose them. It creates strong and unique passphrases formed
from a master password and a label (and some optional parameters),
helping you get rid of the bad habit of using a single password for
multiple websites. Dispass is a console application, but also has a
simple graphical interface.

Resources
=========

- Main website: https://dispass.org
- Python Package Index: http://pypi.python.org/pypi/DisPass
- Agile project management: https://waffle.io/babab/DisPass
- Github: https://github.com/babab/dispass
- Bitbucket: https://bitbucket.org/babab/dispass


Quick start
==============================================================================

These are quick instructions for the impatient, just wanting to check
out DisPass. For full documentation on using **DisPass**, visit
http://dispass.org

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

.. image:: https://raw.githubusercontent.com/babab/DisPass/master/docs/screencast.png
    :target: https://asciinema.org/a/38378


Software license
==============================================================================

DisPass is released under an ISC license, which is functionally
equivalent to the simplified BSD and MIT/Expat licenses, with language
that was deemed unnecessary by the Berne convention removed.

::

   Copyright (c) 2012-2016  Tom Willemse <tom@ryuslash.org>
   Copyright (c) 2011-2016  Benjamin Althues <benjamin@althu.es>

   Permission to use, copy, modify, and distribute this software for any
   purpose with or without fee is hereby granted, provided that the above
   copyright notice and this permission notice appear in all copies.

   THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
   WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
   MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
   ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
   WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
   ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
   OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

