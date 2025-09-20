from world_state import WorldState
from agent import construct_agent, TimedEvent
from actions import StatEffect, StatType
from output import OutputHandler

num_days = 7
agent = construct_agent()
world_state = WorldState()
output = OutputHandler()

events = [TimedEvent("Your owner departed for work. You felt more lonely than usual...", -1, 9, [StatEffect(StatType.Fun, -15), StatEffect(StatType.Energy, -10)])
, TimedEvent("Your owner returned home! You were very excited!", -1, 17, [StatEffect(StatType.Fun, 20), StatEffect(StatType.Hunger, 10)])]

for step in range(24 * num_days):
    for e in events:
        if e.occur_hour == world_state.hour:
            agent.timed_event_affect(e, world_state)
    
    chosen_action = agent.decide_action(world_state)
    output.append_step(step, world_state, [e for e in events if e.occur_hour == world_state.hour], chosen_action, agent)
    agent.step()

    if not agent.is_alive():
        break

    if world_state.hour == 23 and step != 0:
        agent.reflect(world_state.day)
        output.append_goal_reflection(agent.goal)

    world_state.step()

print("Simulation finished.")
output.append_end(step, agent.is_alive)
output.write_output()