class PausePlayManager:
    def __init__(self):
        self.is_paused = False

    def invert_is_paused(self):
        self.is_paused = not self.is_paused