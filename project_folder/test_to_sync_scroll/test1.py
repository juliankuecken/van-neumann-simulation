from tkinter import *


class Widget:
    def __init__(self):
        self.window = Tk()

        self.linenumbers = Text(self, width=3)
        self.linenumbers.grid(row=1, column=1, sticky=NS)
        # self.linenumbers.config(font=self.__myfont)

        self.linenumbers.tag_configure('line', justify='right')
        self.linenumbers.config(state=DISABLED)

        def scrollBoth(self, action, position, type=None):
            self.textarea.yview_moveto(position)
            self.linenumbers.yview_moveto(position)

        def updateScroll(self, first, last, type=None):
            self.textarea.yview_moveto(first)
            self.linenumbers.yview_moveto(first)
            self.uniscrollbar.set(first, last)

        self.uniscrollbar= Scrollbar(self)
        self.uniscrollbar.grid(row=1, column=3, sticky=NS)
        self.uniscrollbar.config(command=self.scrollBoth)
        self.textarea.config(yscrollcommand=self.updateScroll)
        self.linenumbers.config(yscrollcommand=self.updateScroll)

g=Widget()