Development documentation
******************************************************************************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Core modules
==============================================================================

algos
-----

The algos module is the most important part of DisPass. The algorithms
DisPass uses to create the passphrases are defined as separate classes
in the `dispass.algos` module.

.. automodule:: dispass.algos
   :members:

common
------

.. automodule:: dispass.common
   :members:

dispass
-------

.. automodule:: dispass.dispass
   :members:

Interface modules
==============================================================================


cli
---

.. automodule:: dispass.cli
   :members:

gui
---

.. automodule:: dispass.gui
   :members:

filehandler
-----------

.. automodule:: dispass.filehandler
   :members:

interactive_editor
------------------

.. automodule:: dispass.interactive_editor
   :members:

Subcommands
==============================================================================

Subcommands are defined in the `dispass.commands` package as separate modules
containing a class derived from `dispass.common.BaseCommand`.

add
---

.. automodule:: dispass.commands.add
   :members:

generate
--------

.. automodule:: dispass.commands.generate
   :members:

gui
---

.. automodule:: dispass.commands.gui
   :members:

help
----

.. automodule:: dispass.commands.help
   :members:

list
----

.. automodule:: dispass.commands.list
   :members:

rm
--

.. automodule:: dispass.commands.rm
   :members:

version
-------

.. automodule:: dispass.commands.version
   :members:
