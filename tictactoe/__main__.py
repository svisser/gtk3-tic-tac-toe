#!/usr/bin/env python3

import gi
gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from tictactoe.game import GameState
from tictactoe.gui import TicTacToeWindow


win = TicTacToeWindow(GameState.get_initial_state())
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
