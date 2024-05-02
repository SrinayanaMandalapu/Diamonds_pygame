import pygame
import sys
import os
import random
from gameplay import Game
from strategy import ComputerStrategy
from ui import UI

class FullGame:
    def __init__(self):
        self.ui = UI()

    def main_menu(self):
        self.ui.main_menu()

    def start_game(self, against_computer):
        self.ui.start_game(against_computer)

    def quit_game(self):
        self.ui.quit_game()

if __name__ == "__main__":
    pygame.init()
    full_game = FullGame()
    full_game.main_menu()
