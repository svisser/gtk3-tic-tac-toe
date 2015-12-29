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

CELL_SIZE = 100
GRID_OFFSET_X = 5
GRID_OFFSET_Y = 5


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
        self.set_default_size(CELL_SIZE * game_state.width + 20,
                              CELL_SIZE * game_state.height + 40)

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
                rx = GRID_OFFSET_X + CELL_SIZE * x
                ry = GRID_OFFSET_Y + CELL_SIZE * y
                cx.rectangle(rx, ry, CELL_SIZE, CELL_SIZE)
                if cell == Cell.O:
                    cx.move_to(rx + CELL_SIZE - CELL_SIZE * 0.1, ry + CELL_SIZE / 2)
                    cx.arc(rx + CELL_SIZE / 2, ry + CELL_SIZE / 2, CELL_SIZE * 0.4, 0, math.pi * 2)
                elif cell == Cell.X:
                    cx.move_to(rx + CELL_SIZE * 0.2, ry + CELL_SIZE * 0.2)
                    cx.rel_line_to(CELL_SIZE * 0.6, CELL_SIZE * 0.6)
                    cx.move_to(rx + CELL_SIZE * 0.8, ry + CELL_SIZE * 0.2)
                    cx.rel_line_to(-1 * CELL_SIZE * 0.6, CELL_SIZE * 0.6)
        cx.stroke()

    def on_menu_file_quit(self, widget):
        Gtk.main_quit()


game_state = GameState(3, 3)

win = TicTacToeWindow(game_state)
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
