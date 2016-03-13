MANPAGE
******************************************************************************

SYNOPSIS
==============================================================================

dispass [-f <labelfile>] [-h] [-V] <command> [<args>]

gdispass


SUMMARY
==============================================================================

DisPass is a password manager for GNU/Linux, \*BSD, MacOS X and Windows.
It can be used as any traditional password manager, but has one key
difference. DisPass does not store your passwords anywhere, so you
can never lose them. It creates strong and unique passphrases formed
from a master password and a label (and some optional parameters),
helping you get rid of the bad habit of using a single password for
multiple websites. Dispass is a console application, but also has a
simple graphical interface.

DOCUMENTATION
==============================================================================

Resources
---------

- Main website: https://dispass.org/
- Python Package Index: http://pypi.python.org/pypi/DisPass/
- Agile project management: https://waffle.io/babab/DisPass
- Github: https://github.com/babab/dispass/
- Bitbucket: https://bitbucket.org/babab/dispass/

Definitions
-----------

Here are some definitions which may help you understand the rest of the
documentation better.

label
   A label is a string that you use to identify the passphrase. This
   can be a domain name of the service the passphrase is used for,
   e.g. 'google.com'.

Since this program asks for a password/passphrase to generate another
password/passphrase, things may get a bit confusing. I've decided to use the
words 'password' and 'passphrase' differently and consistent.

password
   Use of the word 'password' is dedicated to the input password, i.e. the
   password you are asked to enter and only you know. Whenever you read
   password, this is the one I mean. The password needs to be at least 8
   characters long and does not have a maximum length.

passphrase
   With 'passphrase' I always mean the output passphrase, i.e. the passphrase
   that is unique and generated from a label, password and sequence number.
   Generated passphrases are 30 characters long. The length can be optionally
   changed.

Labelfile
---------

DisPass does not store your passwords or passphrases, but it does store
labels and their settings (algorithm, length and sequence_number) for
convenience. However, please keep in mind that you should try to name
labels in a way that you can easily 'dispass generate' a passphrase on
any computer/device that has DisPass at any given moment without having
your labelfile at hand.

When dispass is run without arguments it will try to find a labelfile.
The location of this file varies and depends on the platform type you use,
the file flag and the environment variables that may be set:

You can override the location of the labelfile using the
``-f <labelfile>, --file=<labelfile>`` flag. This can be a way for you
to use different sets of labels/passphrases with a different 'master'
password for each set.

1. If -f flag is given, that value is used.
2. If environment var DISPASS_LABELFILE is set, that value is used.
3. If environment var XDG_DATA_HOME is set,
   ``$XDG_DATA_HOME/dispass/labels`` is used.

4. If none of the above applies, the labelfile will default to the following
   locations:

   * **GNU/Linux and Mac OS X**: ``~/.dispass/labels``
   * **\*BSD and other Unixen**: ``~/.dispass/labels``
   * **Windows**:   ``C:\Users\<username>\dispass\labels``

Basic usage
-----------

You can start using dispass for e.g. google.com like this:

.. code:: console

   dispass generate google.com

The passphrases created are 30 characters long by default, but some
websites may not validate such a long passphrase or you might want to
make it even longer. You can easily set a desired passphrase length
using the ``-l`` flag. Hotmail passwords are limited to 16 characters:

.. code:: console

   dispass generate -l 16 hotmail

Generating passphrases for multiple labels is just as easy:

.. code:: console

   dispass generate google hotmail YaHo0 "P0551bly*a81t)H4rd2rmbr"

Labels are case-sensitive and digits and special characters can be used.
You should try to name labels in a way that you can easily generate a
passphrase on any computer/device that has DisPass at any given moment.

Label specifications
--------------------

While the above works fine without storing any information, you are
encouraged to store your labels in a labelfile for convenience. That
way, you don't have to use the ``-l 16`` option everytime you create
your hotmail password.

Labels have a specification that consists of the following parameters:

- length (the length of the passphrase)
- algorithm (the algorithm to use)
- sequence number (not used in default algorithm)

The **labelspec** looks like this::

   label[:size[:algorithm[:sequence_number]]]

Adding a label
--------------

You can save a new ``hotmail`` label with a length of 16 and generate the
passphrase in one go:

.. code:: console

   dispass add -g hotmail:16

The next time you generate a passphrase for ``hotmail`` using:

.. code:: console

   dispass generate hotmail

it will return the same passphrase as before (with a length of 16
characters).

Incrementing sequence numbers
-----------------------------

You might want to change the passphrase you enter into some system.
Of course, you can do this simply by using a different label, e.g.:
``Hotmail`` or ``hotmail-2``. You don't have to though.

DisPass supports dealing with this situation in the *dispass2* algorithm.
It basically gives you an option of *bumping* a passphrase by simply
incrementing a **sequence number**.

To use sequence numbers with the hotmail label from before you can
update it to use the dispass2 algorithm with sequence number 1:

.. code:: console

   dispass update hotmail 16:dispass2:1
   dispass generate hotmail

The next time you want to use a different passphrase, you can simply use

.. code:: console

   dispass increment hotmail
   dispass generate hotmail

Using gdispass
--------------

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


OPTIONS
==============================================================================

dispass
-------

-f <labelfile>, --file=<labelfile>  override labelfile
-h, --help                          show this help information
-V, --version                       show full version information

dispass add
-----------

Add a new label to the labelfile and generate passphrase.
The labelspec looks like this: ``label[:size[:algorithm[:sequence_number]]]``

dispass add [-g] [-n] [-s] <labelspec> [<labelspec2>] [...]

dispass add [-i] [-g] [-h]

-i, --interactive  add label in an interactive manner
-g, --generate     immediately generate passphrase after adding it
-h, --help         show this help information
-n, --dry-run      do not actually add label to labelfile
-s, --silent       do not print success message


dispass disable
---------------

Disable a label without throwing it away

dispass disable <label>

-h, --help     show this help information
-n, --dry-run  do not actually update label in labelfile
-s, --silent   do not print success message


dispass enable
--------------

Enable a label

dispass enable <label>

-h, --help     show this help information
-n, --dry-run  do not actually update label in labelfile
-s, --silent   do not print success message


dispass generate
----------------

Generate passphrases for one or more labels

Use the ``-v`` flag to ask for password twice to avoid typing errors

dispass generate [options] <label> [<label2>] [<label3>] [...]

-h, --help                            show this help information
-v, --verify                          verify password
-l <length>, --length=<length>        length of passphrase
-a <algorithm>, --algo=<algorithm>    algorithm to use for generation
-s <seqno>, --seqno=<seqno>           sequence number to use for generation
-p <password>, --password=<password>  password to use for generation
-o, --stdout                          output passphrase(s) directly to stdout
--silent                              do not show a prompt when errors occur


dispass gui
-----------

Start the graphical version of DisPass.

dispass gui [-h]

-h, --help  show this help information


dispass help
------------

Show help information

dispass help [<command>]


dispass increment
-----------------

Increment the sequence number of a label

dispass increment [-n] [-s] <label>

dispass increment [-h]

-h, --help     show this help information
-n, --dry-run  do not actually update label in labelfile
-s, --silent   do not print success message


dispass list
------------

Print a formatted table of labelfile contents

If ``--script`` is passed the output will be optimized for easy
parsing by other programs and scripts by not printing the header
and always printing one entry on a single line using the
following positions::

   Column  1-50: labelname        50 chars wide
   Column 52-54: length            3 chars wide
   Column 56-70: hash algo        15 chars wide
   Column 72-74: sequence number   3 chars wide
   Column 76-77: disabled          1 char wide

dispass list [-h] [-n] [--script]

-a, --all         include disabled labels
-h, --help        show this help information
-n, --names-only  only print names of the labels
--script          output in fixed columns


dispass remove
--------------

Remove label from labelfile

dispass remove [-n] [-s] <labelname> [<labelname2>] [...]

dispass remove [-i] [-h]

-i, --interactive  remove label in an interactive manner
-h, --help         show this help information
-n, --dry-run      do not actually remove label from labelfile
-s, --silent       do not print success message


dispass update
--------------

Update information for a label

dispass update [-n] [-s] <label> [<size>]:[<algorithm>]:[<sequence_number>]

dispass update [-h]

-h, --help     show this help information
-n, --dry-run  do not actually update label in labelfile
-s, --silent   do not print success message


dispass version
---------------

Show full version information

dispass version


Acknowledgements
==============================================================================

Many thanks go out to Tom (ryuslash) Willemsen for valuable contributions to
gdispass and the new algorithm. He also wrote an awesome wrapper for Emacs so
you can use DisPass in your favorite editor.


SEE ALSO
==============================================================================

Main website with full documentation
   http://dispass.babab.nl

The cheeseshop (PyPI) project page
   http://pypi.python.org/pypi/DisPass/

Github repository and Issue tracker
   https://github.com/dispass/dispass/

IRC
   #dispass at Freenode (chat.freenode.net)

Emacs wrapper
   http://ryuslash.org/projects/dispass.el.html


.. vim: set et ts=3 sw=3 sts=3 ai:
