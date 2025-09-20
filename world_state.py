class WorldState:
    def __init__(self):
        self.day = 1
        self.hour = 0

    def step(self):
        self.hour += 1

        if self.hour >= 24:
            self.day += 1
            self.hour = 0

    def __str__(self):
        return f"Day {self.day}, {self.hour}" + ("AM" if self.hour < 12 else  "PM")