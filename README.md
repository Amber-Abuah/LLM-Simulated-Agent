## LLM Simulated Agent  
A survival-based simulation, similar to Tamagotchi, where a virtual cat must autonomously perform actions to increase its chance of survival.
 
### 💤 Needs  
The agent has 3 needs:
- **Hunger**, 
- **Fun**, 
- **Energy**,
   
which must be kept above 0 to survive during the simulation.  

### 🤖 Decision Making  
The agent uses a small Large Language Model (LLama3), capable of choosing actions based on the cat’s current state, past memories, and daily goals.

### 🔄 Reflection  
At the end of each day, the agent reflects upon its actions from the current day and creates a new goal to follow the next day.  
For example, if the agent neglected playing during the day, it will attempt to play more the following day.

### ❗Dynamic Event Adaptation  
Random events may occur during the day, which may have a sudden negative or positive effect on the agent's needs.  
The agent is capable of adapting to these sudden changes and continuing to survive.