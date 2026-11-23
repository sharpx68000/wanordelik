import colorsys
import math
import tkinter as tk

class DoublePendulumVisualizer:
    def __init__(self, parent):
        self.root = parent
        self.root.winfo_toplevel().title("Wanordelik // Double Pendulum Simulation")

        self.width = 900
        self.height = 700
        self.canvas = tk.Canvas(parent, width=self.width, height=self.height, bg="#020205", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.control_panel = tk.Frame(parent, bg="#0d0d14", padx=12, pady=12)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y)

        self.r1 = 180.0
        self.r2 = 180.0
        self.m1 = 20.0
        self.m2 = 20.0
        self.g = 9.81

        self.a1 = math.pi / 2
        self.a2 = math.pi / 2
        self.a1_v = 0.0
        self.a2_v = 0.0

        self.trace = []
        self.max_trace = 3000
        self.dt = 0.2
        self.time_var = 0.0
        self.auto_morph = tk.BooleanVar(value=False)

        chk_auto = tk.Checkbutton(
            self.control_panel, text="Variar Masa M2 (Morph)", variable=self.auto_morph,
            bg="#0d0d14", fg="#00ffcc", selectcolor="#1b1b26", activebackground="#0d0d14",
            activeforeground="#00ffcc", font=("Courier", 10, "bold")
        )
        chk_auto.pack(anchor="w", pady=(0, 10))

        self.create_slider("Masa 1 (m1):", 5.0, 50.0, self.m1, self.update_m1)
        self.create_slider("Masa 2 (m2):", 5.0, 50.0, self.m2, self.update_m2)
        self.create_slider("Longitud 1 (r1):", 80.0, 250.0, self.r1, self.update_r1)
        self.create_slider("Longitud 2 (r2):", 80.0, 250.0, self.r2, self.update_r2)
        self.create_slider("Rastro (Líneas):", 500, 6000, self.max_trace, self.update_max_trace, res=250)

        btn_reset = tk.Button(
            self.control_panel, text="Soltar Péndulo", command=self.reset_system,
            bg="#1b1b26", fg="#00ffcc", activebackground="#00ffcc", activeforeground="#000000",
            font=("Courier", 10, "bold")
        )
        btn_reset.pack(fill=tk.X, pady=15)

        self.animate()

    def create_slider(self, label_text, from_, to, default, callback, res=1.0):
        lbl = tk.Label(self.control_panel, text=label_text, bg="#0d0d14", fg="#00ffcc", font=("Courier", 9, "bold"))
        lbl.pack(anchor="w", pady=(6, 0))
        slider = tk.Scale(
            self.control_panel, from_=from_, to=to, resolution=res, orient=tk.HORIZONTAL,
            bg="#0d0d14", fg="#ffffff", highlightthickness=0, troughcolor="#1b1b26", command=callback
        )
        slider.set(default)
        slider.pack(fill=tk.X, pady=(0, 4))
        return slider

    def update_m1(self, val):
        self.m1 = float(val)

    def update_m2(self, val):
        if not self.auto_morph.get():
            self.m2 = float(val)

    def update_r1(self, val):
        self.r1 = float(val)

    def update_r2(self, val):
        self.r2 = float(val)

    def update_max_trace(self, val):
        self.max_trace = int(val)

    def reset_system(self):
        self.a1 = math.pi / 2
        self.a2 = math.pi / 2
        self.a1_v = 0.0
        self.a2_v = 0.0
        self.trace.clear()
        if self.canvas.winfo_exists():
            self.canvas.delete("all")

    def animate(self):
        if not self.canvas.winfo_exists():
            return

        if self.auto_morph.get():
            self.time_var += 0.01
            self.m2 = 20.0 + 15.0 * math.sin(self.time_var * 0.5)

        num1 = -self.g * (2 * self.m1 + self.m2) * math.sin(self.a1)
        num2 = -self.m2 * self.g * math.sin(self.a1 - 2 * self.a2)
        num3 = -2 * math.sin(self.a1 - self.a2) * self.m2 * (self.a2_v**2 * self.r2 + self.a1_v**2 * self.r1 * math.cos(self.a1 - self.a2))
        den1 = self.r1 * (2 * self.m1 + self.m2 - self.m2 * math.cos(2 * self.a1 - 2 * self.a2))
        a1_a = (num1 + num2 + num3) / den1

        num4 = 2 * math.sin(self.a1 - self.a2) * (self.a1_v**2 * self.r1 * (self.m1 + self.m2) + self.g * (self.m1 + self.m2) * math.cos(self.a1) + self.a2_v**2 * self.r2 * self.m2 * math.cos(self.a1 - self.a2))
        den2 = self.r2 * (2 * self.m1 + self.m2 - self.m2 * math.cos(2 * self.a1 - 2 * self.a2))
        a2_a = num4 / den2

        self.a1_v += a1_a * self.dt
        self.a2_v += a2_a * self.dt
        self.a1 += self.a1_v * self.dt
        self.a2 += self.a2_v * self.dt

        x0, y0 = self.width / 2, self.height / 3
        x1 = x0 + self.r1 * math.sin(self.a1)
        y1 = y0 + self.r1 * math.cos(self.a1)
        x2 = x1 + self.r2 * math.sin(self.a2)
        y2 = y1 + self.r2 * math.cos(self.a2)

        self.trace.append((x2, y2))
        if len(self.trace) > self.max_trace:
            self.trace.pop(0)

        self.canvas.delete("all")

        total_pts = len(self.trace)
        if total_pts > 1:
            for i in range(total_pts - 1):
                tx1, ty1 = self.trace[i]
                tx2, ty2 = self.trace[i + 1]
                hue = (i / total_pts * 0.85) % 1.0
                r, g, b = colorsys.hsv_to_rgb(hue, 1.0, i / total_pts)
                color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
                self.canvas.create_line(tx1, ty1, tx2, ty2, fill=color, width=1.5)

        self.canvas.create_line(x0, y0, x1, y1, fill="#ffffff", width=2)
        self.canvas.create_line(x1, y1, x2, y2, fill="#ffffff", width=2)
        self.canvas.create_oval(x1-6, y1-6, x1+6, y1+6, fill="#00ffcc", outline="")
        self.canvas.create_oval(x2-8, y2-8, x2+8, y2+8, fill="#ff0055", outline="")

        self.root.after(16, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = DoublePendulumVisualizer(root)
    root.mainloop()