class Config:
    __screen = None
    __map = None
    __puzzletilemap = None
    __pygame = None
    __isInitialized = False
    __player = None

    @staticmethod
    def Initialize(screen):
        Config.__screen = screen
        Config.__isInitialized = Config.CheckAllProps()

    @staticmethod
    def InternalSetPyGame(pygame):
        Config.__pygame = pygame

    @staticmethod
    def get_pygame():
        return Config.__pygame

    @staticmethod
    def InternalSetTileMap(map):
        Config.__map = map

    @staticmethod
    def InternalSetPuzzleTileMap(puzzletilemap):
        Config.__puzzletilemap = puzzletilemap

    @staticmethod
    def InternalSetPlayer(player):
        Config.__player = player

    @staticmethod
    def get_Player():
        return Config.__player

    @staticmethod
    def ValidateInitialize():
        if not Config.__isInitialized:
            raise Exception("Config is not initialized!")

    @staticmethod
    def CheckAllProps():
        return (Config.__map is not None
                and Config.__screen is not None)

    @staticmethod
    def get_Screen():
        return Config.__screen

    @staticmethod
    def get_Map():
        return Config.__map
