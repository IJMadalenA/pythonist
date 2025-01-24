import os
import platform
import random
import time
import tkinter as tk
from tkinter import messagebox

def pull_the_trigger(bullets: int):
    shoot = random.randint(1, 6)
    time.sleep(4)

    if shoot <= bullets:
        current_os = platform.system()

        if current_os == "Windows":
            os.system("shutdown /s /t 0")
        elif current_os == "Linux":
            os.system("shutdown now")

        return "You're dead."
    else:
        return "You're alive."


def on_button_click():
    try:
        bullets_inserted = int(e1.get())
        if bullets_inserted < 1 or bullets_inserted > 5:
            raise ValueError("The number of bullets must be between 1 and 5.")
        result = pull_the_trigger(bullets_inserted)
        result_label.config(text=result)
    except ValueError as ve:
        messagebox.showerror("Invalid Input", str(ve))

root = tk.Tk()
root.title("Russian Roulette")
root.geometry("420x240")
root.configure(bg="#2b2b2b")

label = tk.Label(root, text="How many bullets do you have?", bg="#2b2b2b", fg="#ffffff", font=("Helvetica", 14))
label.pack(pady=10)

e1 = tk.Entry(root, font=("Helvetica", 12))
e1.pack(pady=5)
e1.insert(tk.END, str(random.randint(1, 5)))

button = tk.Button(root, text="Get Roulette", command=on_button_click, bg="#555555", fg="#ffffff", font=("Helvetica", 12))
button.pack(pady=10)

result_label = tk.Label(root, text="", bg="#2b2b2b", fg="#ffffff", font=("Helvetica", 14))
result_label.pack(pady=10)

root.mainloop()
