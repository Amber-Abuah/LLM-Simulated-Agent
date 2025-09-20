from enum import Enum

class StatType(Enum):
    Hunger = 1,
    Fun = 2,
    Energy = 3

class Stat:
    def __init__(self, stat_type: StatType, max_value: int, decay_rate: int, stat_descs: list[str]):
        self.stat_type = stat_type
        self.max_value = max_value
        self.decay_rate = decay_rate
        self.value = max_value
        self.stat_descs = stat_descs

    def natural_decay(self):
        self.value = max(0, self.value - self.decay_rate)

    def affect(self, value: int):
        self.value = max(min(self.value + value, self.max_value), 0)

    def __str__(self):
        increments = self.max_value / len(self.stat_descs)

        for i in range(len(self.stat_descs)):
            if(self.value >= self.max_value - increments * (i + 1)):
                return self.stat_descs[i]

        return "error state."

class StatEffect:
    def __init__(self, stat_type: StatType, effect: int):
        self.stat_type = stat_type
        self.effect = effect

    def __call__(self, stats: list[Stat]):
        for stat in stats:
            if stat.stat_type == self.stat_type:
                stat.affect(self.effect)


class Action:
    def __init__(self, action_name: str, action_desc: str, stat_effects: list[StatEffect]):
        self.action_name = action_name
        self.action_desc = action_desc
        self.stat_effects = stat_effects

    def __call__(self, stats: list[Stat]):
        for stat_effect in self.stat_effects:
            stat_effect(stats)

    def get_affected_stats(self):
        return [s.stat_type for s in self.stat_effects]

class TimedEvent(Action):
    def __init__(self, event_desc: str, occur_day: int, occur_hour: int, stat_effects: list[StatEffect]):
        self.event_desc = event_desc
        self.occur_day = occur_day
        self.occur_hour = occur_hour
        self.stat_effects = stat_effects

    def __str__(self):
        return self.event_desc