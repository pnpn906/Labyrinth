import pygame
from Config import Config
from UiElement import UIElement
from Button import Button

class Menu(UIElement):
    def __init__(self, title, width, height, background_color, x=0,y=0, orientation="vertical"):
        super().__init__(width, height, background_color, x, y)

        self.title = title
        self.need_show = False

        self.ui_elements = pygame.sprite.Group()

        # Orientation Block
        self.spacing = 30
        self.orientation = orientation    # не используется нигде, хотя должна

        # Title Block
        self.textColor = (0, 0, 0)
        self.textStyle = "arial"
        self.textSize = 20
        self.textAntialias = True
        self.SetTitle()

    def SetTitle(self):
        print(pygame.font.get_fonts())
        font = pygame.font.SysFont(self.textStyle, self.textSize)
        self.title_text = font.render(self.title, self.textAntialias, self.textColor)
        self.titleRect = self.title_text.get_rect()
        self.RebuildFromMain()

    def RebuildFromMain(self):
        self.titleRect.bottom = self.main_rect.top
        self.titleRect.left = self.main_rect.left

    def GetTop(self):
        return self.titleRect.top

    def blit(self):
        super().blit()

        Config.get_Screen().blit(self.title_text, self.titleRect)

        for el in self.ui_elements.sprites():
            el.blit()

    def update(self):
        pass

    def AddUiElemnt(self, ui_element: UIElement):
        """
        Чтобы правильно все позиционировалось необходимо строить дерево следующим образом:
        - создал элемент родителя (э1)
        - закинул в него дочерний элемент (э2)
        - потом создаешь и добавляешь дочерние элементы для э2.

        :param ui_element:
        :return:
        """
        if not isinstance(ui_element, UIElement):
            raise Exception("В элементы пользовательского интерфейса можно добавлять только объекты UIElement.")

        all_ui_elements = self.ui_elements.sprites()


        # Если элементов никаких нет, то позицизионировать наш добавляемый элемент  будем относительно
        # верха/лева (в зависимости от ориентации)
        # Если элементы есть, то позицизионировать  наш добавляемый элемент будем относительно
        # низа/права последнего элемента в списке (в зависимости от ориентации)z

        relative_ui_elemnt = None

        if len(all_ui_elements) == 0:
            relative_ui_elemnt = self
        else:
            relative_ui_elemnt = all_ui_elements[-1]

        if self.orientation == "vertical":
            if relative_ui_elemnt == self:
                relativeTop = relative_ui_elemnt.main_rect.top
            else:
                relativeTop = relative_ui_elemnt.GetBottom()

            newTop = relativeTop + self.spacing

            ui_element.SetCoords(self.GetLeft() + 30,newTop)
        else:
            relativeTop = self.main_rect.top
            newTop = relativeTop + self.spacing

            if relative_ui_elemnt == self:
                relative_right = relative_ui_elemnt.main_rect.left
            else:
                relative_right = relative_ui_elemnt.GetRight()

            newLeft = relative_right + self.spacing
            ui_element.SetCoords(newLeft, newTop)

        self.ui_elements.add(ui_element)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    Config.Initialize(screen)
    Config.InternalSetPyGame(pygame)
    menu = Menu("Menu", 500, 1000, (60,60,60), 200, 50)
    subMenu = Menu("Submenu", 400, 500, (90,90,0), orientation="horizontal")
    subMenu2 = Menu("Submenu2", 400, 150, (0,0,0))
    subMenu3 = Menu("Submenu3", 400, 150, (0,0,0))

    menu.AddUiElemnt(subMenu)
    btn1 = Button("+", 20, 20, 20, (243, 243, 243))
    btn2 = Button("-", 20, 10, 10, (243, 243, 243))
    btn3 = Button("-", 20, 40, 40, (243, 243, 243))
    subMenu.AddUiElemnt(btn1)
    subMenu.AddUiElemnt(btn2)
    subMenu.AddUiElemnt(btn3)

    menu.AddUiElemnt(subMenu2)
    menu.AddUiElemnt(subMenu3)
    while True:
        screen.fill((33, 174, 233))

        menu.blit()

        pygame.display.flip()