import colorsys
import math
import tkinter as tk

class ThomasVisualizer:
    def __init__(self, parent):
        self.root = parent
        self.root.winfo_toplevel().title("Wanordelik // Thomas Cyclical Attractor")

        self.width = 900
        self.height = 700
        self.canvas = tk.Canvas(parent, width=self.width, height=self.height, bg="#020205", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.control_panel = tk.Frame(parent, bg="#0d0d14", padx=12, pady=12)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y)

        self.b = 0.20815

        self.x, self.y, self.z = 0.1, 0.0, 0.0
        self.dt = 0.04
        self.steps_per_frame = 12

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

        self.create_slider("Param B (Disipación):", 0.05, 0.35, self.b, self.update_b, res=0.005)
        self.create_slider("Densidad (Líneas):", 1000, 12000, self.max_points, self.update_max_points, res=500)

        btn_reset = tk.Button(
            self.control_panel, text="Reiniciar Sistema", command=self.reset_system,
            bg="#1b1b26", fg="#00ffcc", activebackground="#00ffcc", activeforeground="#000000",
            font=("Courier", 10, "bold")
        )
        btn_reset.pack(fill=tk.X, pady=15)

        self.animate()

    def create_slider(self, label_text, from_, to, default, callback, res=0.01):
        lbl = tk.Label(self.control_panel, text=label_text, bg="#0d0d14", fg="#00ffcc", font=("Courier", 9, "bold"))
        lbl.pack(anchor="w", pady=(8, 0))
        slider = tk.Scale(
            self.control_panel, from_=from_, to=to, resolution=res, orient=tk.HORIZONTAL,
            bg="#0d0d14", fg="#ffffff", highlightthickness=0, troughcolor="#1b1b26", command=callback
        )
        slider.set(default)
        slider.pack(fill=tk.X, pady=(0, 5))
        return slider

    def update_b(self, val):
        if not self.auto_morph.get():
            self.b = float(val)

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
            self.time_var += 0.008
            self.b = 0.20815 + 0.05 * math.sin(self.time_var * 0.3)

        scale = 75.0
        for _ in range(self.steps_per_frame):
            dx = (math.sin(self.y) - self.b * self.x) * self.dt
            dy = (math.sin(self.z) - self.b * self.y) * self.dt
            dz = (math.sin(self.x) - self.b * self.z) * self.dt

            self.x += dx
            self.y += dy
            self.z += dz

            rot = self.time_var * 0.2
            rx = self.x * math.cos(rot) - self.y * math.sin(rot)
            ry = self.x * math.sin(rot) + self.y * math.cos(rot)

            px = self.width / 2 + rx * scale
            py = self.height / 2 + (ry * 0.5 - self.z * 0.8) * scale
            self.points.append((px, py, self.z))

        if len(self.points) > self.max_points:
            self.points = self.points[-self.max_points:]

        self.canvas.delete("all")
        total_pts = len(self.points)

        if total_pts > 1:
            for i in range(0, total_pts - 1, 2):
                x1, y1, z1 = self.points[i]
                x2, y2, _ = self.points[i + 1]

                hue = (0.55 + (z1 / 10.0) + (self.time_var * 0.04)) % 1.0
                alpha_factor = i / total_pts
                value = 0.3 + 0.7 * alpha_factor

                r, g, b = colorsys.hsv_to_rgb(hue, 0.9, value)
                color_hex = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
                line_width = 1.8 if i > total_pts - 300 else 1.0

                self.canvas.create_line(x1, y1, x2, y2, fill=color_hex, width=line_width)

        self.root.after(16, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = ThomasVisualizer(root)
    root.mainloop()