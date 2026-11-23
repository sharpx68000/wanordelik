import os
import sys
import tkinter as tk

from apps.lorenz import ChaosVisualizer as LorenzVisualizer
from apps.roessler import RoesslerVisualizer
from apps.aizawa import AizawaVisualizer
from apps.thomas import ThomasVisualizer
from apps.halvorsen import HalvorsenVisualizer
from apps.double_pendulum import DoublePendulumVisualizer

class WanordelikApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wanordelik // ChaosLab Suite")
        self.root.geometry("1150x720")
        self.root.configure(bg="#020205")

        # Sidebar (Menú Izquierdo)
        self.sidebar = tk.Frame(root, bg="#0d0d14", width=250, padx=10, pady=15)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Viewport (Área de Renderizado Derecha)
        self.viewport = tk.Frame(root, bg="#020205")
        self.viewport.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        lbl_title = tk.Label(self.sidebar, text="WANORDELIK", bg="#0d0d14", fg="#00ffcc", font=("Courier", 18, "bold"))
        lbl_title.pack(pady=(10, 2))

        lbl_sub = tk.Label(self.sidebar, text="Chaos Suite v1.0", bg="#0d0d14", fg="#8888aa", font=("Courier", 8))
        lbl_sub.pack(pady=(0, 20))

        self.simulations = [
            ("Atractor de Lorenz", LorenzVisualizer),
            ("Atractor de Rössler", RoesslerVisualizer),
            ("Atractor de Aizawa", AizawaVisualizer),
            ("Atractor de Thomas", ThomasVisualizer),
            ("Atractor de Halvorsen", HalvorsenVisualizer),
            ("Péndulo Doble", DoublePendulumVisualizer),
        ]

        # Creación de botones corregida (padx=10 en lugar de px=10)
        for title, sim_class in self.simulations:
            btn = tk.Button(
                self.sidebar, text=title, command=lambda c=sim_class: self.load_simulation(c),
                bg="#1b1b26", fg="#ffffff", activebackground="#00ffcc", activeforeground="#000000",
                font=("Courier", 10, "bold"), bd=0, pady=8, anchor="w", padx=10
            )
            btn.pack(fill=tk.X, pady=4)

        self.active_frame = None
        self.load_simulation(self.simulations[0][1])  # Cargar la primera simulación por defecto

    def load_simulation(self, sim_class):
        if self.active_frame is not None:
            self.active_frame.destroy()

        self.active_frame = tk.Frame(self.viewport, bg="#020205")
        self.active_frame.pack(fill=tk.BOTH, expand=True)

        sim_class(self.active_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = WanordelikApp(root)
    root.mainloop()