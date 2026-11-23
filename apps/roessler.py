import colorsys
import math
import tkinter as tk

class RoesslerVisualizer:
    def __init__(self, parent):
        self.root = parent
        self.root.winfo_toplevel().title("Wanordelik // Rössler Attractor")

        self.width, self.height = 900, 700
        self.canvas = tk.Canvas(
            parent, width=self.width, height=self.height, bg="#020205", highlightthickness=0
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.control_panel = tk.Frame(parent, bg="#0d0d14", padx=12, pady=12)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y)

        self.a = 0.2
        self.b = 0.2
        self.c = 5.7

        self.x, self.y, self.z = 0.1, 0.0, 0.0
        self.dt = 0.02
        self.steps_per_frame = 10

        self.points = []
        self.max_points = 6000
        self.time_var = 0.0
        self.auto_morph = tk.BooleanVar(value=True)

        chk_auto = tk.Checkbutton(
            self.control_panel, text="Modo Tiempo Real (Morph)", variable=self.auto_morph,
            bg="#0d0d14", fg="#00ffcc", selectcolor="#1b1b26", activebackground="#0d0d14",
            activeforeground="#00ffcc", font=("Courier", 10, "bold")
        )
        chk_auto.pack(anchor="w", pady=(0, 10))

        self.create_slider("Parámetro A:", 0.1, 0.5, self.a, self.update_a, res=0.01)
        self.create_slider("Parámetro B:", 0.1, 0.5, self.b, self.update_b, res=0.01)
        self.create_slider("Parámetro C (Caos):", 1.0, 15.0, self.c, self.update_c, res=0.1)
        self.create_slider("Densidad (Líneas):", 1000, 12000, self.max_points, self.update_max_points, res=500)

        btn_reset = tk.Button(
            self.control_panel, text="Reiniciar Sistema", command=self.reset_system,
            bg="#1b1b26", fg="#00ffcc", activebackground="#00ffcc", activeforeground="#000000",
            font=("Courier", 10, "bold")
        )
        btn_reset.pack(fill=tk.X, pady=15)

        self.animate()

    def create_slider(self, label_text, from_, to, default, callback, res=0.1):
        lbl = tk.Label(self.control_panel, text=label_text, bg="#0d0d14", fg="#00ffcc", font=("Courier", 9, "bold"))
        lbl.pack(anchor="w", pady=(8, 0))

        slider = tk.Scale(
            self.control_panel, from_=from_, to=to, resolution=res, orient=tk.HORIZONTAL,
            bg="#0d0d14", fg="#ffffff", highlightthickness=0, troughcolor="#1b1b26", command=callback
        )
        slider.set(default)
        slider.pack(fill=tk.X, pady=(0, 5))
        return slider

    def update_a(self, val):
        if not self.auto_morph.get():
            self.a = float(val)

    def update_b(self, val):
        if not self.auto_morph.get():
            self.b = float(val)

    def update_c(self, val):
        if not self.auto_morph.get():
            self.c = float(val)

    def update_max_points(self, val):
        self.max_points = int(val)

    def reset_system(self):
        self.x, self.y, self.z = 0.1, 0.0, 0.0
        self.time_var = 0.0
        self.points.clear()
        if self.canvas.winfo_exists():
            self.canvas.delete("all")

    def animate(self):
        if not self.canvas.winfo_exists():
            return

        if self.auto_morph.get():
            self.time_var += 0.01
            self.c = 5.7 + 4.0 * math.sin(self.time_var * 0.4)

        scale = 18.0
        for _ in range(self.steps_per_frame):
            dx = (-self.y - self.z) * self.dt
            dy = (self.x + self.a * self.y) * self.dt
            dz = (self.b + self.z * (self.x - self.c)) * self.dt

            self.x += dx
            self.y += dy
            self.z += dz

            px = self.width / 2 + self.x * scale
            py = self.height / 2 + self.y * scale - 50
            self.points.append((px, py, self.z))

        if len(self.points) > self.max_points:
            self.points = self.points[-self.max_points:]

        self.canvas.delete("all")
        total_points = len(self.points)

        for i in range(0, total_points - 1, 2):
            x1, y1, z1 = self.points[i]
            x2, y2, _ = self.points[i + 1]

            hue = (0.8 + z1 / 30.0 + self.time_var * 0.05) % 1.0
            r, g, b = colorsys.hsv_to_rgb(hue, 0.95, i / total_points)
            color = f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=1.5)

        self.root.after(16, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    RoesslerVisualizer(root)
    root.mainloop()