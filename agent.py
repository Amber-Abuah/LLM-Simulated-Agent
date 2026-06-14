from actions import Stat, StatType, Action, StatEffect, TimedEvent
import ollama
import re
from memory import MemoryStream

max_stat_value = 50
stat_decay_rate = 2
stat_increase_rate = 7

base_prompt = open("prompt_template/prompt_template.txt").read()

class LLM:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def __call__(self, prompt: str):
        return ollama.chat(self.model_name, messages=[{"role":"system", "content":prompt}]).message.content


class Agent:
    def __init__(self, stats: list[Stat], possible_actions: list[Action]):
        self.llm = LLM("llama3")
        self.stats = stats
        self.name_to_stats = {s.stat_type:s for s in stats}
        self.possible_actions = possible_actions
        self.name_to_action = dict([[action.action_name, action] for action in possible_actions])
        self.memories = MemoryStream()
        self.goal = "'I want to maximise my stats to survive until the end of the day and diversify my actions over the hours.'"

    def decide_action(self, world_state):
        llm_response = self.llm(self.construct_prompt(world_state))
        extracted_actions = re.findall("|".join(rf"{action.action_name}" for action in self.possible_actions), llm_response)
        chosen_action = extracted_actions[-1] if len(extracted_actions) > 0 else "Nothing"
        self.name_to_action[chosen_action](self.stats)
        self.memories.add_action_memory(self.name_to_action[chosen_action], world_state)
        return chosen_action
    
    def step(self):
        recent_memories = self.memories.recall_previous_hour()

        for stat in self.stats:
            if not any(stat.stat_type in affected_stats for affected_stats in [r.action_event.get_affected_stats() for r in recent_memories]):
                stat.natural_decay()

    def is_alive(self):
        return False not in [stat.value > 0 for stat in self.stats]
    
    def reflect(self, day):
        day_memories = self.memories.recall_day_memories(day)
        action_count = dict([[action.action_name, len([mem for mem in day_memories if mem.action_event == action])] for action in self.possible_actions if action.action_name != "Nothing"])
        least_chosen_action_name = min(action_count, key=action_count.get)
        self.goal = f"'I would like to {least_chosen_action_name} just a little more today, but only if I am not in not in danger or near death.'"

    def construct_prompt(self, world_state) -> str:
        prompt = base_prompt
        prompt = prompt.replace("{day-time}", str(world_state))
        prompt = prompt.replace("{memory}", self.memories.recall_recent_memories())
        prompt = prompt.replace("{goal}", self.goal)
        prompt = prompt.replace("{actions}", "\n".join(f"`{action.action_name}`: {action.action_desc}"  for action in self.possible_actions))
        prompt = prompt.replace("{stats}", "\n".join(f"You are {stat}" for stat in self.stats))
        return prompt
    
    def timed_event_affect(self, event: TimedEvent, world_state):
        event(self.stats)
        self.memories.add_event_memory(event, world_state)
    
    def __str__(self):
        return "Cat stats:\n" + "\t".join([f"{stat.stat_type.name}: {stat.value}" for stat in self.stats])

def construct_agent() -> Agent:
    return Agent(stats=[
        Stat(StatType.Hunger, max_stat_value, stat_decay_rate, ["full of food.", "slightly peckish.", "getting very hungry.", "extremely famished. If you do not Eat soon you will die."]),
        Stat(StatType.Energy, max_stat_value, stat_decay_rate, ["full of energy.", "slightly tired.", "very sleepy.", "on the brink of exhaustion. If you do not Sleep soon you will die."]),
        Stat(StatType.Fun, max_stat_value, stat_decay_rate, ["excited and content.", "a bit bored.", "very bored.", "on the verge of death from boredom. If you do not Play soon you will die."])
    ],

    possible_actions=[
        Action("Eat", "Munch on some kibble from your food bowl to reduce hunger.", [StatEffect(StatType.Hunger, stat_increase_rate)]),
        Action("Sleep", "Lie down and rest on the floor to restore energy.", [StatEffect(StatType.Energy, stat_increase_rate)]),
        Action("Play", "Play with your tail to increase fun.", [StatEffect(StatType.Fun, stat_increase_rate)]),
        Action("Nothing", "Stare into thin air without a single thought.", []),
    ])
