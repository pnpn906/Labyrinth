from UiElement import UIElement
import pygame

class ItemSelector(UIElement):
    def __init__(self, values: pygame.sprite.Group, width, height, x=0, y=0, orientation="horizontal"):
        super().__init__(width, height, x=x, y=y)
        self.ui_elements = values
        self.currentSelectedText = None

        if len(values.sprites()) == 0:
            raise Exception("Values can not be empty.")

        for val in values.sprites():
            if not isinstance(val, UIElement):
                raise Exception("В элементы пользовательского интерфейса можно добавлять только объекты UIElement.")

        # Orientation Block
        self.spacing = 30
        self.top_spacing = 10
        self.orientation = orientation

        if self.orientation == "horizontal":
            pass

    def RebuildFromMain(self):
        relative = self

        for element in self.ui_elements.sprites():
            if relative == self:
                newTop = self.GetTop()
                newLeft = self.GetLeft()
            else:
                relativeRight = relative.GetRight()

                newTop = relative.GetTop()
                newLeft = relativeRight + self.spacing

            element.SetCoords(newLeft, newTop)

            if element.GetRight() > self.main_rect.right:
                newTop = element.GetBottom() + self.top_spacing
                newLeft = self.GetLeft()
                element.SetCoords(newLeft, newTop)

            relative = element

    def blit(self):

        for el in self.ui_elements.sprites():
            el.blit()

    def HandleEvent(self, event):
        super().HandleEvent(event)

        all_ui_elements = self.ui_elements.sprites()

        for uiElement in all_ui_elements:
            uiElement.HandleEvent(event)