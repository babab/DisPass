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
            r = '- No password generated, label field is empty -'
        elif len(passwordin) == 0:
            r = '- No password generated, password field is empty -'
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

        # List allowed characters
        allowedchars = [
                'a-z, A-Z, 0-9, special',
                'a-z, A-Z, 0-9',
                'a-z, A-Z',
                'a-z, 0-9',
                'A-Z, 0-9'
                ]

        # Create widgets
        ttitle = Label(master, text=self.dp.versionStr, font=(f, 14))

        tchartypes = Label(master, text='Char types', font=(f, 12))
        wchartypes = Listbox(master, height=5, exportselection=0)
        for item in allowedchars:
            wchartypes.insert(END, item)
        wchartypes.select_set(0) # default is 'a-z, A-Z, 0-9, special'

        tnchars = Label(master, text='# Chars', font=(f, 12))
        nCharsFrame = Frame(master)
        scrollbar = Scrollbar(nCharsFrame, orient=VERTICAL)
        wnchars = Listbox(nCharsFrame, width=5, height=3, 
                exportselection=0, yscrollcommand=scrollbar.set)
        scrollbar.config(command=wnchars.yview)
        for n in range(8, 50):
            wnchars.insert(END, n)
        wnchars.select_set(7) # default is 15 chars
        wnchars.see(7)
        # Pack wnchars and scrollbar together in a frame, apply grid later
        scrollbar.pack(side=RIGHT, fill=Y)
        wnchars.pack()

        tlabel = Label(master, text='Label', font=(f, 12))
        tsalt = Label(master, text='Salt', font=(f, 12))
        tpasswordin = Label(master, text='Password', font=(f, 12))
        self.label = Entry(master, width=20)
        self.salt = Entry(master, width=20)
        self.passwordin = Entry(master, width=20, show="*")
        button = Button(master, text="Generate password", width=60, 
                command=self.gen)
        resultw = Entry(master, width=63, textvariable=self.passwordout)

        # Layout widgets in a grid
        ttitle.grid(row=0, column=0, sticky=N, columnspan=3)
        tchartypes.grid(row=6, column=1, sticky=N)
        wchartypes.grid(row=7, column=1, sticky=NW)
        tnchars.grid(row=9, column=1, sticky=N)
        nCharsFrame.grid(row=10, column=1)
        tlabel.grid(row=14, column=0, sticky=N)
        tsalt.grid(row=14, column=1, sticky=N)
        tpasswordin.grid(row=14, column=2, sticky=N)
        self.label.grid(row=15, column=0, sticky=NW)
        self.salt.grid(row=15, column=1, sticky=NW)
        self.passwordin.grid(row=15, column=2, sticky=NW)
        button.grid(row=17, column=0, sticky=NW, columnspan=3)
        resultw.grid(row=19, column=0, sticky=N, columnspan=3)

if __name__ == '__main__':
    app = DisPass()
    app.main()
