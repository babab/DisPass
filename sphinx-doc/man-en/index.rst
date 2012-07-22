MANPAGE
******************************************************************************

SYNOPSIS
==============================================================================

dispass
-------

dispass [-cghoV] [-f <labelfile>] [-s <string>] [--script]

dispass [-co] [-l <length>] <label> [<label2>] [...] [--script]

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
   password, this is the one I mean.

passphrase
   With 'passphrase' I always mean the output passphrase, i.e. the passphrase
   that is unique and generated from a label and password

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
The location of this file varies and depends on the platform type you use:

 * **GNU/Linux and Mac OS X**: ``~/.dispass``
 * **\*BSD and other Unixen**: ``~/.dispass``
 * **Windows**:   ``C:\Users\<username>\.dispass``

You can start by copying the labelfile from skel/dot.dispass to this location
and editing it by adding your own labels. Or you can just start writing the
file from scratch which really isn't a hard thing to do.

The labels need to be specified on a single line with optional arguments.
A typical labelfile might look like this::

   google.com length=18
   yahoo.com

Now, when running ``dispass`` without arguments it will create two
passphrases with varying lengths.

You can override the location of the labelfile using the ``-f`` flag.
This can be a way for you to use different sets of labels/passphrases
with a different 'master' password for each set.


OPTIONS
==============================================================================

dispass
-------

Short options:

-c                  use if this passphrase is new (check input PW)
-g                  start guided graphical version of DisPass
-h                  show this help and exit
-o                  output passphrases to stdout
                    (instead of the more secure way of displaying via curses)
-V                  show full version information and exit
-l <length>         set length of passphrase (default: 30, max: 171)
-s <string>         dispass label from file that uniquely matches <string>
-f <labelfile>      set location of labelfile (default: ~/.dispass)

Long options:

--create            use if this passphrase is new (check input PW)
--gui               start guided graphical version of DisPass
--help              show this help and exit
--output            output passphrases to stdout
                    (instead of the more secure way of displaying via curses)
--version           show full version information and exit
--length <length>   set length of passphrase (default: 30, max: 171)
--search <string>   dispass label from file that uniquely matches <string>
--file <labelfile>  set location of labelfile (default: ~/.dispass)
--script            optimize input/output for 'wrapping' dispass

dispass-labels
--------------

Short options:

-h                  show this help and exit
-l                  print all labels and options found in labelfile
-V                  show full version information and exit
-f <labelfile>      set location of labelfile (default: ~/.dispass)

Long options:

--help              show this help and exit
--list              print all labels and options found in labelfile
--version           show full version information and exit
--file=<labelfile>  set location of labelfile (default: ~/.dispass)
--script            optimize input/output for 'wrapping' dispass-label


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

   #dispass at OFTC (irc.oftc.net)

Emacs wrapper
   https://github.com/ryuslash/dispass.el


.. vim: set et ts=3 sw=3 sts=3 ai:
