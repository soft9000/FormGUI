#!/usr/bin/python3
from tkinter import *

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from FormGUI.SQLite.BasicFields import BasicFields
from FormGUI.SQLite.BasicTable import BasicTable
from FormGUI.Project.ProjectFile import ProjectFile
from FormGUI.Project.Meta import Meta


# Mission: Create a way to CRUD a BasicTable.
class BasicForm:
    def __init__(self):
        self._dict = None
        self._isOk = None
        self.last_row = None

    def _okay(self):
        self._isOk = True
        self.tk.quit()

    def _cancel(self):
        self._isOk = False
        self.tk.quit()

    @staticmethod
    def Begin(basic_table, title="Input"):
        if not isinstance(basic_table, BasicTable):
             return False
        ''' Create the frame, add the title, as well as the input fields.'''
        from collections import OrderedDict
        self = BasicForm()
        self.tk = Tk()

        self._dict = OrderedDict()

        if title:
            self.tk.title(title)

        self.last_row = 0
        # zFields (A Label, plus an Entry, in a grid layout)
        for ref in basic_table.fields:
            obj = Label(master=self.tk, text=str(ref))
            obj.grid(row=self.last_row, column=0)

            obj = Entry(master=self.tk, bd=5)
            obj.grid(row=self.last_row, column=1)

            self._dict[ref]=obj
            self.last_row += 1
        return self

    @staticmethod
    def End(basic_form):
        ''' Add the closing buttons, center, and pack the Frame.'''
        if basic_form.last_row is None:
            return False
        if isinstance(basic_form, BasicForm) is False:
            return False
        # zButtons (A Frame in the grid, plus the properly-centered pair of buttons)
        bottom = Frame(basic_form.tk)
        bottom.grid(row=basic_form.last_row, columnspan=2)
        btn = Button(bottom, text="Okay", command=basic_form._okay)
        btn.pack(side=LEFT, pady=12)

        btn = Button(bottom, text="Cancel", command=basic_form._cancel)
        btn.pack(side=RIGHT, padx=10)

        # zCenter (Close enough to make no odds?)
        width = basic_form.tk.winfo_screenwidth()
        height = basic_form.tk.winfo_screenheight()
        x = (width - basic_form.tk.winfo_reqwidth()) / 2
        y = (height - basic_form.tk.winfo_reqheight()) / 2
        basic_form.tk.geometry("+%d+%d" % (x, y))
        return True

    def show(self):
        from collections import OrderedDict
        self.tk.mainloop()
        try:
            results = OrderedDict()
            if self._isOk is not True:
                return results

            for ref in self._dict.keys():
                results[ref] = (self._dict[ref]).get()
            return results
        finally:
            try:
                self.tk.destroy()
            except:
                pass


    @staticmethod
    def EntryCreate(basic_table, title="Input"):
        if not isinstance(basic_table, BasicTable):
            return False
        ''' Basic mission statement completed. '''
        self = BasicForm.Begin(basic_table, title=title)
        if BasicForm.End(self) is False:
            raise Exception("AddButtons: Unexpected Error.")
        return self.show()


if __name__ == "__main__":
    # Here is how we would use the BasicForm from a Console Program:
    table = BasicTable()
    table.add_field("Email", "TEXT")
    table.add_field("Name", "TEXT")
    table.add_field("Age", "INTEGER")
    table.add_field("Balance", "REAL")
    project_file = ProjectFile("MyTestData")
    project_file.add_table(table)
    results = BasicForm.EntryCreate(table, title=project_file.project_name)
    if len(results) is 0:
        print("Pressed Cancel - no values!")
    else:
        print("Pressed Okay - got values!")
        for ref in results:
            print(ref, results[ref])
