if Game.showMenu:
    # Main menu

    new_menu = NewMenu("NEW MENU", Game.screen.get_width(), Game.screen.get_height(), (60, 60, 60), 0, 0, alignment="center")

    btn1 = Button("вернуться в главное меню", 20, 470, 40, (243, 243, 223))
    btn2 = Button("продолжить игру", 20, 470, 40, (243, 243, 223))


    new_menu.AddUiElemnt(btn1)
    new_menu.AddUiElemnt(btn2)
