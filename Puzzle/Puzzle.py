import pygame
from Config import Config


class Puzzle():
    def __init__(self):
        super().__init__()
        self.__screen = Config.get_Screen()
        self.__puzzletilemap = Config.__puzzletilemap()