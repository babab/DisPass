Using dispass
=============

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

Labels are case-sensitive and digits and special characters can be
used. You should try to name labels in a way that you can easily
'dispass generate' a passphrase on any computer/device that has
DisPass at any given moment. You are encouraged to store your labels
in a labelfile for convenience though.

dispass
-------

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
-----------

.. code:: console

   usage: dispass add [-g] [-n] [-s] <labelspec> [<labelspec2>] [...]
          dispass add [-i] [-g] [-h]

   Add a new label to the labelfile and generate passphrase.
   The labelspec looks like this:

       label[:size[:algorithm[:sequence_number]]]

   Options:
   -i, --interactive  add label in an interactive manner
   -g, --generate     immediately generate passphrase after adding it
   -h, --help         show this help information
   -n, --dry-run      do not actually add label to labelfile
   -s, --silent       do not print success message



dispass disable
---------------

.. code:: console

   usage: dispass disable <label>

   Disable a label without throwing it away

   Options:
   -h, --help     show this help information
   -n, --dry-run  do not actually update label in labelfile
   -s, --silent   do not print success message


dispass enable
--------------

.. code:: console

   usage: dispass enable <label>

   Enable a label

   Options:
   -h, --help     show this help information
   -n, --dry-run  do not actually update label in labelfile
   -s, --silent   do not print success message


dispass generate
----------------

.. code:: console

   usage: dispass generate [options] <label> [<label2>] [<label3>] [...]

   Generate passphrases for one or more labels

   Use the '-v' flag to ask for password twice to avoid typing errors

   Options:
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

.. code:: console

   usage: dispass gui [-h]

   Start the graphical version of DisPass.

   Options:
   -h, --help  show this help information


dispass help
------------

.. code:: console

   usage: dispass help [<command>]

   Show help information


dispass increment
-----------------

.. code:: console

   usage: dispass increment [-n] [-s] <label>
          dispass increment [-h]

   Increment the sequence number of a label

   Options:
   -h, --help     show this help information
   -n, --dry-run  do not actually update label in labelfile
   -s, --silent   do not print success message


dispass list
------------

.. code:: console

   usage: dispass list [-h] [-n] [--script]

   Print a formatted table of labelfile contents

   If --script is passed the output will be optimized for easy
   parsing by other programs and scripts by not printing the header
   and always printing one entry on a single line using the
   following positions:

   Column  1-50: labelname        50 chars wide
   Column 52-54: length            3 chars wide
   Column 56-70: hash algo        15 chars wide
   Column 72-74: sequence number   3 chars wide
   Column 76-77: disabled          1 char wide

   Options:
   -a, --all         include disabled labels
   -h, --help        show this help information
   -n, --names-only  only print names of the labels
   --script          output in fixed columns


dispass remove
--------------

.. code:: console

   usage: dispass remove [-n] [-s] <labelname> [<labelname2>] [...]
          dispass remove [-i] [-h]

   Remove label from labelfile

   Options:
   -i, --interactive  remove label in an interactive manner
   -h, --help         show this help information
   -n, --dry-run      do not actually remove label from labelfile
   -s, --silent       do not print success message


dispass update
--------------

.. code:: console

   usage: dispass update [-n] [-s] <label> [<size>]:[<algorithm>]:[<sequence_number>]
          dispass update [-h]

   Update information for a label

   Options:
   -h, --help     show this help information
   -n, --dry-run  do not actually update label in labelfile
   -s, --silent   do not print success message


dispass version
---------------

.. code:: console

   usage: dispass version

   Show full version information
