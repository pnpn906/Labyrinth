from UiElements.UiElement import UIElement
from Config import Config
import pygame

class Image(UIElement):
    def __init__(self, texture, hight_light_color, width, height, x=0, y=0):
        super().__init__(width + 2, height + 2, hight_light_color, x=x, y=y)

        self.texture = texture
        image = pygame.image.load(f"{texture}").convert_alpha()
        self.image = pygame.transform.scale(image, (width, height))
        self.img_rect = self.image.get_rect()
        self.need_high_light = False

    def high_light(self, hight_light=True):
        self.need_high_light = hight_light
    def RebuildFromMain(self):

        super().RebuildFromMain()
        self.img_rect.center = self.main_rect.center
    def blit(self):
        if self.need_high_light:
            super().blit()
        Config.get_Screen().blit(self.image,self.img_rect)

    def HandleEvent(self, event, **args):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x,y = event.pos

            if self.CheckPressed(x,y):
                print(args)
                args["texture"] = self.texture
                print(args)
                print(**args)
                self.Pressed(**args)