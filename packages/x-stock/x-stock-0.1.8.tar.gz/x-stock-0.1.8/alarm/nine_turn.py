

class NineTurn:
    """神奇的九转大法
    """
    def __init__(self):
        self._alarm = False

    def turn_on(self):
        self._alarm = True

    def turn_off(self):
        self._alarm = False

    def is_on(self):
        return self._alarm