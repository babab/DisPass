MANPAGE
******************************************************************************

SYNOPSIS
==============================================================================

dispass
-------

dispass [-cghoV?] [-f <labelfile>] [-s <string>] [--script]

dispass [-co] [-l <length>] [-a <algo>] [-n <sequence-number>] [--script] <label> [<label2>] [label3]  [...]

gdispass

dispass-label
-------------

dispass-label [-hlV] [-f <labelfile>] [--script]


SUMMARY
==============================================================================

DisPass is a passphrase generator for GNU/Linux, \*BSD, MacOS X and Windows.
It enables you to generate unique passphrases formed from a master password
and a label, helping you get rid of the bad habit of using a single password
for multiple websites. When using a different passphrase for every website,
the chance of abuse of your password on other sites (when a website leaks it)
is eliminated.
Dispass is a console application, but also has a simple graphical interface.


DOCUMENTATION
==============================================================================

label
   A label is a string that you use to identify the passphrase.
   This can be a domainname of the service the passphrase is used for,
   e.g. 'google.com'.

Since this program asks for a password/passphrase to generate another
password/passphrase, things may get a bit confusing. I've dediced to use the
words 'password' and 'passphrase' diffently and consistent.

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

When DisPass is executed as 'gdispass' or 'dispass -g',
the graphical version will be started.

You can use dispass by entering your labels after the dispass command and/or
you can store your labels in a textfile called a labelfile.


Using dispass to create one or more passphrases
-----------------------------------------------

You can start using dispass for e.g. google.com like this::

   $ dispass -c google.com

Now you will be asked to enter a password twice and after that your
passphrase will be shown on the screen. This will now be the passphrase you
will use for logging in to google.com
It can be created everytime you need it by running::

   $ dispass google.com

The ``-c`` argument we used before was just a way to make sure to not make
typos when creating passphrases for the first time. It is advised you use
this everytime you create a passphrase for a new label.

The passphrases created are 30 characters long by default, but some website's
may not validate such a long passphrase or you might want to make it even
longer. You can easily set a desired passphrase length using the ``-l`` flag.
If you wanted to make your google.com 18 chars you can run::

   $ dispass -c -l 18 google.com

Generating passphrases for multiple labels is just as easy::

   $ dispass google.com yahoo.com


Using a labelfile
=================

When dispass is run without arguments it will try to find a labelfile.
The location of this file varies and depends on the platform type you use,
the file flag and the environment variables that may be set:

You can override the location of the labelfile using the ``-f`` flag.
This can be a way for you to use different sets of labels/passphrases
with a different 'master' password for each set.

1. If -f flag is given, that value is used.
2. If environment var DISPASS_LABELFILE is set, that value is used.
3. If environment var XDG_CONFIG_HOME is set,
   ``$XDG_CONFIG_HOME/dispass/labels`` is used.
4. If none of the above applies, the labelfile will default to the following
   locations:

   * **GNU/Linux and Mac OS X**: ``~/.config/dispass/labels``
   * **\*BSD and other Unixen**: ``~/.config/dispass/labels``
   * **Windows**:   ``C:\Users\<username>\dispass\labels``

You can start by copying the labelfile from skel/dot.dispass to this location
and editing it by adding your own labels. Or you can just start writing the
file from scratch which really isn't a hard thing to do.

The labels need to be specified on a single line with optional arguments.
A typical labelfile might look like this::

   google.com length=18
   yahoo.com

Now, when running ``dispass`` without arguments it will create two
passphrases with varying lengths.


OPTIONS
==============================================================================

dispass
-------

Options (general):

-c, --create    use if this passphrase is new (check input PW)
-g, --gui       start guided graphical version of DisPass
-h, --help      show this help and exit
-o, --output    output passphrases to stdout
                (instead of the more secure way of displaying via curses)
-V, --version   show full version information and exit
--script        optimize input/output for 'wrapping' dispass

Options (when using labelfile):

-s <string>, --search=<string>      dispass label from file that uniquely
                                    matches <string>
-f <labelfile>, --file=<labelfile>  set location of labelfile

Options (when passing labels as arguments):

-l <length>, --length=<length>      set length of passphrase
                                    (default: 30, max: 171)
-a <algorithm>, --algo=<algorithm>  override algorithm for generating
                                    passphrase(s)
-n <number>, --number=<number>      override sequence number (default = 1)

dispass-label
-------------

-h, --help                          show help and exit
-l, --list                          print all labels and options found in
                                    labelfile
-V, --version                       show full version information and exit
-f <labelfile>, --file=<labelfile>  set location of labelfile
--script                            optimize input/output for 'wrapping'
                                    dispass-label


Using the graphical *gdispass* application
==============================================================================

You can start using gDisPass by running the ``gdispass`` executable.
Fill in a name for the label that you can easily remember.

To generate a passphrase for a new label, i.e. a label that you have never
used before, check the appropiate checkbox. This will allow you to enter the
(master) password twice. gDisPass will then compare the passwords to see if
they are the same. This is needed to minimize the risk of typos. It is advised
that you check the box everytime you create a passphrase for a new label.

Subsequential generation of passphrases for the same label most probably do
not need this check. You will likely be warned when/if you made a typo by
the system or website you want to authenticate for.

If you correctly entered a label and password, you can generate the passphrase
by pressing <Return> or by clicking the appropiate button. The resulting
passphrase will be focused and selected. On platforms that support it
(e.g. \*BSD or GNU/Linux) the passphrase will be automatically placed into
your copy/paste buffer.

Resetting all fields when you are done or when you need to quickly cancel the
generation (because someone is watching over your shoulders) can be done by
pressing <Escape> or by clicking the appropiate button.


Wrapping / scripting dispass
============================

You can use dispass entirely as you wish and create different interfaces
by using the appropiate libraries as long as it is allowed by the ISC license.

Dispass provides a way to make the behaviour and IO more suitable for
scripting by passing the ``--script`` option.


dispass
-------
If the ``--script`` flag is passed together with ``-o`` or ``--output``
the output will be optimized for easy parsing by other programs
and scripts by always printing one entry on a single line using
the following positions::

   Column  1-50 : label


dispass-label
-------------
If the ``--script`` flag is passed together with ``-l`` or ``--list``
the output will be optimized for easy parsing by other programs
and scripts by not printing the header and always printing one
entry on a single line using the following positions::

   Column  1-50: label           (50 chars wide)
   Column 52-54: length           (3 chars wide)
   Column 56-70: hash algo       (15 chars wide)
   Column 72-74: sequence number  (3 chars wide)

Otherwise an ascii table is printed with a variable width depending
on the length of the longest label. The table has a header but does
not display the hash algo until support for multiple hashing algos
is added.


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
   https://github.com/babab/DisPass/

IRC
   #dispass at Freenode (chat.freenode.net)

Emacs wrapper
   https://github.com/ryuslash/dispass.el


.. vim: set et ts=3 sw=3 sts=3 ai:
