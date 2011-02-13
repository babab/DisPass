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
        gui = GUI(root, self)
        gui.draw(root)
        root.mainloop()

class digest:
    '''Control message digest'''
    def hash(self, message):
        '''Construct and return secure hash from message'''
        d = hashlib.sha512()
        d.update(message)
        shastr = d.hexdigest()
        r = base64.b64encode(shastr, '49') # replace +/ with 49
        r = r.replace('=','') # filter '='
        return str(r)

class GUI:
    label = None
    salt = None
    passwordin = None
    passwordout = None
    chartypes = None
    nchars = None

    def __init__(self, master, dp):
        '''Draw main window'''
        self.dp = dp
        frame = Frame(master)
        frame.master.title(dp.versionStr)
        frame.grid()

    def gen(self):
        '''Handle and draw digest or message if input is insufficient'''

        label = self.label.get()
        salt = self.label.get()
        passwordin = self.passwordin.get()
        mchartypes = map(int, self.chartypes.curselection())
        chartypes = mchartypes[0]
        mnchars = map(int, self.nchars.curselection())
        nchars = mnchars[0]

        if len(label) == 0:
            r = '- No password generated, label field is empty -'
        elif len(passwordin) == 0:
            r = '- No password generated, password field is empty -'
        else:
            s = self.label.get() + self.salt.get() + self.passwordin.get()
            o = digest()
            h = o.hash(s)

            # optionally strip chars according to chartypes
            if chartypes == 0:
                r = h
            elif chartypes == 1:
                r = re.sub("[0-9]", "", h)
            elif chartypes == 2:
                r = re.sub("[A-Z]", "", h)
            elif chartypes == 3:
                r = re.sub("[a-z]", "", h)

            # Set length of string returned
            r = r[0:nchars+8]

        self.passwordout.set(r)

        if len(salt) == 0:
            print 'salt is empty'

    def draw(self, master):
        '''Draw and align widgets'''

        f = "Verdana" # font
        self.passwordout = StringVar()
        self.passwordout.set('- No password generated yet -')

        # List allowed characters
        allowedchars = [
                'a-z, A-Z, 0-9',
                'a-z, A-Z',
                'a-z, 0-9',
                'A-Z, 0-9'
                ]

        # Create widgets
        ttitle = Label(master, text=self.dp.versionStr, font=(f, 14))

        tchartypes = Label(master, text='Char types', font=(f, 12))
        self.chartypes = Listbox(master, height=4, exportselection=0)
        for item in allowedchars:
            self.chartypes.insert(END, item)
        self.chartypes.select_set(0) # default is 'a-z, A-Z, 0-9, special'

        tnchars = Label(master, text='# Chars', font=(f, 12))
        nCharsFrame = Frame(master)
        scrollbar = Scrollbar(nCharsFrame, orient=VERTICAL)
        self.nchars = Listbox(nCharsFrame, width=5, height=3, 
                exportselection=0, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.nchars.yview)
        for n in range(8, 31):
            self.nchars.insert(END, n)
        self.nchars.select_set(7) # default is 15 chars
        self.nchars.see(6)
        # Pack self.nchars and scrollbar together in a frame, apply grid later
        scrollbar.pack(side=RIGHT, fill=Y)
        self.nchars.pack()

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
        tchartypes.grid(row=6, column=1, sticky=N)
        self.chartypes.grid(row=7, column=1, sticky=NW)
        tnchars.grid(row=9, column=1, sticky=N)
        nCharsFrame.grid(row=10, column=1)
        tlabel.grid(row=14, column=0, sticky=N)
        tsalt.grid(row=14, column=1, sticky=N)
        tpasswordin.grid(row=14, column=2, sticky=N)
        self.label.grid(row=15, column=0, sticky=NW)
        self.salt.grid(row=15, column=1, sticky=NW)
        self.passwordin.grid(row=15, column=2, sticky=NW)
        button.grid(row=17, column=0, sticky=NW, columnspan=3)
        wresult.grid(row=19, column=0, sticky=N, columnspan=3)

if __name__ == '__main__':
    app = DisPass()
    app.main()
