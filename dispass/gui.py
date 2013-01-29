# Copyright (c) 2011, 2012, 2013  Benjamin Althues <benjamin@babab.nl>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from Tkinter import *
import tkMessageBox
import ttk

import algos
from dispass import versionStr as dispass_version
from filehandler import Filehandler

versionStr = 'g%s' % dispass_version


class GUI(Frame):
    '''Houses all GUI related objects and interactions'''

    font = "Verdana"
    '''Default font (Verdana)'''

    fontsize = 10
    '''Default fontsize (10 pt.)'''

    def __init__(self, settings):
        '''Initialize GUI object, create the widgets and start mainloop

        Try to import Tkinter and tkMessageBox. If that fails, show a help
        message with quick instructions on installing Tkinter.
        '''

        self.settings = settings
        self.labelspecs = {l[0]: l[1:] for l in
                           Filehandler(self.settings).labelfile}

        Frame.__init__(self, Tk(className='dispass'))
        self.lengthVar = IntVar()
        self.lengthVar.set(self.settings.passphrase_length)
        self.master.title(versionStr)
        self.grid()
        self.createWidgets()

    def getFont(self, sizediff=0):
        '''Get `font` and `fontsize`, optionally differ from default `fontsize`

        :Parameters:
            - `sizediff`: The difference in pt. from the default `fontsize`

        :Return:
            - Tuple of `(font, fontsize)` to be used when creating widgets
        '''

        return (self.font, self.fontsize + sizediff)

    def warn(self, message, warning_type='soft', box_title=''):
        '''Prototype for warning user

         * soft warnings display a message in the passwordout field
         * hard warnings do the same and also display a messagebox

        :Parameters:
            - `message`: The message string for warning the user
            - `warning_type`: Either 'soft' (default value) or 'hard'
            - `box_title`: Optional title for tkMessageBox on hard warnings
        '''

        if warning_type == 'soft' or warning_type == 'hard':
            self.result.config(fg="black", readonlybackground="red")
            self.passwordout.set('- ' + message + ' -')

        if warning_type == 'hard':
            self.passwordin1.delete(0, END)
            self.passwordin2.delete(0, END)
            tkMessageBox.showwarning(box_title, message)

# GUI # Event actions
    def validateAndShow(self):
        '''Check user input

        Warn when user input is insufficient or wrong. Create digest and
        display the generated password if user input is OK.
        '''

        label = self.label.get()
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
        h = algos.Dispass1.digest(label, passwordin1,
                                  length=self.lengthVar.get())
        self.result.config(fg="black", readonlybackground="green")
        self.passwordout.set(h)
        self.clearInput()
        self.result.focus_set()
        self.result.select_range(0, END)

    def toggleCheck(self):
        '''Toggle checking of input password'''

        if self.isnew.get() == 0:
            # Disable double check (default)
            self.passwordin2.delete(0, END)
            self.passwordin2.config(state=DISABLED)
        else:
            # Password is new, allow for double checking passwordin
            self.passwordin2.config(state=NORMAL)

    def clearInput(self):
        '''Clear all input fields'''

        self.lengthVar.set(self.settings.passphrase_length)
        self.label.delete(0, END)
        self.passwordin1.delete(0, END)
        self.passwordin2.delete(0, END)

    def clearOutput(self):
        '''Clear all output fields'''
        self.passwordout.set('- No password generated -')
        self.result.config(fg="black", readonlybackground="gray")

    def clearIO(self):
        '''Clear all input and output fields'''

        self.clearInput()
        self.clearOutput()

    def reset(self):
        '''Clear all input and output and focus label entry'''

        self.clearIO()
        self.label.focus_set()

    def labelSelected(self, event):
        '''Set values of input fields according to the selected label.'''
        self.lengthVar.set(self.labelspecs[self.label.get()][0])

# GUI # Create Widgets
    def createWidgets(self):
        '''Create and align widgets'''

        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.passwordout = StringVar()
        self.passwordout.set('- No password generated -')
        self.isnew = IntVar()

        ttitle = Label(self, text=versionStr, font=self.getFont(4))
        wisnew = Checkbutton(self, height=2, font=self.getFont(),
                             text="This is a new password, that I have not "
                                  + "used before",
                             variable=self.isnew, command=self.toggleCheck)
        tlabel = Label(self, text='Label', font=self.getFont(2))
        tpasswordin1 = Label(self, text='Password', font=self.getFont(2))
        tpasswordin2 = Label(self, text='Password (again)',
                             font=self.getFont(2))
        tlength = Label(self, text='Length', font=self.getFont(2))
        self.label = ttk.Combobox(self, width=27, font=self.getFont(),
                                  values=self.labelspecs.keys())
        self.passwordin1 = Entry(self, width=27, font=self.getFont(), show="*")
        self.passwordin2 = Entry(self, width=27, font=self.getFont(), show="*",
                                 state=DISABLED)
        length = Spinbox(self, width=3, font=self.getFont, from_=9,
                         to=171, textvariable=self.lengthVar)
        genbutton = Button(self, text="Generate password",
                           font=self.getFont(), command=self.validateAndShow,
                           default="active")
        clrbutton = Button(self, text="Clear fields", font=self.getFont(),
                           command=self.clearIO)
        self.result = Entry(self, font=self.getFont(4),
                            textvariable=self.passwordout, state="readonly",
                            fg="black", readonlybackground="gray")

        # Keybindings
        self.passwordin1.bind('<Return>', lambda e: genbutton.invoke())
        self.passwordin2.bind('<Return>', lambda e: genbutton.invoke())
        length.bind('<Return>', lambda e: genbutton.invoke())
        self.master.bind('<Control-q>', lambda e: self.quit())
        self.master.bind('<Escape>', lambda e: self.reset())
        self.label.bind('<<ComboboxSelected>>', self.labelSelected)

        # Layout widgets in a grid
        ttitle.grid(row=0, column=0, sticky=N + S + E + W, columnspan=4)
        wisnew.grid(row=1, column=0, sticky=N + S + E + W, columnspan=4)
        tlabel.grid(row=2, column=0, sticky=N + S + E + W)
        tpasswordin1.grid(row=2, column=1, sticky=N + S + E + W)
        tpasswordin2.grid(row=2, column=2, sticky=N + S + E + W)
        tlength.grid(row=2, column=3, sticky=N + S + E + W)
        self.label.grid(row=3, column=0, sticky=N + S + E + W)
        self.passwordin1.grid(row=3, column=1, sticky=N + S + E + W)
        self.passwordin2.grid(row=3, column=2, sticky=N + S + E + W)
        length.grid(row=3, column=3, sticky=N + S + E + W)
        genbutton.grid(row=4, column=0, sticky=N + S + E + W, columnspan=2)
        clrbutton.grid(row=4, column=2, sticky=N + S + E + W, columnspan=2)
        self.result.grid(row=5, column=0, sticky=N + S + E + W, columnspan=4)

        # Initially, set focus on self.label
        self.label.focus_set()
