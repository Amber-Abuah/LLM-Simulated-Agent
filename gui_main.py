from world_state import WorldState
from agent import construct_agent, TimedEvent
from actions import StatEffect, StatType
from output import OutputHandler
import threading
from gui.gui_ctk import app, update_gui, update_gui_end, pause_play_manager
import time

num_days = 1
agent = construct_agent()
world_state = WorldState()
output = OutputHandler()
step_delay_seconds = 2

events = [TimedEvent("Your owner departed for work. You felt more lonely than usual...", -1, 9, [StatEffect(StatType.Fun, -15), StatEffect(StatType.Energy, -10)])
, TimedEvent("Your owner returned home! You were very excited!", -1, 17, [StatEffect(StatType.Fun, 20), StatEffect(StatType.Hunger, 10)])]

def agent_step(step):
    for e in events:
        if e.occur_hour == world_state.hour:
            agent.timed_event_affect(e, world_state)
    
    chosen_action = agent.decide_action(world_state)
    output_log = output.append_step(step, world_state, [e for e in events if e.occur_hour == world_state.hour], chosen_action, agent, print_to_console=False)

    hunger_percentage = agent.name_to_stats[StatType.Hunger].value / agent.name_to_stats[StatType.Hunger].max_value
    fun_percentage = agent.name_to_stats[StatType.Fun].value / agent.name_to_stats[StatType.Fun].max_value
    energy_percentage = agent.name_to_stats[StatType.Energy].value / agent.name_to_stats[StatType.Fun].max_value

    app.after(0, update_gui(str(world_state), step, chosen_action.lower(), hunger_percentage, energy_percentage, fun_percentage, output_log))
    agent.step()

    if world_state.hour == 23 and step != 0:
        agent.reflect(world_state.day)
        output.append_goal_reflection(agent.goal)

    world_state.step()

def agent_step_loop():
    for step in range(24 * num_days):
        while pause_play_manager.is_paused:
            time.sleep(0.5)

        agent_step(step)
        time.sleep(step_delay_seconds)

        if not agent.is_alive():
            break

    final_output = output.append_end(step, agent.is_alive)
    app.after(0, update_gui_end(final_output))

# Run agent logic on seperate thread, whilst GUI runs on main thread
threading.Thread(target=agent_step_loop, daemon=True).start()
app.mainloop()