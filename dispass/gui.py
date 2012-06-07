try:
    from Tkinter import *
    import tkMessageBox
    hasTk = True
except ImportError:
    hasTk = False

import dispass

class GUI:
    '''Houses all GUI related objects and interactions'''

    font = "Verdana"
    '''Default font (Verdana)'''

    fontsize = 10
    '''Default fontsize (10 pt.)'''

    def __init__(self):
        '''Initialize GUI object, create the widgets and start mainloop

        Try to import Tkinter and tkMessageBox. If that fails, show a help
        message with quick instructions on installing Tkinter.
        '''

        if not hasTk:
            print 'Could not find Tkinter, this is a package needed '\
                    'for using\nthe graphical version of dispass.'
            print 'To install, search for a python-tk package for your OS.\n'
            print 'Debian / Ubuntu\t\t$ sudo apt-get install python-tk'
            print 'OpenBSD        \t\t# pkg_add -i python-tk'
            return

        self.root = Tk()
        self.root.title(dispass.versionStr)
        self.createWidgets(self.root)
        self.root.mainloop()

# GUI # Setters and getters
    def setFont(self):
        '''Set font and fontsize'''
        pass

    def getFont(self, sizediff=0):
        '''Get `font` and `fontsize`, optionally differ from default `fontsize`

        :Parameters:
            - `sizediff`: The difference in pt. from the default `fontsize`

        :Return:
            - Tuple of (`font`, `fontsize`) to be used when creating widgets
        '''
        return (self.font, self.fontsize + sizediff)

# GUI # Prototypes
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
    def OnGen(self):
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
        h = dispass.digest(label + passwordin1)
        self.result.config(fg="black", readonlybackground="green")
        self.passwordout.set(h)

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
        '''Clear all input fields'''
        self.label.delete(0, END)
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

        ttitle = Label(master, text=dispass.versionStr, font=self.getFont(4))
        wisnew = Checkbutton(master, height=2, font=self.getFont(),
                text="This is a new password, that I have not used before",
                variable=self.isnew, command=self.OnNew)
        tlabel = Label(master, text='Label', font=self.getFont(2))
        tpasswordin1 = Label(master, text='Password', font=self.getFont(2))
        tpasswordin2 = Label(master, text='Password (again)',
                font=self.getFont(2))
        self.label = Entry(master, width=27, font=self.getFont())
        self.passwordin1 = Entry(master, width=27, font=self.getFont(),
                show="*")
        self.passwordin2 = Entry(master, width=27, font=self.getFont(),
                show="*", state=DISABLED)
        genbutton = Button(master, text="Generate password",
                font=self.getFont(), command=self.OnGen)
        clrbutton = Button(master, text="Clear fields", font=self.getFont(),
                command=self.OnClear)
        self.result = Entry(master, font=self.getFont(4),
                textvariable=self.passwordout, state="readonly", fg="black",
                readonlybackground="gray")

        # Layout widgets in a grid
        ttitle.grid(row=0, column=0, sticky=N+S+E+W, columnspan=3)
        wisnew.grid(row=1, column=0, sticky=N+S+E+W, columnspan=3)
        tlabel.grid(row=2, column=0, sticky=N+S+E+W)
        tpasswordin1.grid(row=2, column=1, sticky=N+S+E+W)
        tpasswordin2.grid(row=2, column=2, sticky=N+S+E+W)
        self.label.grid(row=3, column=0, sticky=N+S+E+W)
        self.passwordin1.grid(row=3, column=1, sticky=N+S+E+W)
        self.passwordin2.grid(row=3, column=2, sticky=N+S+E+W)
        genbutton.grid(row=4, column=0, sticky=N+S+E+W, columnspan=2)
        clrbutton.grid(row=4, column=2, sticky=N+S+E+W)
        self.result.grid(row=5, column=0, sticky=N+S+E+W, columnspan=3)

        # Initially, set focus on self.label
        self.label.focus_set()
