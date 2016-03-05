API Reference
=============

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Core modules
------------

dispass.algos
#############

The algos module is the most important part of DisPass. The algorithms
DisPass uses to create the passphrases are defined as separate classes
in the `dispass.algos` module.

.. automodule:: dispass.algos
   :members:

dispass.dispass
###############

.. automodule:: dispass.dispass
   :members:

Interface modules
-----------------

dispass.cli
###########

.. automodule:: dispass.cli
   :members:

dispass.gui
###########

.. automodule:: dispass.gui
   :members:

dispass.filehandler
###################

.. automodule:: dispass.filehandler
   :members:

dispass.interactive_editor
##########################

.. automodule:: dispass.interactive_editor
   :members:


Subcommand modules
------------------

Subcommands are defined in the `dispass.commands` package as separate modules
containing a class derived from `pycommand.CommandBase`.

dispass.commands.add
####################

.. automodule:: dispass.commands.add
   :members:

dispass.commands.generate
#########################

.. automodule:: dispass.commands.generate
   :members:

dispass.commands.gui
####################

.. automodule:: dispass.commands.gui
   :members:

dispass.commands.help
#####################

.. automodule:: dispass.commands.help
   :members:

dispass.commands.increment
##########################

.. automodule:: dispass.commands.increment
   :members:

dispass.commands.list
#####################

.. automodule:: dispass.commands.list
   :members:

dispass.commands.remove
#######################

.. automodule:: dispass.commands.remove
   :members:

dispass.commands.version
########################

.. automodule:: dispass.commands.version
   :members:
