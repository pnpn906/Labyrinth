import pygame
from pygame.rect import Rect

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        te = target.rect.move(self.state.topleft)
        return te

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

