#!/usr/bin/env python3

from enum import Enum
import math

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

CELL_WIDTH = 100


class Cell(Enum):
    EMPTY = " "
    X = "X"
    O = "O"


class Player(Enum):
    X = "X"
    O = "O"


class GameState(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_player = Player.X
        self.grid = [[Cell.EMPTY for _ in range(width)] for _ in range(height)]


class TicTacToeWindow(Gtk.Window):

    def __init__(self, game_state):
        super().__init__(title="Tic-tac-toe")
        self.set_default_size(CELL_WIDTH * game_state.width + 20,
                              CELL_WIDTH * game_state.height + 40)

        self.game_state = game_state

        action_group = Gtk.ActionGroup("my_actions")
        self.add_file_menu_actions(action_group)

        uimanager = Gtk.UIManager()
        uimanager.add_ui_from_string(MENU_DESCRIPTION)
        self.add_accel_group(uimanager.get_accel_group())
        uimanager.insert_action_group(action_group)

        menubar = uimanager.get_widget("/MenuBar")
        drawing_area = self.get_drawing_area()

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(menubar, False, False, 0)
        box.pack_start(drawing_area, True, True, 0)

        self.add(box)

    def add_file_menu_actions(self, action_group):
        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        action_group.add_action(action_filemenu)

        action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        action_filequit.connect("activate", self.on_menu_file_quit)
        action_group.add_action(action_filequit)

    def get_drawing_area(self):
        drawing_area = Gtk.DrawingArea()
        drawing_area.connect("draw", self.on_drawing_area_draw)
        return drawing_area

    def on_drawing_area_draw(self, widget, cx):
        cx.set_line_width(5)
        cx.set_source_rgb(0, 0, 0)
        for y in range(self.game_state.height):
            for x in range(self.game_state.width):
                cell = self.game_state.grid[y][x]
                rx = 5 + CELL_WIDTH * x
                ry = 5 + CELL_WIDTH * y
                cx.rectangle(rx, ry, CELL_WIDTH, CELL_WIDTH)
                if cell == Cell.O:
                    cx.move_to(rx + CELL_WIDTH - 10, ry + CELL_WIDTH / 2)
                    cx.arc(rx + 50, ry + 50, 40, 0, math.pi * 2)
                elif cell == Cell.X:
                    cx.move_to(rx + 20, ry + 20)
                    cx.rel_line_to(60, 60)
                    cx.move_to(rx + 80, ry + 20)
                    cx.rel_line_to(-60, 60)
        cx.stroke()

    def on_menu_file_quit(self, widget):
        Gtk.main_quit()


game_state = GameState(3, 3)

win = TicTacToeWindow(game_state)
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
