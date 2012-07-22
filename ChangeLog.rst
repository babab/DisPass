ChangeLog
==============================================================================

**Development version** currently in Github / Bitbucket

 * Change default location of labelfile
 * Add dispass `--script` option
 * Add dispass-label for managing labelfiles
 * Use separate text for manpage instead of README
 * Add option to lookup a lable in with '-s' switch
 * Require a min. password length of 8 chars in cli
 * Rename ChangeLog -> ChangeLog.rst
 * Make DisPass run from Python shell without exiting
 * Remove dispass.el emacs wrapper, maintained separately by Tom Willemsen

**v0.1-alpha-8**  released June 21st, 2012

 * Add dispass.el emacs wrapper, authored by Tom Willemsen (ryuslash)
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


**v0.1-alpha-7**  released May 28th, 2012

 * Distribute as package instead of a single module
 * Add LICENSE file
 * Rename README to README.rst
 * Add 'master' Makefile for building documentation


**v0.1-alpha-6**  released May 24th, 2012

 * Initial release of Dispass as single python module

