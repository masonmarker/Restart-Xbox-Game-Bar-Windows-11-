import subprocess
import time
import tkinter as tk
from tkinter import messagebox
import keyboard


default_gamebar_shortcut = '(Win + G)'


def is_process_running(process_name):
    """Determines if a process with a specific name is running."""
    result = subprocess.run(['tasklist', '/FI', f'IMAGENAME eq {process_name}'],
                            capture_output=True, text=True)
    return process_name.lower() in result.stdout.lower()


def restart_game_bar():
    """Restarts the Xbox Game Bar."""
    start = time.time()
    status_label.config(text="Terminating Xbox Game Bar...")
    root.update()
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'GameBar.exe'],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, check=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to terminate GameBar.exe:\n{e}")
        return

    status_label.config(text="Waiting for GameBar.exe to terminate...")
    root.update()
    while is_process_running('GameBar.exe'):
        time.sleep(0.1)

    status_label.config(text="GameBar.exe terminated. Restarting...")
    root.update()
    try:
        subprocess.run('start ms-gamebar:', shell=True, check=True)
    except Exception as e:
        messagebox.showerror("Error",
                             f"Failed to restart Xbox Game Bar:\n{e}\nTry manually starting it with {default_gamebar_shortcut}.")
        return

    status_label.config(text="Xbox Game Bar restarted. Attempting to open...")
    root.update()
    
    keyboard.press_and_release('windows+g')
    status_label.config(text="Xbox Game Bar opened successfully.")

    elapsed_time = time.time() - start
    status_label.config(text=f"Finished in {elapsed_time:.2f}s")


# Tkinter GUI
root = tk.Tk()
root.title("Xbox Game Bar Restarter")
root.geometry("400x200")
root.resizable(False, False)

# Header
header_label = tk.Label(root, text="Xbox Game Bar Restarter", font=("Helvetica", 16))
header_label.pack(pady=10)

# Instructions
instructions_label = tk.Label(root, text="Click the button below to restart Xbox Game Bar.")
instructions_label.pack(pady=5)

# Restart Button
restart_button = tk.Button(root, text="Restart Xbox Game Bar", font=("Helvetica", 12),
                           command=restart_game_bar)
restart_button.pack(pady=10)

# Status Label
status_label = tk.Label(root, text="", font=("Helvetica", 10), fg="blue")
status_label.pack(pady=10)

# Run Tkinter main loop
root.mainloop()