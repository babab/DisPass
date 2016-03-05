Using the *dispass* command line app
******************************************************************************

::

   usage: dispass [options] <command> [<args>]

   Commands:
      add          add a new label to labelfile
      generate     generate passphrases for one or more labels
      gui          start the graphical version of DisPass
      help         show this help information
      increment    increment the sequence number of a label
      list         print a formatted table of labelfile contents
      rm           remove label from labelfile
      update       update length, algo or seqno of a label
      version      show full version information

   Options:
   -f <labelfile>, --file=<labelfile>  override labelfile
   -h, --help                          show this help information
   -V, --version                       show full version information

   See 'dispass help <command>' for more information on a specific command.


dispass add
==============================================================================

::

   usage: dispass add [-n] [-s] <labelspec>
          dispass add [-i] [-h]

   Add a new label to the labelfile and generate passphrase.
   The labelspec looks like this:

       label[:size[:algorithm[:sequence_number]]]

   Options:
   -i, --interactive  add label in an interactive manner
   -h, --help         show this help information
   -n, --dry-run      do not actually add label to labelfile
   -s, --silent       do not print success message


dispass disable
==============================================================================

::

   usage: dispass disable [<options>] <label>

   Disable a label without throwing it away.

   Options:
   -h, --help     show this help information
   -n, --dry-run  do not actually update label in labelfile
   -s, --silent   do not print success message


dispass enable
==============================================================================

::

   usage: dispass enable [<options>] <label>

   Enable a label.

   Options:
   -h, --help     show this help information
   -n, --dry-run  do not actually update label in labelfile
   -s, --silent   do not print success message


dispass generate
==============================================================================

::

   usage: dispass generate [options] <label> [<label2>] [<label3>] [...]

   Generate passphrases for one or more labels

   Options:
   -h, --help                            show this help information
   -l <length>, --length=<length>        length of passphrase
   -a <algorithm>, --algo=<algorithm>    algorithm to use for generation
   -s <seqno>, --seqno=<seqno>           sequence number to use for generation
   -p <password>, --password=<password>  password to use for generation
   -o, --stdout                          output passphrase(s) directly to stdout
   --silent                              do not show a prompt when errors occur


dispass gui
==============================================================================

::

   usage: dispass gui [-h]

   Start the graphical version of DisPass.

   Options:
   -h, --help  show this help information


dispass increment
==============================================================================

::

   usage: dispass increment [-n] [-s] <label>
          dispass increment [-h]

   Increment the sequence number of a label

   Options:
   -h, --help     show this help information
   -n, --dry-run  do not actually update label in labelfile
   -s, --silent   do not print success message

dispass list
==============================================================================

::

   usage: dispass list [-h] [--script]

   Print a formatted table of labelfile contents

   If --script is passed the output will be optimized for easy
   parsing by other programs and scripts by not printing the header
   and always printing one entry on a single line using the
   following positions:

   Column  1-50: label            50 chars wide
   Column 52-54: length            3 chars wide
   Column 56-70: hash algo        15 chars wide
   Column 72-74: sequence number   3 chars wide
   Column 76-77: disabled          1 char wide

   Options:
   -a, --all   include disabled labels
   -h, --help  show this help information
   --script    output in fixed columns


dispass rm
==============================================================================

::

   usage: dispass remove [-n] [-s] <labelname>
          dispass remove [-i] [-h]

   Remove label from labelfile

   Options:
   -i, --interactive  add label in an interactive manner
   -h, --help         show this help information
   -n, --dry-run      do not actually remove label from labelfile
   -s, --silent       do not print success message


dispass update
==============================================================================

::

   usage: dispass update [-n] [-s] <label> [<size>]:[<algorithm>]:[<sequence_number>]
          dispass update [-h]

   Update information for a label

   Options:
   -h, --help     show this help information
   -n, --dry-run  do not actually update label in labelfile
   -s, --silent   do not print success message


dispass version
==============================================================================

::

   usage: dispass version

   Show full version information


Using dispass to create one or more passphrases
===============================================

You can start using dispass for e.g. google.com like this::

   $ dispass -c google.com

The passphrases created are 30 characters long by default, but some
website's may not validate such a long passphrase or you might want to
make it even longer. You can easily set a desired passphrase length
using the ``-l`` flag. Hotmail passwords are limited to 16 characters::

   $ dispass -l 18 hotmail

Generating passphrases for multiple labels is just as easy::

   $ dispass google hotmail YaHo0 "P0551bly*a81t)H4rd2rmbr"

Labels are case-sensitive and digits and special characters can be used.
You should try to name labels in a way that you can easily 'dispass' a
passphrase on any computer/device that has DisPass at any given moment.
You are encouraged to store your labels in a labelfile for convenience
though.

Using a labelfile
-----------------

When dispass is run without arguments it will try to find a labelfile.
The location of this file varies and depends on the platform type you use,
the file flag and the environment variables that may be set:

You can override the location of the labelfile using the ``-f`` flag.
This can be a way for you to use different sets of labels/passphrases
with a different 'master' password for each set.

1. If -f flag is given, that value is used.
2. If environment var DISPASS_LABELFILE is set, that value is used.
3. If environment var XDG_DATA_HOME is set,
   ``$XDG_DATA_HOME/dispass/labels`` is used.

4. If none of the above applies, the labelfile will default to the following
   locations:

   * **GNU/Linux and Mac OS X**: ``~/.dispass/labels``
   * **\*BSD and other Unixen**: ``~/.dispass/labels``
   * **Windows**:   ``C:\Users\<username>\dispass\labels``

