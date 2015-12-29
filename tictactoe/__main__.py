#!/usr/bin/env python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


MENU_DESCRIPTION = """
<ui>
    <menubar name='MenuBar'>
        <menu action='FileMenu'>
            <menuitem action='FileQuit' />
        </menu>
    </menubar>
</ui>
"""


class TicTacToeWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="Tic-tac-toe")
        self.set_default_size(800, 600)

        action_group = Gtk.ActionGroup("my_actions")
        self.add_file_menu_actions(action_group)

        uimanager = Gtk.UIManager()
        uimanager.add_ui_from_string(MENU_DESCRIPTION)
        self.add_accel_group(uimanager.get_accel_group())
        uimanager.insert_action_group(action_group)

        menubar = uimanager.get_widget("/MenuBar")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(menubar, False, False, 0)

        self.add(box)

    def add_file_menu_actions(self, action_group):
        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        action_group.add_action(action_filemenu)

        action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        action_filequit.connect("activate", self.on_menu_file_quit)
        action_group.add_action(action_filequit)

    def on_menu_file_quit(self, widget):
        Gtk.main_quit()


win = TicTacToeWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
