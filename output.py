class OutputHandler:
    def __init__(self):
        self.output_stream = []
        self.seperator = "\n" + "-" * 10

    def append_step(self, step: int, world_state, events, chosen_action, agent, print_to_console=True):
        output = f"Step {step + 1}:\n{str(world_state)}\n"

        for e in events:
            output += "Event: "+  str(e) + "\n"        
        
        output += f"\n{agent}\n\nAction chosen by agent: {chosen_action}."
        output += self.seperator
        self.output_stream.append(output)

        if print_to_console:
            print(output)

        return output

    def append_goal_reflection(self, goal: str, print_to_console=True):
        output = f"Agent has reflected on its action during the day and updated its goal to:\n{goal}" + self.seperator
        self.output_stream.append(output)

        if print_to_console:
            print(output)

    def append_end(self, step, is_alive:bool):
        output = ""
        if not is_alive:
            output += f"Agent has died at step {step + 1}."
        else:
            output += f"Agent has successfully survived entire simulation."

        output += "\nSimulation finished."
        self.output_stream.append(output)
        return output

    def write_output(self):
        open("agent_output/output.txt", "w").write("\n".join(self.output_stream))