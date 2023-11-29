import platform
import psutil
import cpuinfo
import tkinter as tk
from tkinter import ttk

def read_requirements(file_path):
    requirements = {}
    current_game = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                current_game = line[1:-1]
                requirements[current_game] = {}
            elif current_game and '=' in line:
                key, value = line.split('=')
                requirements[current_game][key.strip()] = value.strip()

    return requirements

def compare_requirements(system_info, selected_game, game_requirements):
    result = ""
    reqs = game_requirements.get(selected_game, {})
    
    if not reqs:
        return "Selected game not found in requirements."

    result += f"\nComparison Result for {selected_game}:\n"
    for req, value in reqs.items():
        if req in system_info:
            system_value = convert_to_mb(system_info[req])
            req_value = convert_to_mb(value)

            if system_value >= req_value:
                result += f"{req}: {value} - Requirement met\n"
            else:
                result += f"{req}: {value} - Requirement NOT met\n"
        else:
            result += f"{req}: {value} - Requirement NOT met\n"
    return result

def convert_to_mb(value):
    if isinstance(value, str):
        if 'GB' in value:
            return int(float(value.replace('GB', '')) * 1024)
        elif 'MB' in value:
            return int(float(value.replace('MB', '')))
        elif 'VRAM' in value:
            return int(value.split(' ')[0])
        try:
            return int(float(value))
        except ValueError:
            return 0
    return int(value)

def get_system_info():
    system_info = {
        'OS': platform.system(),
        'Processor': cpuinfo.get_cpu_info()['brand_raw'],
        'RAM': f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB",
        'GPU': 'Your GPU information here', 
    }
    return system_info

def on_game_selected(event):
    selected_game = game_menu.get()
    if selected_game:
        system_info = get_system_info()
        system_info_text.set(format_system_info(system_info))
        software_info_text.set(format_software_info(software_requirements[selected_game]))
        result_text.set(compare_requirements(system_info, selected_game, software_requirements))

def format_system_info(system_info):
    formatted_info = "System Information:\n"
    for key, value in system_info.items():
        formatted_info += f"{key}: {value}\n"
    return formatted_info

def format_software_info(software_info):
    formatted_info = "Software Information:\n"
    for key, value in software_info.items():
        formatted_info += f"{key}: {value}\n"
    return formatted_info

root = tk.Tk()
root.title("System Requirements Checker")

file_path = 'software_requirements.txt'
software_requirements = read_requirements(file_path)
games = list(software_requirements.keys())

result_text = tk.StringVar()
result_text.set("")

system_info_text = tk.StringVar()
system_info_text.set("")

software_info_text = tk.StringVar()
software_info_text.set("")


bg_color = "#f0f0f0"  
text_color = "#333333" 
font_style = ("Helvetica", 12)


label_game = tk.Label(root, text="Select Game:", background=bg_color, fg=text_color, font=font_style)
label_game.grid(row=0, column=0, pady=10, sticky='w')

game_menu = ttk.Combobox(root, values=games, font=font_style)
game_menu.grid(row=0, column=1, pady=10, sticky='w')
game_menu.bind("<<ComboboxSelected>>", on_game_selected)

result_label = tk.Label(root, textvariable=result_text, justify="left", wraplength=400, background=bg_color, fg=text_color, font=font_style)
result_label.grid(row=2, column=0, columnspan=2, pady=10)


system_info_label = tk.Label(root, textvariable=system_info_text, justify="left", wraplength=400, background=bg_color, fg=text_color, font=font_style)
system_info_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')


software_info_label = tk.Label(root, textvariable=software_info_text, justify="left", wraplength=400, background=bg_color, fg=text_color, font=font_style)
software_info_label.grid(row=1, column=1, padx=10, pady=10, sticky='w')


root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)


root.configure(background=bg_color)


root.mainloop()
