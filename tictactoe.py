from __future__ import annotations

import numpy as np

def _get_player_str(player_num) -> str:
    if player_num == 1:
        return 'X'
    elif player_num == -1:
        return 'O'
    else:
        return ' '


class TicTacToe:

    def __init__(self, x_is_initial_player = True):
        self.gameState = np.array([[0, 0, 0],
                                  [0, 0, 0],
                                  [0, 0, 0]])

        if x_is_initial_player:
            self.currentPlayer = 'X'
        else:
            self.currentPlayer = 'O'

    def __str__(self):
        return f" {_get_player_str(self.gameState[0][0])}  |  {_get_player_str(self.gameState[0][1])}  |  {_get_player_str(self.gameState[0][2])}\n" + \
            "---------------\n" + \
            f" {_get_player_str(self.gameState[1][0])}  |  {_get_player_str(self.gameState[1][1])}  |  {_get_player_str(self.gameState[1][2])}\n" + \
            "---------------\n" + \
            f" {_get_player_str(self.gameState[2][0])}  |  {_get_player_str(self.gameState[2][1])}  |  {_get_player_str(self.gameState[2][2])}\n"

    def _toggle_player(self) -> None:
        if self.currentPlayer == 'X':
            self.currentPlayer = 'O'
        else:
            self.currentPlayer = 'X'

    def make_move(self, player, loc) -> int | None:
        loc_x = loc % 3
        loc_y = loc // 3

        if loc < 0 or loc > 8 or self.gameState[loc_y][loc_x] != 0:
            raise ValueError("Invalid location")

        if player != self.currentPlayer:
            raise ValueError("Invalid player")

        self.gameState[loc_y][loc_x] = 1 if self.currentPlayer == 'X' else -1
        if self._check_win_state():
            return 1 if player == "X" else -1

        if self._check_draw_state():
            return 0
        self._toggle_player()

        return None

    def get_current_game_state(self) -> np.ndarray:
        return self.gameState

    def get_active_player(self) -> str:
        return self.currentPlayer

    def _check_draw_state(self) -> bool:
        #check rows
        for row in self.gameState:
            if 0 in row:
                return False
        return True


    def _check_win_state(self) -> bool:
        # Check rows
        for row in self.gameState:
            if 0 in row:
                continue
            if row[0] == row[1] == row[2]:
                return True

        # Check columns
        for col in range(3):
            column = self.gameState[:, col]
            if 0 in column:
                continue
            if column[0] == column[1] == column[2]:
                return True

        # Check diagonals
        if self.gameState[1][1] == 0:
            return False

        if self.gameState[0][0] == self.gameState[1][1] == self.gameState[2][2]:
            return True

        if self.gameState[0][2] == self.gameState[1][1] == self.gameState[2][0]:
            return True

        return False