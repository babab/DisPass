Change Log
----------

v0.3.0 - released March 18th, 2016
##################################

Added
*****

* Option for disabling/enabling labels
* Zsh completion for dispass (sub)command(s)
* Interactive modes for ``add`` and ``rm`` commands
* Algorithm and sequence number fields (GUI)
* pycommand dependency for command argument parsing (extracted from DisPass)
* Info documentation (different from manpage, same as the website)

Changed
*******

* Lookup label parameters from labelfile
* Use different subcommands for all actions

  - add
  - disable
  - enable
  - generate
  - gui
  - help
  - increment
  - list
  - remove
  - update
  - version

* Include Python version in version information
* Drop support for arguments for ``-h, --help``, you can use the new
  help command for that.
* Always save full label specifications in labelfile
* Focus password field after selecting a label (GUI)
* Select label options after FocusOut  (GUI)
* Filter labels in combobox by given value (GUI)
* Use a vertical layout instead of a horizontal one (GUI)
* Make the gui *command* listen to the -f switch (GUI)
* Use a more flexible approach for algorithm handling
* The file /skel/labelfile is removed


v0.2.0 - released April 16th, 2013
##################################

.. warning::

    The default location of labelfile has changed from:

    * **\*nix**:   ``~/.dispass``
    * **Windows**: ``C:\Users\<username>\.dispass``

    To the following location:

    * **\*nix**:   ``~/.config/dispass/labels``
    * **Windows**: ``C:\Users\<username>\dispass\labels``


* Add support for multiple algorithms
* Add new algorithm Dispass2
* Add -a, --algo option for specifying algorithm
* Add -n, --number option for specifying sequence number
* Add label length selection in gui
* Add label/parameters selection in gui
* Add interactive labelfile editor 'dispass-label'
* Center the fields when the window gets bigger
* Reset all fields in gdispass by pressing <Escape>
* Optionally quit gdispass with Ctrl-Q
* Gracefully quit on (Ctrl-C) keyboard interrupt
* Clear input fields after passphrase generation
* Auto-select generated passphrase in gdispass
* Generate passphrases in gdispass by pressing <Return>
* Change default location of labelfile
* Add dispass `--script` option
* Add dispass-label for managing labelfiles
* Use separate text for manpage instead of README
* Add option to lookup a lable in with '-s' switch
* Require a minimum password length of 8 chars in CLI
* Rename ChangeLog -> ChangeLog.rst
* Make DisPass run from Python shell without exiting
* Remove dispass.el emacs wrapper, maintained separately by Tom Willemse


v0.1-alpha-8 - released June 21st, 2012
#######################################

* Add dispass.el emacs wrapper, authored by Tom Willemse (ryuslash)
* Allow generating a list of passphrases with varying lengths
* Add labelfile handler and skel/dot.dispass
* Add -f <labelfile>, --file=<labelfile> option
* Use labelfile at $HOME/.dispass if no labels are specified
* Add -l <length> --length= option
* Do not autostart gui on Windows
* Explicitly name the gui version 'gDisPass'
* Autofill 1st column on output via stdout
* Remove platform name from usage/help
* Add manpage
* Use a landing page for the html documentation


v0.1-alpha-7 - released May 28th, 2012
######################################

* Distribute as package instead of a single module
* Add LICENSE file
* Rename README to README.rst
* Add 'master' Makefile for building documentation


v0.1-alpha-6 - released May 24th, 2012
######################################

* Initial release of Dispass as single python module
