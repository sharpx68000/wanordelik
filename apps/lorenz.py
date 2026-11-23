import colorsys
import math
import tkinter as tk

class ChaosVisualizer:
    def __init__(self, parent):
        self.root = parent
        self.width = 900
        self.height = 700
        self.canvas = tk.Canvas(parent, width=self.width, height=self.height, bg="#020205", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.control_panel = tk.Frame(parent, bg="#0d0d14", padx=12, pady=12)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y)

        self.sigma = 10.0
        self.rho = 28.0
        self.beta = 8.0 / 3.0

        self.x, self.y, self.z = 0.1, 0.0, 0.0
        self.dt = 0.005
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

        self.create_slider("Rho (Caos):", 1.0, 60.0, self.rho, self.update_rho)
        self.create_slider("Sigma (Viscosidad):", 1.0, 30.0, self.sigma, self.update_sigma)
        self.create_slider("Densidad (Líneas):", 1000, 12000, self.max_points, self.update_max_points, res=500)

        btn_reset = tk.Button(
            self.control_panel, text="Reiniciar Sistema", command=self.reset_system,
            bg="#1b1b26", fg="#00ffcc", activebackground="#00ffcc", activeforeground="#000000",
            font=("Courier", 10, "bold")
        )
        btn_reset.pack(fill=tk.X, pady=15)

        self.update_title()
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

    def update_rho(self, val):
        if not self.auto_morph.get():
            self.rho = float(val)

    def update_sigma(self, val):
        if not self.auto_morph.get():
            self.sigma = float(val)

    def update_max_points(self, val):
        self.max_points = int(val)

    def update_title(self):
        if not self.canvas.winfo_exists():
            return
        mode = "Auto Morph" if self.auto_morph.get() else "Manual"
        self.root.winfo_toplevel().title(
            f"Wanordelik // Lorenz Attractor [{mode}] Rho {self.rho:.1f} Sigma {self.sigma:.1f}"
        )

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
            self.rho = 28.0 + 18.0 * math.sin(self.time_var * 0.5)
            self.sigma = 10.0 + 4.0 * math.cos(self.time_var * 0.3)

        self.update_title()

        scale = 11.0
        for _ in range(self.steps_per_frame):
            dx = self.sigma * (self.y - self.x) * self.dt
            dy = (self.x * (self.rho - self.z) - self.y) * self.dt
            dz = (self.x * self.y - self.beta * self.z) * self.dt

            self.x += dx
            self.y += dy
            self.z += dz

            rot_angle = self.time_var * 0.2
            rx = self.x * math.cos(rot_angle) - self.y * math.sin(rot_angle)
            ry = self.x * math.sin(rot_angle) + self.y * math.cos(rot_angle)

            px = self.width / 2 + (rx * 0.86 - ry * 0.5) * scale
            py = self.height / 2 + (rx * 0.2 + ry * 0.3 - self.z * 0.8) * scale + 150

            self.points.append((px, py, self.z))

        if len(self.points) > self.max_points:
            self.points = self.points[-self.max_points:]

        self.canvas.delete("all")
        total_pts = len(self.points)
        
        if total_pts > 1:
            for i in range(0, total_pts - 1, 2):
                x1, y1, z1 = self.points[i]
                x2, y2, _ = self.points[i + 1]

                hue = ((i / 400.0) + (z1 / 60.0) + (self.time_var * 0.1)) % 1.0
                alpha_factor = i / total_pts
                value = 0.3 + 0.7 * alpha_factor

                r, g, b = colorsys.hsv_to_rgb(hue, 0.9, value)
                color_hex = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
                line_width = 1.8 if i > total_pts - 300 else 1.0

                self.canvas.create_line(x1, y1, x2, y2, fill=color_hex, width=line_width)

        self.root.after(16, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChaosVisualizer(root)
    root.mainloop()