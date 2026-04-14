import tkinter as tk
from tkinter import ttk

from models.drowsiness_model import start_drowsiness
from models.sign_model import start_sign
from models.hazard_model import start_hazard

def start_gui():
    root = tk.Tk()
    root.title("Driver AI System")
    root.geometry("1500x600")

    
    v1 = tk.Label(root,  width=480, height=360)
    v2 = tk.Label(root,  width=480, height=360)
    v3 = tk.Label(root,  width=480, height=360)


    v1.grid(row=0, column=0)
    v2.grid(row=0, column=1)
    v3.grid(row=0, column=2)

    start_drowsiness(v1)
    start_sign(v2)
    start_hazard(v3)

    root.mainloop()