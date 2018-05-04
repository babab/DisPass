Using gdispass
==============

Before you start using ``gDispass``, make sure that the Tkinter
library is available. Here are some instructions to help you along:

Debian / Ubuntu
   Make sure the ``python-tk`` package is installed::

      sudo apt-get install python-tk

OpenBSD
   Make sure the ``python-tk`` package is installed::

      pkg_add -i python-tk

Archlinux
   The tkinter Python library is included in the ``python`` package,
   to make it work you need to be sure the ``tk`` package is
   installed::

      sudo pacman -S tk

You can start using gDisPass by running the ``gdispass`` executable.
Fill in a name for the label that you can easily remember.

To generate a passphrase for a new label, i.e. a label that you have
never used before, check the appropriate checkbox. This will allow you
to enter the (master) password twice. gDisPass will then compare the
passwords to see if they are the same. This is needed to minimize the
risk of typos. It is advised that you check the box everytime you
create a passphrase for a new label.

Subsequential generation of passphrases for the same label most probably do
not need this check. You will likely be warned when/if you made a typo by
the system or website you want to authenticate for.

If you correctly entered a label and password, you can generate the
passphrase by pressing <Return> or by clicking the appropriate button.
The resulting passphrase will be focused and selected. On platforms
that support it (e.g. \*BSD or GNU/Linux) the passphrase will be
automatically placed into your copy/paste buffer.

Resetting all fields when you are done or when you need to quickly
cancel the generation (because someone is watching over your
shoulders) can be done by pressing <Escape> or by clicking the
appropriate button.
