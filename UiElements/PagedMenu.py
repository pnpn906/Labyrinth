from UiElements.UiElement import UIElement
from UiElements.Menu import Menu

class PagedMenu(UIElement):
    BIND_NEXT = "next_bind"
    BIND_BACK = "back_bind"

    def __init__(self, *menus, **forBind):
        self.menus = list()

        for menu in menus:
            if not isinstance(menu, Menu):
                raise Exception("Элемент не является меню.")

            self.menus.append(menu)

        nextBind = forBind.get(PagedMenu.BIND_NEXT)
        backBind = forBind.get(PagedMenu.BIND_BACK)

        if nextBind is not None:
            self.__bind(nextBind, self.go_to_next)

        if backBind is not None:
            self.__bind(backBind, self.go_to_back)

        self.current_position = 0

    def __bind(self, listBtns, action):
        if not isinstance(listBtns, list):
            raise Exception("Not list.")

        for el in listBtns:
            if not isinstance(el, UIElement):
                raise Exception("Not UI element.")

            el.BindAction(action)

    def blit(self):
        self.menus[self.current_position].blit()

    def update(self, *args, **kwargs):
        self.menus[self.current_position].update()

    def HandleEvent(self, event, **args):
        return self.menus[self.current_position].HandleEvent(event, **args)

    def go_to_next(self, **kwargs):
        self.__incr()

    def go_to_back(self, **kwargs):
        self.__decr()

    def __incr(self):
        self.current_position += 1

        if self.current_position > len(self.menus) - 1:
            self.current_position = 0

        print(self.current_position)

    def __decr(self):
        print(self.current_position)
        self.current_position -= 1

        if self.current_position < 0:
            self.current_position = len(self.menus) - 1