import customtkinter as ctk
from gui.gui_cat_drawer import build_grid

### Visual Settings ------------------------------------------------------------

width = 1000
height = 520
font_size = 20
font = "Segoe UI"

large_font_size = 20
medium_font_size = 17
small_font_size = 15

button_colour = "#d56ebb"
button_hover_colour = "#bb5da3"
button_width = 40

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

### App Creation ------------------------------------------------------------

app = ctk.CTk()
app.geometry(f"{width}x{height}")
app.title("LLM Simulated Agent")
app.iconbitmap("gui/icon.ico")

left_frame = ctk.CTkFrame(app, width=width/2, height=height)
left_frame.pack(side=ctk.LEFT)
left_frame.pack_propagate(False)

right_frame = ctk.CTkFrame(app, width=width/2, height=height)
right_frame.pack(side=ctk.RIGHT, fill="x")
right_frame.pack_propagate(False)

### Left Frame ------------------------------------------------------------
# Consists of ASCII art, basic simulation + step info and button controls.

title_label = ctk.CTkLabel(left_frame, text="Simulation Starting...", font=(font, medium_font_size, "bold"))
title_label.pack()

top_divider = ctk.CTkFrame(left_frame, height=2, bg_color="white")
top_divider.pack(fill="x")

cat = build_grid("sit")

agent_art_label = ctk.CTkLabel(left_frame, text=cat, font=("TKFixedFont", large_font_size), justify=ctk.LEFT)
agent_art_label.pack()

bottom_divider = ctk.CTkFrame(left_frame, height=2, bg_color="white")
bottom_divider.pack(fill="x")

step_label = ctk.CTkLabel(left_frame, text="Step 0", font=(font, small_font_size))
step_label.pack()

agent_action_label = ctk.CTkLabel(left_frame, text="", font=(font, small_font_size), justify=ctk.LEFT)
agent_action_label.pack()

control_frame = ctk.CTkFrame(left_frame)
control_frame.pack(pady=10)

for button_type in ["<<", "||", ">>"]:
    button = ctk.CTkButton(control_frame, text=button_type, font=(font, 12, "bold"), fg_color=button_colour, hover_color=button_hover_colour, width=button_width)
    button.pack(side=ctk.LEFT, padx=2)

### Right Frame ------------------------------------------------------------
# Consists of agent's needs and actions log.

needs_frame = ctk.CTkFrame(right_frame)
needs_frame.pack(fill="x")

needs_title = ctk.CTkLabel(needs_frame, text="Needs", font=(font, medium_font_size, "bold"))
needs_title.pack()

need_state_labels = {}

for need in ["Hunger", "Fun", "Energy"]:
    hunger_frame = ctk.CTkFrame(needs_frame, width=20, height=20)
    hunger_frame.pack(fill="x")

    need_label = ctk.CTkLabel(hunger_frame, text=need, font=(font, small_font_size))
    need_label.pack(side=ctk.LEFT, padx=10)

    state_label = ctk.CTkLabel(hunger_frame, text="▉▉▉▉▉▉▉▉▉▉")
    state_label.pack(side=ctk.RIGHT, padx=10)

    need_state_labels[need] = state_label

log_label = ctk.CTkLabel(right_frame, text="Log", font=(font,medium_font_size, "bold"))
log_label.pack(pady=(10,0))

log_frame = ctk.CTkScrollableFrame(right_frame, height=580)
log_frame.pack(fill="both")

log_entries = ctk.CTkLabel(log_frame, text="", font=(font, small_font_size), justify=ctk.LEFT, wraplength=width/2)
log_entries.pack(fill="both")

### Functions to update GUI  ------------------------------------------------------------

def update_need_figure(stat_label:ctk.CTkLabel, need_percentage:float):
    stat_label.configure(text="".join(["▉" if need_percentage > i/10 else "☐" for i in range(10)]))

def add_log_entry(output:str):
    log_entries.configure(text=log_entries._text + "\n" + output)

def update_gui(day_hour:str, step:int, action:str, hunger_percentage:float, energy_percentage:float, fun_percentage:float, log:str):
    title_label.configure(text=day_hour)
    step_label.configure(text=f"Step {step}")
    agent_art_label.configure(text=build_grid(action))
    agent_action_label.configure(text=f"Cat has decided to: {action.capitalize()}")

    update_need_figure(need_state_labels["Hunger"] , hunger_percentage)
    update_need_figure(need_state_labels["Fun"] , fun_percentage)
    update_need_figure(need_state_labels["Energy"] , energy_percentage)

    add_log_entry(log)

def update_gui_end(output:str):
    agent_action_label.configure(text=output)
    add_log_entry(output)