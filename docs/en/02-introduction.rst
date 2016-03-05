Introduction
============

Resources
---------

- `Main website <http://dispass.org>`_
- `Python Package Index (PyPI) page <http://pypi.python.org/pypi/DisPass/>`_
- `Waffle.io board <https://waffle.io/babab/DisPass>`_
- `Github repository and Issue tracker <https://github.com/babab/dispass/>`_
- `Bitbucket repository <https://bitbucket.org/babab/dispass/>`_

Definitions
-----------

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
