#!/usr/bin/env python3

import enum
import math

import gi
gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk


MENU_DESCRIPTION = """
<ui>
    <menubar name='MenuBar'>
        <menu action='FileMenu'>
            <menuitem action='FileNew' />
            <menuitem action='FileQuit' />
        </menu>
    </menubar>
</ui>
"""

CELL_SIZE = 100
DEFAULT_WIDTH = 3
DEFAULT_HEIGHT = 3
GRID_OFFSET_X = 10
GRID_OFFSET_Y = 10


class Cell(enum.Enum):
    EMPTY = " "
    X = "X"
    O = "O"


class Player(enum.Enum):
    X = "X"
    O = "O"

    def get_cell(self):
        return {
            Player.X: Cell.X,
            Player.O: Cell.O,
        }[self]

    def get_opposite_player(self):
        return {
            Player.X: Player.O,
            Player.O: Player.X,
        }[self]

    def __str__(self):
        return str(self.value)


class GameStatus(enum.Enum):
    ACTIVE = 0
    GAME_OVER = 1


class GameState(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_player = Player.X
        self.status = GameStatus.ACTIVE
        self.winning_player = None
        self.winning_cells = None
        self.symbols_placed = 0
        self.grid = [[Cell.EMPTY for _ in range(width)] for _ in range(height)]

    @classmethod
    def get_initial_state(cls):
        return cls(DEFAULT_WIDTH, DEFAULT_HEIGHT)

    def place_symbol(self, gx, gy):
        self.symbols_placed += 1
        self.grid[gy][gx] = self.current_player.get_cell()

        winner, cells = self.calculate_winner()
        if winner is not None:
            self.status = GameStatus.GAME_OVER
            self.winning_player = winner
            self.winning_cells = cells
            return

        if self.symbols_placed == self.width * self.height:
            self.status = GameStatus.GAME_OVER
            return

        self.current_player = self.current_player.get_opposite_player()

    def calculate_possibilities(self):
        for x in range(self.width):
            yield frozenset((x, y) for y in range(self.height))
        for y in range(self.height):
            yield frozenset((x, y) for x in range(self.width))
        yield frozenset((k, k) for k in range(self.width))
        yield frozenset((k, self.width - 1 - k) for k in range(self.width))

    def calculate_winner(self):
        for player in Player:
            symbol = player.get_cell()
            for cells in self.calculate_possibilities():
                if all(self.grid[cy][cx] == symbol for cx, cy in cells):
                    return player, cells
        return None, None


class TicTacToeWindow(Gtk.Window):

    def __init__(self, game_state):
        super().__init__(title="Tic Tac Toe")
        self.set_default_size(CELL_SIZE * game_state.width + GRID_OFFSET_X * 2,
                              CELL_SIZE * game_state.height + GRID_OFFSET_Y * 2 + 60)

        self.game_state = game_state

        action_group = Gtk.ActionGroup("my_actions")
        self.add_file_menu_actions(action_group)

        uimanager = Gtk.UIManager()
        uimanager.add_ui_from_string(MENU_DESCRIPTION)
        self.add_accel_group(uimanager.get_accel_group())
        uimanager.insert_action_group(action_group)

        menubar = uimanager.get_widget("/MenuBar")
        self.drawing_area = self.get_drawing_area()
        self.statusbar = Gtk.Statusbar()
        self.statusbar_context_id = self.statusbar.get_context_id("default_context_id")
        self.calculate_statusbar_message()

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(menubar, False, False, 0)
        box.pack_start(self.drawing_area, True, True, 0)
        box.pack_start(self.statusbar, False, False, 0)

        self.add(box)

    def add_file_menu_actions(self, action_group):
        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        action_group.add_action(action_filemenu)

        action_filenew = Gtk.Action("FileNew", None, None, Gtk.STOCK_NEW)
        action_filenew.connect("activate", self.on_menu_file_new)
        action_group.add_action(action_filenew)

        action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        action_filequit.connect("activate", self.on_menu_file_quit)
        action_group.add_action(action_filequit)

    def get_drawing_area(self):
        drawing_area = Gtk.DrawingArea()
        drawing_area.connect("draw", self.on_drawing_area_draw)
        drawing_area.connect("button-press-event", self.on_drawing_area_button_press_event)
        drawing_area.set_events(drawing_area.get_events() | Gdk.EventMask.BUTTON_PRESS_MASK)
        return drawing_area

    def on_drawing_area_draw(self, widget, cx):
        cx.set_line_width(5)
        for y in range(self.game_state.height):
            for x in range(self.game_state.width):
                cx.set_source_rgb(0, 0, 0)
                cell = self.game_state.grid[y][x]

                rx = GRID_OFFSET_X + CELL_SIZE * x
                ry = GRID_OFFSET_Y + CELL_SIZE * y
                cx.rectangle(rx, ry, CELL_SIZE, CELL_SIZE)
                cx.stroke()

                color = (0, 0, 0)
                if self.game_state.winning_cells and (x, y) in self.game_state.winning_cells:
                    color = (1, 0, 0)
                cx.set_source_rgb(*color)

                if cell == Cell.O:
                    cx.move_to(rx + CELL_SIZE - CELL_SIZE * 0.1, ry + CELL_SIZE / 2)
                    cx.arc(rx + CELL_SIZE / 2, ry + CELL_SIZE / 2, CELL_SIZE * 0.4, 0, math.pi * 2)
                elif cell == Cell.X:
                    cx.move_to(rx + CELL_SIZE * 0.2, ry + CELL_SIZE * 0.2)
                    cx.rel_line_to(CELL_SIZE * 0.6, CELL_SIZE * 0.6)
                    cx.move_to(rx + CELL_SIZE * 0.8, ry + CELL_SIZE * 0.2)
                    cx.rel_line_to(-1 * CELL_SIZE * 0.6, CELL_SIZE * 0.6)
                cx.stroke()

    def get_grid_coordinates(self, rx, ry):
        gx = math.floor((rx - GRID_OFFSET_X) / CELL_SIZE)
        gy = math.floor((ry - GRID_OFFSET_Y) / CELL_SIZE)
        if 0 <= gx <= self.game_state.width and 0 <= gy <= self.game_state.height:
            return gx, gy
        return None, None

    def on_drawing_area_button_press_event(self, widget, event):
        if self.game_state.status == GameStatus.ACTIVE:
            gx, gy = self.get_grid_coordinates(event.x, event.y)
            if gx is not None and gy is not None and self.game_state.grid[gy][gx] == Cell.EMPTY:
                self.game_state.place_symbol(gx, gy)
                self.on_game_state_change()
        return False

    def calculate_statusbar_message(self):
        if self.game_state.status == GameStatus.ACTIVE:
            message = "Current player: {current_player}".format(current_player=self.game_state.current_player)
        elif self.game_state.status == GameStatus.GAME_OVER:
            if self.game_state.winning_player is not None:
                message = "Game over! Player {winner} has won!".format(winner=self.game_state.winning_player)
            else:
                message = "Game over! Neither player has won!"
        self.statusbar.pop(self.statusbar_context_id)
        self.statusbar.push(self.statusbar_context_id, message)

    def on_game_state_change(self):
        self.drawing_area.queue_draw()
        self.calculate_statusbar_message()

    def on_menu_file_new(self, widget):
        self.game_state = GameState.get_initial_state()
        self.on_game_state_change()

    def on_menu_file_quit(self, widget):
        Gtk.main_quit()


win = TicTacToeWindow(GameState.get_initial_state())
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
