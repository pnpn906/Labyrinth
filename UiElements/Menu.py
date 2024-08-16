import pygame
from Config import Config
from UiElements.UiElement import UIElement
from UiElements.Button import Button, Text
from UiElements.ItemSelector import ItemSelector
from UiElements.Image import Image

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

        # Окей, а как же другие элементы?
        for element in self.ui_elements.sprites()[:]:
            self.ui_elements.remove(element)
            self.AddUiElemnt(element)

    def GetTop(self):
        return self.titleRect.top

    def blit(self):
        super().blit()

        Config.get_Screen().blit(self.title_text, self.titleRect)

        for el in self.ui_elements.sprites():
            el.blit()

    def update(self):
        all_ui_elements = self.ui_elements.sprites()

        for uiElement in all_ui_elements:
            uiElement.update()

    def CheckPressed(self, x, y):
        pass

    def HandleEvent(self, event):
        all_ui_elements = self.ui_elements.sprites()

        for uiElement in all_ui_elements:
            uiElement.HandleEvent(event)

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
    curValue = 0
    text = None

    def ActionForBindIncrement():
        global curValue

        curValue +=1
        text.UpdateText(str(curValue))


    def ActionForBindDicrement():
        global curValue

        curValue -= 1
        text.UpdateText(str(curValue))

    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    Config.Initialize(screen)
    Config.InternalSetPyGame(pygame)
    menu = Menu("UiElements", 500, 1000, (60,60,60), 200, 50)
    subMenu = Menu("Submenu", 400, 500, (90,90,0), orientation="horizontal")
    subMenu2 = Menu("Submenu2", 400, 150, (154,45,0))
    subMenu3 = Menu("Submenu3", 400, 300, (233,233,233))

    subMenu31 = Menu("Submenu4", 300, 250, (0, 3, 100))
    subMenu311 = Menu("Submenu5", 200, 200, (100, 7, 0))
    subMenu3111 = Menu("Submenu6", 100, 100, (80, 56, 70))
    subMenu31111 = Menu("Submenu6", 50, 50, (250, 0, 70))



    text = Text(str(curValue), 20, (0, 0, 0))

    menu.AddUiElemnt(subMenu)
    btn1 = Button("+", 20, 20, 20, (243, 243, 243))
    btn1.BindAction(ActionForBindIncrement)
    btn2 = Button("-", 20, 10, 10, (243, 243, 243))
    btn2.BindAction(ActionForBindDicrement)

    subMenu.AddUiElemnt(btn1)
    subMenu.AddUiElemnt(text)
    subMenu.AddUiElemnt(btn2)

    # TODO - не позиционируются элементы с большой глубиной
    subMenu21 = Menu("Submenu31", 200, 100, (255, 255, 255), orientation="horizontal")
    text1 = Text("Text1", 20, (0, 0, 0))
    text2 = Text("TExt2", 20, (0, 0, 0))
    subMenu21.AddUiElemnt(text1)
    subMenu21.AddUiElemnt(text2)

    subMenu2.AddUiElemnt(subMenu21)
    menu.AddUiElemnt(subMenu2)
    menu.AddUiElemnt(subMenu3)

    # Depth - 5
    #subMenu3.AddUiElemnt(subMenu31)
    #subMenu31.AddUiElemnt(subMenu311)
    #subMenu311.AddUiElemnt(subMenu3111)
    #subMenu3111.AddUiElemnt(subMenu31111)

    # ItemSelector
    textGroup = pygame.sprite.Group()
    textGroup.add(Text("Select1", 20, (0, 0, 0)))
    textGroup.add(Text("Select2", 20, (0, 0, 0)))
    textGroup.add(Text("Select3", 20, (0, 0, 0)))
    textGroup.add(Text("Select4", 20, (0, 0, 0)))
    textGroup.add(Text("Select5", 20, (0, 0, 0)))
    textGroup.add(Text("Select6", 20, (0, 0, 0)))
    textGroup.add(Text("Select6", 20, (0, 0, 0)))
    textGroup.add(Text("Select6", 20, (0, 0, 0)))
    itemSelector = ItemSelector(textGroup, 350, 250)

    imgGroup = pygame.sprite.Group()
    imgGroup.add(Image("fioor.png", (255,0,0), 30,30))
    imgGroup.add(Image("fioor.png", (255,0,0), 30,30))
    imgGroup.add(Image("fioor.png", (255,0,0), 30,30))

    itemSelector2 = ItemSelector(imgGroup, 350, 250)
    subMenu3.AddUiElemnt(itemSelector)

    subMenu.AddUiElemnt(itemSelector2)
    while True:
        screen.fill((33, 174, 233))

        for event in pygame.event.get():
            menu.HandleEvent(event)

        menu.update()

        menu.blit()

        pygame.display.flip()