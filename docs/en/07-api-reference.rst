API Reference
=============

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Core modules
------------

algos
#####

The algos module is the most important part of DisPass. The algorithms
DisPass uses to create the passphrases are defined as separate classes
in the `dispass.algos` module.

.. automodule:: dispass.algos
   :members:

dispass
#######

.. automodule:: dispass.dispass
   :members:

Interface modules
-----------------

cli
###

.. automodule:: dispass.cli
   :members:

gui
###

.. automodule:: dispass.gui
   :members:

filehandler
###########

.. automodule:: dispass.filehandler
   :members:

interactive_editor
##################

.. automodule:: dispass.interactive_editor
   :members:


Subcommand modules
------------------

Subcommands are defined in the `dispass.commands` package as separate modules
containing a class derived from `pycommand.CommandBase`.

add
###

.. automodule:: dispass.commands.add
   :members:

generate
########

.. automodule:: dispass.commands.generate
   :members:

gui
###

.. automodule:: dispass.commands.gui
   :members:

help
####

.. automodule:: dispass.commands.help
   :members:

increment
#########

.. automodule:: dispass.commands.increment
   :members:

list
####

.. automodule:: dispass.commands.list
   :members:

remove
######

.. automodule:: dispass.commands.remove
   :members:

version
#######

.. automodule:: dispass.commands.version
   :members:
