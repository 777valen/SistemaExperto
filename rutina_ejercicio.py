import collections.abc
import collections
collections.Mapping = collections.abc.Mapping

from experta import *
import tkinter as tk
from tkinter import messagebox


class SistemaExpertoEjercicio(KnowledgeEngine):
    @Rule(Fact(peso=MATCH.p & P(lambda p: p < 50)))
    def bajo_peso(self):
        self.declare(Fact(categoria="bajo peso"))

    @Rule(Fact(peso=MATCH.p & P(lambda p: 50 <= p <= 80)))
    def peso_normal(self):
        self.declare(Fact(categoria="peso normal"))

    @Rule(Fact(peso=MATCH.p & P(lambda p: 80 < p <= 100)))
    def sobrepeso(self):
        self.declare(Fact(categoria="sobrepeso"))

    @Rule(Fact(peso=MATCH.p & P(lambda p: p > 100)))
    def obesidad(self):
        self.declare(Fact(categoria="obesidad"))

    @Rule(Fact(categoria="bajo peso"))
    def rutina_bajo_peso(self):
        self.declare(Fact(rutina="Rutina de fuerza con pesas ligeras, ejercicios de resistencia y alimentación rica en proteínas."))

    @Rule(Fact(categoria="peso normal"))
    def rutina_peso_normal(self):
        self.declare(Fact(rutina="Rutina equilibrada con cardio moderado, fuerza y flexibilidad (yoga, pilates)."))

    @Rule(Fact(categoria="sobrepeso"))
    def rutina_sobrepeso(self):
        self.declare(Fact(rutina="Rutina de quema de grasa con caminatas rápidas, bicicleta estática y ejercicios de bajo impacto."))

    @Rule(Fact(categoria="obesidad"))
    def rutina_obesidad(self):
        self.declare(Fact(rutina="Rutina suave con caminatas, ejercicios de movilidad articular y respiración consciente."))

    @Rule(Fact(toma_azucar="si"))
    def azucar_rutina(self):
        self.declare(Fact(rutina="Incluye ejercicios cardiovasculares para mejorar la sensibilidad a la insulina."))

    @Rule(Fact(fuma="si"))
    def fumar_rutina(self):
        self.declare(Fact(rutina="Agrega ejercicios respiratorios y caminatas al aire libre para mejorar la capacidad pulmonar."))

    @Rule(Fact(ejercicio="no"))
    def sin_ejercicio(self):
        self.declare(Fact(rutina="Comienza con rutinas suaves: estiramientos, caminatas cortas y ejercicios de movilidad."))

    # Nuevas reglas basadas en hábitos
    @Rule(Fact(sueno="poco"))
    def rutina_sueno_poco(self):
        self.declare(Fact(rutina="Incluye ejercicios suaves y relajación para mejorar la calidad del sueño."))

    @Rule(Fact(sueno="mucho"))
    def rutina_sueno_mucho(self):
        self.declare(Fact(rutina="Rutina activa para mantener energía y evitar sedentarismo."))

    @Rule(Fact(agua="poca"))
    def rutina_agua_poca(self):
        self.declare(Fact(rutina="Incluye pausas para hidratación y ejercicios de baja intensidad."))

    @Rule(Fact(agua="mucha"))
    def rutina_agua_mucha(self):
        self.declare(Fact(rutina="Rutina intensa con cardio y fuerza, aprovechando buena hidratación."))

    @Rule(Fact(sueno="normal"), Fact(agua="normal"))
    def rutina_equilibrada(self):
        self.declare(Fact(rutina="Rutina equilibrada con cardio moderado, fuerza y estiramientos."))

    def ejecutar(self, peso, toma_azucar, fuma, ejercicio, sueno, agua):
        self.reset()
        self.declare(Fact(peso=peso))
        self.declare(Fact(toma_azucar=toma_azucar))
        self.declare(Fact(fuma=fuma))
        self.declare(Fact(ejercicio=ejercicio))
        self.declare(Fact(sueno=sueno))
        self.declare(Fact(agua=agua))
        self.run()
        return [fact["rutina"] for _, fact in self.facts.items() if "rutina" in fact]


def obtener_rutina():
    try:
        peso = int(entry_peso.get())
        toma_azucar = var_azucar.get()
        fuma = var_fuma.get()
        ejercicio = var_ejercicio.get()
        sueno = var_sueno.get()
        agua = var_agua.get()

        experto = SistemaExpertoEjercicio()
        rutinas = experto.ejecutar(peso, toma_azucar, fuma, ejercicio, sueno, agua)

        messagebox.showinfo("Rutina recomendada", "\n".join(rutinas))
    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese un peso válido (número entero).")


# Interfaz gráfica
root = tk.Tk()
root.title("Sistema Experto: Rutina de Ejercicio")
root.geometry("400x500")

tk.Label(root, text="Ingrese su peso (kg):").pack()
entry_peso = tk.Entry(root)
entry_peso.pack()

var_azucar = tk.StringVar(value="no")
tk.Label(root, text="¿Consume azúcar regularmente?").pack()
tk.Radiobutton(root, text="Sí", variable=var_azucar, value="si").pack()
tk.Radiobutton(root, text="No", variable=var_azucar, value="no").pack()

var_fuma = tk.StringVar(value="no")
tk.Label(root, text="¿Fuma?").pack()
tk.Radiobutton(root, text="Sí", variable=var_fuma, value="si").pack()
tk.Radiobutton(root, text="No", variable=var_fuma, value="no").pack()

var_ejercicio = tk.StringVar(value="si")
tk.Label(root, text="¿Hace ejercicio actualmente?").pack()
tk.Radiobutton(root, text="Sí", variable=var_ejercicio, value="si").pack()
tk.Radiobutton(root, text="No", variable=var_ejercicio, value="no").pack()

var_sueno = tk.StringVar(value="normal")
tk.Label(root, text="¿Cuántas horas duerme al día?").pack()
tk.Radiobutton(root, text="Menos de 6", variable=var_sueno, value="poco").pack()
tk.Radiobutton(root, text="Entre 6 y 8", variable=var_sueno, value="normal").pack()
tk.Radiobutton(root, text="Más de 8", variable=var_sueno, value="mucho").pack()

var_agua = tk.StringVar(value="normal")
tk.Label(root, text="¿Cuánta agua consume al día?").pack()
tk.Radiobutton(root, text="Menos de 1 litro", variable=var_agua, value="poca").pack()
tk.Radiobutton(root, text="Entre 1 y 2 litros", variable=var_agua, value="normal").pack()
tk.Radiobutton(root, text="Más de 2 litros", variable=var_agua, value="mucha").pack()

tk.Button(root, text="Obtener rutina", command=obtener_rutina).pack(pady=10)

root.mainloop()
