#!/usr/bin/env python3
#
# Author: Soft9000.com
# 2020/04/13: Project Begun

# Mission: Create a graphical user interface from an SQL Database File.
# Status: WORK IN PROGRESS

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from collections import OrderedDict

from FormGUI.Project.Meta import Meta
from FormGUI.Project.ProjectFile import ProjectFile
from FormGUI.Gui.StandardEntry import LabelEntry
from FormGUI.Gui.GuiFields import GuiFields as GuiData
from FormGUI.SQLite.BasicTable import BasicTable


class Main(Tk):

    def __init__(self, *args, **kwargs):
        from FormGUI.Project.Meta import Meta
        super().__init__(*args, **kwargs)
        self.ztitle = Meta.Title()
        self.d2c = None
        self.project = None
        self.zoptions = (
            ("Projects",    [("New Project...", self._on_new),
                             ("Open Project...", self._on_open),
                             ("Save Project...", self._on_save),
                             ("Create GUI", self._on_create_gui)],),
            ("About",       [("About FormGUI...", self._on_about),
                             ("Quit", self.destroy)]),
            )
        self.scraper = None
        self.home = "."
        self.order_def = ProjectFile()

        '''
        activeBackground, foreground, selectColor,
        activeForeground, highlightBackground, selectBackground,
        background, highlightColor, selectForeground,
        disabledForeground, insertBackground, troughColor.
        '''
        self.tk_setPalette(
                background="Light Green",# e.g. Global
                foreground="dark blue",  # e.g. Font color
                insertBackground="blue", # e.g. Entry cursor
                selectBackground="gold", # e.g. Editbox selections
                activeBackground="gold", # e.g. Menu selections
                )

    def _on_new(self):
        self.title(self.ztitle)
        self.order_def = ProjectFile()
        self.scraper.empty()
        self.scraper.got_results()
        self.scraper.table_name.set(Meta.DEFAULT_TABLE)
        self._show_order()
    
    def _on_open(self):
        self.project = askopenfilename(
            title="Open Project File",
            filetypes=[("FormGUI. Project", Meta.ProjType)]
            )
        if not self.project:
            return
        zdef = ProjectFile.LoadFile(self.project)
        if not zdef:
            messagebox.showerror(
                "Schema File / Format Error",
                "Unable to import " + self.project)
        else:
            self.scraper.got_results()
            self.title(self.project)
            self.order_def = zdef
            self._show_order()

    def _funkey(self, funk):
        ''' Lots of re-use here - pull def, do funk, mark as ok iff same. '''
        ztbl = self.scraper.pull_results()
        self.order_def = ProjectFile(name=ztbl.get_table_name())
        if not self.order_def.add_table(ztbl):
            messagebox.showerror(
                "Invalid Table",
                "Please verify SQL Table Definition.")
            return False
        if funk() == False:
            return False
        self.scraper.got_results()
        return True

    def _funkey_save(self):
        ''' funk for saving the file - complain on error, only '''
        if ProjectFile.SaveFile(self.home, self.order_def, overwrite=True) is False:
            messagebox.showerror(
                "Exportation Error",
                "Please verify user locations.")
            return False
        return True

    def _funkey_gen(self):
        ''' TODO: funk for generating the FormGUI, final - complain on error, only '''
        messagebox.showinfo("Source Code TO-DO", Meta.ABOUT)
        return False

    def do_save(self):
        ''' 
        Quietly save the project to the table-benamed, file. 
        Complain only if error.'''
        return self._funkey(self._funkey_save)
    
    def _on_save(self):
        ''' GUI Event - Confirm Success Falure '''
        if self.do_save() is True:
            val = os.path.split(self.order_def.project_name)
            messagebox.showinfo(
                "Project Saved",
                "Project file saved.")

    def _on_create_gui(self):
        ''' GUI Event - Confirm Success Falure '''
        return self._funkey(self._funkey_gen)

    def _on_about(self):
        ''' GUI Event - Modal '''
        messagebox.showinfo(
            self.ztitle,
            Meta.ABOUT)

    def _show_order(self):
        ''' GUI Event - Confirm Success Falure '''
        if not self.order_def:
            return False
        self.scraper.empty()
        for key in self.order_def.project_tables:
            td1 = self.order_def.project_tables[key]
            if self.scraper.put_results(td1) is False:
                messagebox.showerror(
                    "Display Error",
                    "Critical: _show_order regression.")
                return False

    def _set_frame(self):
        zframe = Frame(self)
        self.scraper = GuiData(zframe)
        zframe.pack(fill=BOTH)

    def begin(self):
        self.title(self.ztitle)
        try:
            image = PhotoImage(file="zicon.png")
            self.wm_iconphoto(self, image)
        except:
            pass
        zmain = Menu(self)
        for zsub in self.zoptions:
            zdrop = Menu(zmain, tearoff=False)
            zmain.add_cascade(label=zsub[0], menu=zdrop)
            for zz in zsub[1]:
                zdrop.add_command(label=zz[0], command=zz[1])
        self.config(menu=zmain)
        self._set_frame()
        return True

    def run(self):
        self.mainloop()
        return True

    def end(self):
        return True


if __name__ == "__main__":
    main = Main()
    try:
        if main.begin():
            main.run()
    except Exception as ex:
        print(str(ex))
    finally:
        try:
            main.end()
        except:
            pass

