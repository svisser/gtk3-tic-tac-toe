from tictactoe.game import GameState, Player

import pytest


@pytest.fixture
def game_state():
    return GameState.get_initial_state()


@pytest.mark.parametrize("cells", [
    {(0, 0), (1, 0), (2, 0)},  # horizontal
    {(0, 0), (0, 1), (0, 2)},  # vertical
    {(0, 0), (1, 1), (2, 2)},  # diagonal 1
    {(2, 0), (1, 1), (0, 2)},  # diagonal 2
])
def test_place_winning_situations(game_state, cells):
    for cell in cells:
        game_state.place_symbol(*cell, player=Player.X)
    assert game_state.winning_player == Player.X
    assert game_state.winning_cells == cells
