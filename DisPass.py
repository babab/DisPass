#!/usr/bin/env python
# vim: set et ts=4 sw=4 sts=4:

'''Generate and disperse/dispell passwords

Copyright (c) 2011 Benjamin Althues <benjamin@babab.nl>

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
'''

import sys
from Tkinter import *

class DisPass:
    '''This controls the main program and arguments'''

    versionStr = 'DisPass v0.1-alpha'

    def main(self):
        # No command line option parsing atm
        root = Tk()
        gui = GUI(root, self)
        gui.main(root)
        root.mainloop()

class GUI:
    def __init__(self, master, dp):
        self.dp = dp
        frame = Frame(master)
        frame.master.title(dp.versionStr)
        frame.pack()

    def main(self, master):
        # title
        w = Label(master, text=self.dp.versionStr, font=("Verdana", 14))
        w.pack()

if __name__ == '__main__':
    app = DisPass()
    app.main()
