Using dispass
=============

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

Subcommands
-----------

DisPass has many commands around managing the labels. You can see all
available subcommands and options of dispass by running ``dispass
--help`` or just running ``dispass`` wihout any arguments.

.. code:: console

   usage: dispass [options] <command> [<args>]

   Commands:
      add          add a new label to labelfile
      disable      disable a label without throwing it away
      enable       enable a label
      generate     generate passphrases for one or more labels
      gui          start the graphical version of DisPass
      help         show this help information
      increment    increment the sequence number of a label
      list         print a formatted table of labelfile contents
      remove       remove label from labelfile
      update       update length, algo or seqno of a label
      version      show full version information

   Options:
   -f <labelfile>, --file=<labelfile>  override labelfile
   -h, --help                          show this help information
   -V, --version                       show full version information

   See 'dispass help <command>' for more information on a specific command.


dispass add
###########

Add a new label to the labelfile and generate passphrase.
The labelspec looks like this: ``label[:size[:algorithm[:sequence_number]]]``

::

   usage: dispass add [-g] [-n] [-s] <labelspec> [<labelspec2>] [...]
          dispass add [-i] [-g] [-h]

-i, --interactive  add label in an interactive manner
-g, --generate     immediately generate passphrase after adding it
-h, --help         show this help information
-n, --dry-run      do not actually add label to labelfile
-s, --silent       do not print success message


dispass disable
###############

Disable a label without throwing it away

::

   usage: dispass disable <label>

-h, --help     show this help information
-n, --dry-run  do not actually update label in labelfile
-s, --silent   do not print success message


dispass enable
##############

Enable a label

::

   usage: dispass enable <label>

-h, --help     show this help information
-n, --dry-run  do not actually update label in labelfile
-s, --silent   do not print success message


dispass generate
################

Generate passphrases for one or more labels

Use the ``-v`` flag to ask for password twice to avoid typing errors

::

   usage: dispass generate [options] <label> [<label2>] [<label3>] [...]

-h, --help                            show this help information
-v, --verify                          verify password
-l <length>, --length=<length>        length of passphrase
-a <algorithm>, --algo=<algorithm>    algorithm to use for generation
-s <seqno>, --seqno=<seqno>           sequence number to use for generation
-p <password>, --password=<password>  password to use for generation
-o, --stdout                          output passphrase(s) directly to stdout
--silent                              do not show a prompt when errors occur


dispass gui
###########

Start the graphical version of DisPass.

::

   usage: dispass gui [-h]

-h, --help  show this help information


dispass help
############

Show help information

::

   usage: dispass help [<command>]


dispass increment
#################

Increment the sequence number of a label

::

   usage: dispass increment [-n] [-s] <label>
          dispass increment [-h]

-h, --help     show this help information
-n, --dry-run  do not actually update label in labelfile
-s, --silent   do not print success message


dispass list
############

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

::

   usage: dispass list [-h] [-n] [--script]

-a, --all         include disabled labels
-h, --help        show this help information
-n, --names-only  only print names of the labels
--script          output in fixed columns


dispass remove
##############

Remove label from labelfile

::

   usage: dispass remove [-n] [-s] <labelname> [<labelname2>] [...]
          dispass remove [-i] [-h]

-i, --interactive  remove label in an interactive manner
-h, --help         show this help information
-n, --dry-run      do not actually remove label from labelfile
-s, --silent       do not print success message


dispass update
##############

Update information for a label

::

   usage: dispass update [-n] [-s] <label> [<size>]:[<algorithm>]:[<sequence_number>]
          dispass update [-h]

-h, --help     show this help information
-n, --dry-run  do not actually update label in labelfile
-s, --silent   do not print success message


dispass version
###############

Show full version information

::

   usage: dispass version

