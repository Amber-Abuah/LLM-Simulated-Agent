import copy

class Memory:
    def __init__(self, action_event, world_state):
        self.action_event = action_event
        self.world_state = world_state
    
class ActionMemory(Memory):
    def __str__(self):
        return f"On {self.world_state}, you performed {self.action_event.action_name}."
    
class EventMemory(Memory):
    def __str__(self):
        return f"On {self.world_state}, {self.action_event.event_desc}."
        
class MemoryStream:
    def __init__(self):
        self.memories = []

    def add_action_memory(self, action, world_state):
        self.memories.append(ActionMemory(action, copy.deepcopy(world_state)))

    def add_event_memory(self, event, world_state):
        self.memories.append(EventMemory(event, copy.deepcopy(world_state)))

    def recall_recent_memories(self, n: int = 3) -> str:
        return "\n".join([str(mem) for mem in self.memories[-n:]][::-1]) if len(self.memories) > 0 else "No previous memories."
    
    def recall_day_memories(self, day: int) -> list[Memory]:
        return [mem for mem in self.memories if mem.world_state.day == day]
    
    def recall_previous_hour(self) -> list[Memory]:
        current_day, previous_hour = self.memories[-1].world_state.day, self.memories[-1].world_state.hour
        return [mem for mem in self.memories if mem.world_state.day == current_day and mem.world_state.hour == previous_hour]

    def __str__(self):
        return "\n".join(str(mem) for mem in self.memories)