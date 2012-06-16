User Documentation
******************************************************************************

DisPass is a passphrase generator for Windows and Unix / Linux.
You can use it to create unique passwords for logging in to websites, servers
or any other kind of thing that requires login.
DisPass does not keep your passwords in a database but rather lets you
generate a unique passphrase formed from a master password and a label.
It is a command line app, but also has a simple graphical interface.


Downloading/Installing
==============================================================================

A recent version of Python 2 is required for running dispass.


Using pip to download from the Python Package Index
---------------------------------------------------

The recommended way is to download and install directly from the PyPI
repository using pip.

::

   $ sudo pip install dispass

You must have python's docutils installed in able to do so.
This will install the dispass module in python's dist-packages folder.
You can now run dispass using the 'dispass' and 'gdispass' scripts
placed under '/usr/local/bin/' or '/usr/bin/'.

The PyPI project page is at http://pypi.python.org/pypi/DisPass/


Latest (development) version
----------------------------

Clone git repo::

   $ git clone git://github.com/babab/DisPass.git
   $ cd dispass

Then you can either

1. Install through pip::

   $ python setup.py sdist
   $ sudo pip install dist/DisPass-0.1a7.tar.gz


2. Install manually::

   $ sudo python setup.py install


Update or uninstall
==============================================================================

You can easily upgrade to newer versions using pip::

   $ sudo pip install dispass --upgrade

If you have installed dispass using pip with,
you can easily uninstall at any moment::

   $ sudo pip uninstall dispass


Using the command line app
==============================================================================

**label**

A label is a string that you use to identify the password.
This can be a domainname of the service the password is used for
like e.g. 'google.com'.

You can use dispass by entering your labels after the dispass command and/or
you can store your labels in a textfile called a labelfile.

Using dispass to create one or more labels
------------------------------------------

You can start using dispass for e.g. google.com like this::

   $ dispass -c google.com

Now you will be asked to enter a password twice and after that your
passphrase will be shown on the screen. This will now be the passphrase you
will use for logging in to google.com
It can be created everytime you need it by running::

   $ dispass google.com

The `-c` argument before was just a way to make sure you do not make typos
when creating passphrases for the first time. It is advised you use this
everytime you create a passphrase for a new label.

The passphrases created are 30 characters long by default, but some website's
may not validate such a long password or you might want to make it even
longer. You can easily set a desired passphrase length using the `-l` flag.
If you wanted to make your google.com 18 chars you can run::

   $ dispass -c -l 18 google.com

Generating passwords for multiple labels is just as easy::

   $ dispass google.com yahoo.com


Using a labelfile
-----------------

When dispass is run without arguments it will try to find a labelfile.
The location of this file varies and depends on the platform type you use:

 * `GNU/Linux`: ~/.dispass
 * `*BSD`:      ~/.dispass

You can start by copying the labelfile from skel/dot.dispass to this location
and editing it by adding your own labels. Or you can just start writing the
file from scratch which really isn't a hard thing to do.

The labels need to be specified on a single line with optional arguments.
A typical labelfile might look like this::

   google.com length=18
   yahoo.com

Dispass will now create two passphrases with varying lengths.

You can override the location of the labelfile using the `-f` flag.
This can be a way for you to use different sets of labels/passphrases
with a different 'master' password for each set.

All options
-----------

::

   DisPass 0.1a7 - http://dispass.babab.nl/

   When DisPass is executed as 'gdispass' or 'dispass -g',
   the graphical version will be started.

   USAGE: dispass [-cghoV] [-f labelfile]
          dispass [-co] [-l length] label [label2] [label3] [...]
          gdispass

   Options:
   -c, --create    use if this passphrase is new (check input PW)
   -g, --gui       start guided graphical version of DisPass
   -h, --help      show this help and exit
   -o, --output    output passphrases to stdout (instead of the
                   more secure way of displaying via curses)
   -V, --version   show full version information and exit

   -f <labelfile>, --file=<labelfile>
                   set location of labelfile (default: ~/.dispass)
   -l <length>, --length=<length>
                   set length of passphrase (default: 30, max: 171)

Using the graphical version
==============================================================================

No info yet.


Software license
==============================================================================

Copyright (c) 2011-2012 Benjamin Althues <benjamin@babab.nl>

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
