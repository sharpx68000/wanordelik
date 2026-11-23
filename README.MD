# WANORDELIK // ChaosLab Suite // Programa Básico de Física

`Wanordelik` es una suite interactiva de visualización de **dinámica caótica no lineal y física**, desarrollada en Python puro con Tkinter. El proyecto explora la belleza matemática de los atractores extraños y sistemas mecánicos complejos mediante renderizado de trayectorias en tiempo real, paletas de color neón/HSV y oscilación dinámica de parámetros (*Auto Morph*).

---

## Simulaciones Incluidas

1. **Atractor de Lorenz:** El sistema caótico de convección atmosférica clásico en forma de mariposa.
2. **Atractor de Rössler:** Estructura en espiral con giros verticales y plegado de fase.
3. **Atractor de Aizawa:** Geometría de flujo esférico con vórtice axial.
4. **Atractor de Thomas:** Malla tridimensional cíclica con simetría de disipación.
5. **Atractor de Halvorsen:** Anillos caóticos entrelazados alrededor de un eje central.
6. **Péndulo Doble:** Simulación física mediante ecuaciones de Euler-Lagrange.

---

## Características

* **Cero dependencias externas:** Corre sobre la librería estándar de Python (`tkinter`, `math`, `colorsys`).
* **Modo Tiempo Real (Auto Morph):** Oscilación automática de parámetros mediante funciones senoidales para generación de arte dinámico.
* **Renderizado Neon / CRT:** Colores HSB con atenuación progresiva de líneas según la posición y la profundidad.
* **Arquitectura Modular:** Lanzador principal (`main.py`) con barra lateral de navegación para intercalar módulos dinámicamente sin fugas de memoria.

---

## Estructura del Proyecto

```text
wanordelik/
├── main.py              # Lanzador principal con interfaz de navegación
├── README.md            # Documentación del proyecto
└── apps/                # Módulos de simulación independientes
    ├── __init__.py
    ├── lorenz.py
    ├── roessler.py
    ├── aizawa.py
    ├── thomas.py
    ├── halvorsen.py
    └── double_pendulum.py