README
******************************************************************************

DisPass is a password manager for GNU/Linux, \*BSD, MacOS X and Windows. It
can be used as any traditional password manager, but has one key difference.
DisPass does not store your passwords anywhere, so you can never lose them.

It creates strong and unique passphrases formed from a master password and a
label (and some optional parameters), helping you get rid of the bad habit of
using a single password for multiple websites.

Dispass is a console application, but also has a simple graphical interface.

DisPass has several homes on the Internet:

Main website
   http://dispass.babab.nl

The cheeseshop (PyPI) project page
   http://pypi.python.org/pypi/DisPass/

Github repository and Issue tracker
   https://github.com/dispass/dispass/

Bitbucket repository
   https://bitbucket.org/babab/dispass/

Here are some definitions which may help you understand the rest of the
documentation better.

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


Downloading/Installing
==============================================================================

Python 2.7 or higher is required for running dispass.


Using pip to download from the Python Package Index
---------------------------------------------------

The recommended way is to download and install directly from the PyPI
repository using pip::

   $ sudo pip install dispass

This will install the dispass module in python's dist-packages folder.
You can now use dispass by executing the ``dispass``, ``dispass-label``
and/or ``gdispass`` scripts placed under '/usr/local/bin/' or
'/usr/bin/'.

The PyPI project page is at http://pypi.python.org/pypi/DisPass/


Latest (development) version
----------------------------

Clone git repo::

   $ git clone git://github.com/dispass/dispass.git
   $ cd dispass

Then you can either (in order of my personal preference):

1. Install using the Makefile, this will perform all the steps in
   option 2 (below)::

   $ sudo make install

2. Install manually through pip, and install manpage::

   $ python setup.py sdist
   $ sudo pip install dist/DisPass-<version>.tar.gz
   $ sudo gzip -c dispass.1 > dispass.1.gz
   $ sudo mv dispass.1.gz /usr/share/man/man1/

3. Install manually::

   $ sudo python setup.py install


Upgrade or uninstall with pip
==============================================================================

You can easily upgrade to newer versions using pip::

   $ sudo pip install --upgrade dispass

If you have installed dispass using pip, you can easily uninstall at
any moment by running::

   $ sudo pip uninstall dispass


Using the *dispass* command line app
==============================================================================

When DisPass is executed as 'gdispass' or 'dispass -g',
the graphical version will be started.

You can use dispass by entering your labels after the dispass command and/or
you can store your labels in a textfile called a labelfile.

:USAGE: dispass [options]

        dispass [options] <label> [<label2>] [label3]  [...]

        gdispass

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


Using dispass to create one or more passphrases
-----------------------------------------------

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

You can edit the labelfile(s) by using the ``dispass-label`` program.

Creating and searching stored labels
------------------------------------

When creating a new label/password combination you can store the label
and it's arguments by using the ``-c`` flag, this will ask for your
password twice so you can be asured to avoid typing errors::

   $ dispass -c -l 16 hotmail.com

Now you will be asked to enter a password twice and after that your
passphrase will be shown on the screen. It can be re-created everytime you
need it by searching for a label using the ``-s`` flag::

   $ dispass -s hotm

Only part of the label is needed, as long as the (sub)string is unique.


Using the *dispass-label* command line app
==============================================================================

:USAGE: dispass-label [-hlV] [-f <labelfile>] [-a|--add <labelspec>]
        [-r|--remove <labelname] [--script]

Options:

-h, --help                          show help and exit
-l, --list                          print all labels and options found in
                                    labelfile
-V, --version                       show full version information and exit
-f <labelfile>, --file=<labelfile>  set location of labelfile
-a, --add <labelspec>               add a new label to the labelfile, the
                                    labelspec looks like this:
                                    label[:size[:algorithm[:sequence_number]]]
-r, --remove <labelname>            remove a label from the labelfile
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


Got Emacs? You can use the Emacs wrapper
========================================

If you have Emacs you can use the Emacs wrapper created and maintained by
Tom Willemsen (ryuslash).

You can find it at: http://ryuslash.org/projects/dispass.el.html


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


Support / ideas / questions / suggestions
==============================================================================

Issue tracker at Github: https://github.com/dispass/dispass/issues

A mailing list is available: dispass@librelist.com

You can also visit #dispass at Freenode (chat.freenode.net) with your favorite
IRC client.


Acknowledgements
==============================================================================

Many thanks go out to Tom (ryuslash) Willemsen for valuable contributions to
gdispass and the new algorithm. He also wrote an awesome wrapper for Emacs so
you can use DisPass in your favorite editor.


Software license
==============================================================================

Copyright (c) 2011, 2012, 2013  Benjamin Althues <benjamin@babab.nl>

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





.. vim: set et ts=3 sw=3 sts=3 ai:
