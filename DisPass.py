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
import tkMessageBox

class DisPass:
    '''This controls the main program and arguments'''

    versionStr = 'DisPass v0.1-alpha'

    def main(self):
        '''Create apporopiate object depending on command arguments'''
        # No command line option parsing atm
        self.root = Tk()
        self.root.title(self.versionStr)
        gui = GUI(self.root, self)
        self.root.mainloop()

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
        '''Allow access to DisPass object, create widgets'''
        self.dp = dp
        self.createWidgets(master)

# GUI # Setters and getters
    def setFont(self):
        '''Set font and fontsize'''
        pass

    def getFont(self, sizediff=0):
        '''Get font and fontsize, option to differ from default fontsize'''
        self.font = "Verdana"
        self.fontsize = 10
        return (self.font, self.fontsize + sizediff)

# GUI # Prototypes
    def warn(self, message, warning_type='soft', box_title=''):
        '''Prototype for warning user'''

        if warning_type == 'soft' or warning_type == 'hard':
            self.result.config(fg="black", readonlybackground="red")
            self.passwordout.set('- ' + message + ' -')

        if warning_type == 'hard':
            self.passwordin1.delete(0, END)
            self.passwordin2.delete(0, END)
            tkMessageBox.showwarning(box_title, message)

# GUI # Event actions
    def OnGen(self):
        '''Handle and draw digest or message if input is insufficient'''

        label = self.label.get()
        salt = self.label.get()
        passwordin1 = self.passwordin1.get()
        passwordin2 = self.passwordin2.get()
        isnew = self.isnew.get()

        if len(label) == 0:
            self.warn('No password generated, label field is empty')
            return
        elif len(passwordin1) == 0:
            self.warn('No password generated, password field is empty')
            return
        elif len(passwordin1) < 8:
            self.warn('Password must contain at least 8 characters', 'hard',
                    box_title='Password is too short')
            return
        elif isnew and passwordin1 != passwordin2:
            self.warn('Passwords are not identical, please try again', 'hard',
                    box_title='Password mismatch')
            return

        # All checks passed, create digest
        digest = Digest()
        s = label + salt + passwordin1
        h = digest.create(s)
        r = h[:30]
        self.result.config(fg="black", readonlybackground="green")
        self.passwordout.set(r)

    def OnNew(self):
        '''Toggle double checking of input password'''
        if self.isnew.get() == 0:
            # Disable double check (default)
            self.passwordin2.delete(0, END)
            self.passwordin2.config(state=DISABLED)
        else:
            # Password is new, allow for double checking passwordin
            self.passwordin2.config(state=NORMAL)

    def OnClear(self):
        '''Clear all fields'''
        self.label.delete(0, END)
        self.salt.delete(0, END)
        self.passwordin1.delete(0, END)
        self.passwordin2.delete(0, END)
        self.passwordout.set('- No password generated -')
        self.result.config(fg="black", readonlybackground="gray")

# GUI # Create Widgets
    def createWidgets(self, master):
        '''Create and align widgets'''

        self.passwordout = StringVar()
        self.passwordout.set('- No password generated -')
        self.isnew = IntVar()

        ttitle = Label(master, text=self.dp.versionStr, font=self.getFont(4))
        wisnew = Checkbutton(master, height=2, font=self.getFont(),
                text="This is a new password, that I have not used before", 
                variable=self.isnew, command=self.OnNew)
        tlabel = Label(master, text='Label', font=self.getFont(2))
        tsalt = Label(master, text='Salt', font=self.getFont(2))
        tpasswordin1 = Label(master, text='Password', font=self.getFont(2))
        tpasswordin2 = Label(master, text='Password (again)', 
                font=self.getFont(2))
        self.label = Entry(master, width=20, font=self.getFont())
        self.salt = Entry(master, width=20, font=self.getFont())
        self.passwordin1 = Entry(master, width=20, font=self.getFont(), 
                show="*")
        self.passwordin2 = Entry(master, width=20, font=self.getFont(), 
                show="*", state=DISABLED)
        genbutton = Button(master, text="Generate password", 
                font=self.getFont(), command=self.OnGen)
        clrbutton = Button(master, text="Clear fields", font=self.getFont(), 
                command=self.OnClear)
        self.result = Entry(master, font=self.getFont(4),
                textvariable=self.passwordout, state="readonly", fg="black", 
                readonlybackground="gray")

        # Layout widgets in a grid
        ttitle.grid(row=0, column=0, sticky=N+S+E+W, columnspan=4)
        wisnew.grid(row=1, column=0, sticky=N+S+E+W, columnspan=4)
        tlabel.grid(row=14, column=0, sticky=N+S+E+W)
        tsalt.grid(row=14, column=1, sticky=N+S+E+W)
        tpasswordin1.grid(row=14, column=2, sticky=N+S+E+W)
        tpasswordin2.grid(row=14, column=3, sticky=N+S+E+W)
        self.label.grid(row=15, column=0, sticky=N+S+E+W)
        self.salt.grid(row=15, column=1, sticky=N+S+E+W)
        self.passwordin1.grid(row=15, column=2, sticky=N+S+E+W)
        self.passwordin2.grid(row=15, column=3, sticky=N+S+E+W)
        genbutton.grid(row=17, column=0, sticky=N+S+E+W, columnspan=3)
        clrbutton.grid(row=17, column=3, sticky=N+S+E+W, rowspan=2)
        self.result.grid(row=18, column=0, sticky=N+S+E+W, columnspan=3)

        # Initially, set focus on self.label
        self.label.focus_set()

if __name__ == '__main__':
    app = DisPass()
    app.main()
