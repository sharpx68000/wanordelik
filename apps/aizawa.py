import colorsys
import math
import tkinter as tk

class AizawaVisualizer:
    def __init__(self, parent):
        self.root = parent
        self.root.winfo_toplevel().title("Wanordelik // Aizawa Attractor")

        self.width = 900
        self.height = 700
        self.canvas = tk.Canvas(parent, width=self.width, height=self.height, bg="#020205", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.control_panel = tk.Frame(parent, bg="#0d0d14", padx=12, pady=12)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y)

        self.a = 0.95
        self.b = 0.7
        self.c = 0.6
        self.d = 3.5
        self.e = 0.25
        self.f = 0.1

        self.x, self.y, self.z = 0.1, 0.0, 0.0
        self.dt = 0.01
        self.steps_per_frame = 8

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

        self.create_slider("Param A (Eje Z):", 0.5, 1.2, self.a, self.update_a)
        self.create_slider("Param B (Centro):", 0.3, 1.0, self.b, self.update_b)
        self.create_slider("Param D (Giro):", 1.0, 5.0, self.d, self.update_d)
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

    def update_a(self, val):
        if not self.auto_morph.get():
            self.a = float(val)

    def update_b(self, val):
        if not self.auto_morph.get():
            self.b = float(val)

    def update_d(self, val):
        if not self.auto_morph.get():
            self.d = float(val)

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
            self.a = 0.95 + 0.15 * math.sin(self.time_var * 0.3)
            self.d = 3.5 + 0.8 * math.cos(self.time_var * 0.2)

        scale = 160.0
        for _ in range(self.steps_per_frame):
            dx = ((self.z - self.b) * self.x - self.d * self.y) * self.dt
            dy = (self.d * self.x + (self.z - self.b) * self.y) * self.dt
            dz = (self.c + self.a * self.z - (self.z**3) / 3 - (self.x**2 + self.y**2) * (1 + self.e * self.z) + self.f * self.z * (self.x**3)) * self.dt

            self.x += dx
            self.y += dy
            self.z += dz

            rot = self.time_var * 0.25
            rx = self.x * math.cos(rot) - self.y * math.sin(rot)
            ry = self.x * math.sin(rot) + self.y * math.cos(rot)

            px = self.width / 2 + rx * scale
            py = self.height / 2 - (self.z - 0.5) * scale
            self.points.append((px, py, self.z))

        if len(self.points) > self.max_points:
            self.points = self.points[-self.max_points:]

        self.canvas.delete("all")
        total_pts = len(self.points)

        if total_pts > 1:
            for i in range(0, total_pts - 1, 2):
                x1, y1, z1 = self.points[i]
                x2, y2, _ = self.points[i + 1]

                hue = (0.05 + (z1 * 0.25) + (self.time_var * 0.03)) % 1.0
                alpha_factor = i / total_pts
                value = 0.3 + 0.7 * alpha_factor

                r, g, b = colorsys.hsv_to_rgb(hue, 0.9, value)
                color_hex = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
                line_width = 1.8 if i > total_pts - 300 else 1.0

                self.canvas.create_line(x1, y1, x2, y2, fill=color_hex, width=line_width)

        self.root.after(16, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = AizawaVisualizer(root)
    root.mainloop()