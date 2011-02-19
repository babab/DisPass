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

import base64
import hashlib
import re
from Tkinter import *

class DisPass:
    '''This controls the main program and arguments'''

    versionStr = 'DisPass v0.1-alpha'

    def main(self):
        '''Create apporopiate object depending on command arguments'''
        # No command line option parsing atm
        root = Tk()
        root.title(self.versionStr)
        gui = GUI(root, self)
        root.mainloop()

class Digest:
    '''Control message digest'''
    def create(self, message):
        '''Create and return secure hash of message'''
        d = hashlib.sha512()
        d.update(message)
        shastr = d.hexdigest()
        r = base64.b64encode(shastr, '49') # replace +/ with 49
        r = r.replace('=','') # filter '='
        return str(r)

class GUI:
    '''Here the interaction of Tkinters widgets is done'''
    def __init__(self, master, dp):
        '''Draw main window'''
        self.dp = dp
        self.createWidgets(master)

    def gen(self):
        '''Handle and draw digest or message if input is insufficient'''

        label = self.label.get()
        salt = self.label.get()
        passwordin = self.passwordin.get()

        if len(label) == 0:
            r = '- No password generated, label field is empty -'
        elif len(passwordin) == 0:
            r = '- No password generated, password field is empty -'
        else:
            s = self.label.get() + self.salt.get() + self.passwordin.get()
            digest = Digest()
            h = digest.create(s)

            # Set length of string returned
            r = h[:30]

        self.passwordout.set(r)

    def createWidgets(self, master):
        '''Create and align widgets'''

        f = "Verdana" # font
        self.passwordout = StringVar()
        self.passwordout.set('- No password generated yet -')

        # Create widgets
        ttitle = Label(master, text=self.dp.versionStr, font=(f, 14))
        tlabel = Label(master, text='Label', font=(f, 12))
        tsalt = Label(master, text='Salt', font=(f, 12))
        tpasswordin = Label(master, text='Password', font=(f, 12))
        self.label = Entry(master, width=20)
        self.salt = Entry(master, width=20)
        self.passwordin = Entry(master, width=20, show="*")
        button = Button(master, text="Generate password", width=60, 
                command=self.gen)
        wresult = Entry(master, width=63, textvariable=self.passwordout)

        # Layout widgets in a grid
        ttitle.grid(row=0, column=0, sticky=N, columnspan=3)
        tlabel.grid(row=14, column=0, sticky=N)
        tsalt.grid(row=14, column=1, sticky=N)
        tpasswordin.grid(row=14, column=2, sticky=N)
        self.label.grid(row=15, column=0, sticky=NW)
        self.salt.grid(row=15, column=1, sticky=NW)
        self.passwordin.grid(row=15, column=2, sticky=NW)
        button.grid(row=17, column=0, sticky=N, columnspan=3)
        wresult.grid(row=19, column=0, sticky=N, columnspan=3)

if __name__ == '__main__':
    app = DisPass()
    app.main()
