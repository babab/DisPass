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
    label = None
    salt = None
    passwordin = None
    passwordout = None

    def __init__(self, master, dp):
        '''Initialize frame'''
        self.dp = dp
        frame = Frame(master)
        frame.master.title(dp.versionStr)
        frame.grid()

    def gen(self):
        '''Generate password (temporily placed in GUI class)'''

        label = self.label.get()
        salt = self.label.get()
        passwordin = self.passwordin.get()

        if len(label) == 0:
            r = '- Label field is empty -'
        elif len(passwordin) == 0:
            r = '- Password field is empty -'
        else:
            r = self.label.get() + '+' + self.salt.get() + '+' \
                    + self.passwordin.get()
        self.passwordout.set(r)

        if len(salt) == 0:
            print 'salt is empty'

    def main(self, master):
        '''Set and align widgets'''

        f = "Verdana" # font
        self.passwordout = StringVar()
        self.passwordout.set('- No password generated yet -')

        t = Label(master, text=self.dp.versionStr, font=(f, 14))
        t1 = Label(master, text='Label', font=(f, 12))
        t2 = Label(master, text='Salt', font=(f, 12))
        t3 = Label(master, text='Password', font=(f, 12))
        self.label = Entry(master, width=20)
        self.salt = Entry(master, width=20)
        self.passwordin = Entry(master, width=20, show="*")
        button = Button(master, text="Generate password", width=60, 
                command=self.gen)
        resultw = Entry(master, width=63, textvariable=self.passwordout)

        t.grid(row=0, sticky=N, columnspan=3)
        t1.grid(row=1, column=0, sticky=NW)
        t2.grid(row=1, column=1, sticky=NW)
        t3.grid(row=1, column=2, sticky=NW)
        self.label.grid(row=2, column=0, sticky=NW)
        self.salt.grid(row=2, column=1, sticky=NW)
        self.passwordin.grid(row=2, column=2, sticky=NW)
        button.grid(row=3, column=0, sticky=NW, columnspan=3)
        resultw.grid(row=4, column=0, sticky=N, columnspan=3)

if __name__ == '__main__':
    app = DisPass()
    app.main()
