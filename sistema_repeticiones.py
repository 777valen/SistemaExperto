import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Definir variables de entrada
fuerza = ctrl.Antecedent(np.arange(0, 101, 1), 'fuerza')
peso = ctrl.Antecedent(np.arange(0, 51, 1), 'peso')

# Variable de salida
repeticiones = ctrl.Consequent(np.arange(0, 31, 1), 'repeticiones')

# Conjuntos difusos para fuerza
fuerza['baja'] = fuzz.trimf(fuerza.universe, [0, 20, 40])
fuerza['media'] = fuzz.trimf(fuerza.universe, [30, 50, 70])
fuerza['alta'] = fuzz.trimf(fuerza.universe, [60, 80, 100])

# Conjuntos difusos para peso
peso['ligero'] = fuzz.trimf(peso.universe, [0, 10, 20])
peso['medio'] = fuzz.trimf(peso.universe, [15, 25, 35])
peso['pesado'] = fuzz.trimf(peso.universe, [30, 40, 50])

# Conjuntos difusos para repeticiones
repeticiones['pocas'] = fuzz.trimf(repeticiones.universe, [0, 5, 10])
repeticiones['moderadas'] = fuzz.trimf(repeticiones.universe, [10, 15, 20])
repeticiones['muchas'] = fuzz.trimf(repeticiones.universe, [20, 25, 30])

# Reglas difusas
regla1 = ctrl.Rule(fuerza['alta'] & peso['ligero'], repeticiones['muchas'])
regla2 = ctrl.Rule(fuerza['media'] & peso['medio'], repeticiones['moderadas'])
regla3 = ctrl.Rule(fuerza['baja'] & peso['pesado'], repeticiones['pocas'])
regla4 = ctrl.Rule(fuerza['alta'] & peso['pesado'], repeticiones['moderadas'])
regla5 = ctrl.Rule(fuerza['baja'] & peso['ligero'], repeticiones['moderadas'])
regla6 = ctrl.Rule(fuerza['media'] | peso['medio'], repeticiones['moderadas'])
regla7 = ctrl.Rule(fuerza['media'] & peso['ligero'], repeticiones['muchas'])
regla8 = ctrl.Rule(fuerza['media'] & peso['pesado'], repeticiones['pocas'])

# Crear sistema de control
sistema_ctrl = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5, regla6, regla7, regla8])

# Función para calcular repeticiones y mostrar resultado y gráfica en el mismo recuadro
def calcular_repeticiones():
    try:
        fuerza_val = float(entry_fuerza.get())
        peso_val = float(entry_peso.get())

        if not (0 <= fuerza_val <= 100):
            raise ValueError("Fuerza fuera de rango (0-100)")
        if not (0 <= peso_val <= 50):
            raise ValueError("Peso fuera de rango (0-50)")

        simulacion = ctrl.ControlSystemSimulation(sistema_ctrl)
        simulacion.input['fuerza'] = fuerza_val
        simulacion.input['peso'] = peso_val
        simulacion.compute()

        resultado = simulacion.output['repeticiones']
        resultado_label.config(text=f"Repeticiones sugeridas: {resultado:.2f}")

        # Limpiar gráfica anterior si existe
        for widget in frame_resultado.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.get_tk_widget().destroy()

        # Crear nueva gráfica
        fig, ax = plt.subplots(figsize=(5, 3))
        repeticiones.view(sim=simulacion, ax=ax)
        canvas = FigureCanvasTkAgg(fig, master=frame_resultado)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=2)

    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except KeyError:
        messagebox.showerror("Error", "No se pudo calcular las repeticiones. Verifica los valores ingresados.")

# Interfaz gráfica
root = tk.Tk()
root.title("Sistema Difuso: Repeticiones de Ejercicio")

tk.Label(root, text="Nivel de fuerza (0-100):").grid(row=0, column=0)
tk.Label(root, text="Peso mancuernas (kg, 0-50):").grid(row=1, column=0)

entry_fuerza = tk.Entry(root)
entry_peso = tk.Entry(root)

entry_fuerza.grid(row=0, column=1)
entry_peso.grid(row=1, column=1)

tk.Button(root, text="Calcular Repeticiones", command=calcular_repeticiones).grid(row=2, column=0, columnspan=2)

frame_resultado = tk.Frame(root)
frame_resultado.grid(row=3, column=0, columnspan=2)
resultado_label = tk.Label(frame_resultado, text="")
resultado_label.grid(row=0, column=0, columnspan=2)

root.mainloop()