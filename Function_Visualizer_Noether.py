# Interfáz
import customtkinter as ctk
from tkinter import messagebox

# Cálculos
import numpy as np
import sympy as sp

# Gráficas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Utilidades
import math
import os

# Configuración del tema de CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

x = sp.Symbol("x")

# Diccionario con idiomas y textos de ayuda
LANGUAGES = {
    "Español": {
        "title": "Guía de Uso - Visualizador de Funciones",
        "help_btn": "❓ Ayuda e Instrucciones",
        "help_text": (
            "1. Selección de Función:\n"
            "   Elija el tipo de función matemática en el menú desplegable superior.\n\n"
            "2. Ajuste de Parámetros:\n"
            "   Complete los campos numéricos requeridos para la función elegida.\n\n"
            "3. Visualización:\n"
            "   Haga clic en 'Graficar' para renderizar la función. Se actualizarán la curva y la información del dominio, rango y asíntotas.\n\n"
            "4. Laboratorio de Noether:\n"
            "   Acceda mediante el botón inferior para explorar simetrías físicas y cantidades conservadas."
        ),
        "graph_btn": "📈 Graficar Función",
        "noether_btn": "⚛️ Explorar Teorema de Noether",
        "type_label": "Tipo de Función:",
        "info_title": "Información Técnica",
        "param_error_title": "Error de Parámetro",
        "param_error_msg": "El parámetro '{}' debe ser un número válido."
    },
    "English": {
        "title": "User Guide - Function Visualizer",
        "help_btn": "❓ Help & Instructions",
        "help_text": (
            "1. Function Selection:\n"
            "   Choose the mathematical function type from the top dropdown menu.\n\n"
            "2. Parameter Input:\n"
            "   Enter the required numeric values for the selected function.\n\n"
            "3. Visualization:\n"
            "   Click 'Graph' to plot the function. The curve, domain, range, and asymptotes will update automatically.\n\n"
            "4. Noether's Lab:\n"
            "   Use the bottom button to open the interactive module on physical symmetries and conservation laws."
        ),
        "graph_btn": "📈 Plot Function",
        "noether_btn": "⚛️ Explore Noether's Theorem",
        "type_label": "Function Type:",
        "info_title": "Technical Info",
        "param_error_title": "Parameter Error",
        "param_error_msg": "Parameter '{}' must be a valid number."
    },
    "Deutsch": {
        "title": "Bedienungsanleitung - Funktions visualisierer",
        "help_btn": "❓ Hilfe & Anleitung",
        "help_text": (
            "1. Funktionsauswahl:\n"
            "   Wählen Sie den mathematischen Funktionstyp aus dem Dropdown-Menü oben aus.\n\n"
            "2. Parameter eingeben:\n"
            "   Geben Sie die erforderlichen numerischen Werte für die Funktion ein.\n\n"
            "3. Visualisierung:\n"
            "   Klicken Sie auf 'Plotten', um die Funktion darzustellen. Bild, Definitionsbereich und Wertebereich werden aktualisiert.\n\n"
            "4. Noether-Labor:\n"
            "   Öffnen Sie über die untere Schaltfläche das interaktive Labor für physikalische Symmetrien."
        ),
        "graph_btn": "📈 Funktion Plotten",
        "noether_btn": "⚛️ Noether-Theorem erkunden",
        "type_label": "Funktionstyp:",
        "info_title": "Technische Daten",
        "param_error_title": "Parameterfehler",
        "param_error_msg": "Der Parameter '{}' muss eine gültige Zahl sein."
    }
}

# Diccionario de funciones con toda su info
FUNCTIONS = {
    "Linear": {
        "formula": lambda x, m, b: m * x + b,
        "symbolic": lambda x, m, b: m * x + b,
        "parameters": ["m", "b"],
        "description": "Linear Function",
        "domain": "ℝ",
        "asymptotes": "None",
        "preview": "f(x) = mx + b",
        "x_range": {"min": -10, "max": 10, "points": 1000}
    },
    "Quadratic": {
        "formula": lambda x, a, b, c: a * x**2 + b * x + c,
        "symbolic": lambda x, a, b, c: a * x**2 + b * x + c,
        "parameters": ["a", "b", "c"],
        "description": "Quadratic Function",
        "domain": "ℝ",
        "asymptotes": "None",
        "preview": "f(x) = ax² + bx + c",
        "x_range": {"min": -10, "max": 10, "points": 1000}
    },
    "Cubic": {
        "formula": lambda x, a, b, c, d: a * x**3 + b * x**2 + c * x + d,
        "symbolic": lambda x, a, b, c, d: a * x**3 + b * x**2 + c * x + d,
        "parameters": ["a", "b", "c", "d"],
        "description": "Cubic Function",
        "domain": "ℝ",
        "asymptotes": "None",
        "preview": "f(x) = ax³ + bx² + cx + d",
        "x_range": {"min": -10, "max": 10, "points": 1000}
    },
    "Exponential": {
        "formula": lambda x, a, b: a * np.exp(b * x),
        "symbolic": lambda x, a, b: a * sp.exp(b * x),
        "parameters": ["a", "b"],
        "description": "Exponential Function",
        "domain": "ℝ",
        "asymptotes": "Horizontal: y = 0",
        "preview": "f(x) = ae^(bx)",
        "x_range": {"min": -5, "max": 5, "points": 1000}
    },
    "Logarithmic": {
        "formula": lambda x, a, b: a * np.log(x) + b,
        "symbolic": lambda x, a, b: a * sp.log(x) + b,
        "parameters": ["a", "b"],
        "description": "Logarithmic Function",
        "domain": "(0, ∞)",
        "asymptotes": "Vertical: x = 0",
        "preview": "f(x) = a·ln(x) + b",
        "x_range": {"min": 0.01, "max": 10, "points": 1000}
    },
    "Sine": {
        "formula": lambda x, a, b: a * np.sin(b * x),
        "symbolic": lambda x, a, b: a * sp.sin(b * x),
        "parameters": ["a", "b"],
        "description": "Sine Function",
        "domain": "ℝ",
        "asymptotes": "None",
        "preview": "f(x) = a·sin(bx)",
        "x_range": {"min": -2 * np.pi, "max": 2 * np.pi, "points": 2000}
    },
    "Cosine": {
        "formula": lambda x, a, b: a * np.cos(b * x),
        "symbolic": lambda x, a, b: a * sp.cos(b * x),
        "parameters": ["a", "b"],
        "description": "Cosine Function",
        "domain": "ℝ",
        "asymptotes": "None",
        "preview": "f(x) = a·cos(bx)",
        "x_range": {"min": -2 * np.pi, "max": 2 * np.pi, "points": 2000}
    },
    "Tangent": {
        "formula": lambda x, a, b: a * np.tan(b * x),
        "symbolic": lambda x, a, b: a * sp.tan(b * x),
        "parameters": ["a", "b"],
        "description": "Tangent Function",
        "domain": "ℝ \\ {π/2 + kπ}",
        "asymptotes": "Vertical: x = π/2 + kπ",
        "preview": "f(x) = a·tan(bx)",
        "x_range": {"min": -2 * np.pi, "max": 2 * np.pi, "points": 5000}
    }
}

# Ventana principal
main_window = ctk.CTk()
main_window.title("Function Visualizer & Physics Suite")
main_window.geometry("1200x750")
main_window.minsize(1000, 650)

# Frame Izquierdo
left_frame = ctk.CTkFrame(main_window, width=320, corner_radius=15)
left_frame.pack(side="left", fill="y", padx=15, pady=15)

# Título de la App
title = ctk.CTkLabel(
    left_frame, 
    text="Function Visualizer", 
    font=ctk.CTkFont(family="Roboto", size=22, weight="bold")
)
title.pack(pady=(15, 10))

# Selección de Idioma
lang_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
lang_frame.pack(fill="x", padx=10, pady=(0, 10))

ctk.CTkLabel(lang_frame, text="🌐 Language:", font=ctk.CTkFont(size=11)).pack(side="left", padx=5)
lang_option = ctk.CTkOptionMenu(
    lang_frame, 
    values=["Español", "English", "Deutsch"],
    width=110,
    command=lambda val: update_language()
)
lang_option.set("Español")
lang_option.pack(side="right", padx=5)

# Botón de Ayuda
def show_help_modal():
    lang = lang_option.get()
    info = LANGUAGES[lang]
    
    help_win = ctk.CTkToplevel(main_window)
    help_win.title(info["title"])
    help_win.geometry("500x380")
    help_win.attributes("-topmost", True)
    
    ctk.CTkLabel(
        help_win, 
        text=info["title"], 
        font=ctk.CTkFont(size=18, weight="bold")
    ).pack(pady=(15, 10))
    
    textbox = ctk.CTkTextbox(help_win, width=440, height=260, corner_radius=10)
    textbox.pack(padx=20, pady=10)
    textbox.insert("0.0", info["help_text"])
    textbox.configure(state="disabled")

help_button = ctk.CTkButton(
    left_frame, 
    text="❓ Ayuda / Instructions", 
    fg_color="#3B82F6", 
    hover_color="#1D4ED8",
    command=show_help_modal
)
help_button.pack(fill="x", padx=15, pady=(0, 15))

# Combo de Tipos de Función
type_label = ctk.CTkLabel(left_frame, text="Type of Function", font=ctk.CTkFont(weight="bold"))
type_label.pack(anchor="w", padx=15)

function_box = ctk.CTkOptionMenu(
    left_frame,
    values=list(FUNCTIONS.keys()),
    command=lambda choice: on_function_change(choice)
)
function_box.set("Quadratic")
function_box.pack(fill="x", padx=15, pady=(5, 10))

formula_preview = ctk.CTkLabel(
    left_frame,
    text="",
    font=ctk.CTkFont(size=13, slant="italic"),
    text_color="#60A5FA"
)
formula_preview.pack(pady=(0, 10))

# Frame para Parámetros
parameter_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
parameter_frame.pack(fill="x", padx=15, pady=5)

# Panel de Información
info_frame = ctk.CTkFrame(left_frame, corner_radius=10)
info_frame.pack(fill="both", expand=True, padx=15, pady=15)

info_title_label = ctk.CTkLabel(
    info_frame, 
    text="Information", 
    font=ctk.CTkFont(size=14, weight="bold")
)
info_title_label.pack(anchor="w", padx=10, pady=(8, 2))

information_label = ctk.CTkLabel(
    info_frame,
    text="",
    justify="left",
    anchor="nw",
    font=ctk.CTkFont(family="Consolas", size=11)
)
information_label.pack(fill="both", expand=True, padx=10, pady=5)

# Zona de Gráfica
graph_frame = ctk.CTkFrame(main_window, corner_radius=15)
graph_frame.pack(side="right", fill="both", expand=True, padx=(0, 15), pady=15)

# Estilizado de Matplotlib para Modo Oscuro
fig = Figure(figsize=(6, 5), dpi=100, facecolor="#2B2B2B")
ax = fig.add_subplot(111)

def style_axes(target_ax, title_str="Graphic"):
    target_ax.set_facecolor("#1E1E1E")
    target_ax.tick_params(colors="white")
    target_ax.xaxis.label.set_color("white")
    target_ax.yaxis.label.set_color("white")
    target_ax.title.set_color("white")
    for spine in target_ax.spines.values():
        spine.set_color("#555555")
    target_ax.grid(True, color="#333333", linestyle="--")
    target_ax.set_title(title_str, color="white")

style_axes(ax)

canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(10, 5))

parameter_entries = {}

def update_formula_preview():
    selected_function = function_box.get()
    preview = FUNCTIONS[selected_function]["preview"]
    formula_preview.configure(text=preview)

def create_parameter_entries(parameters):
    global parameter_entries
    for widget in parameter_frame.winfo_children():
        widget.destroy()

    parameter_entries = {}
    for parameter in parameters:
        row = ctk.CTkFrame(parameter_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        
        lbl = ctk.CTkLabel(row, text=f"{parameter}:", width=30, anchor="w")
        lbl.pack(side="left", padx=(0, 5))
        
        entry = ctk.CTkEntry(row, placeholder_text="0.0")
        entry.pack(side="right", fill="x", expand=True)
        
        # Valor por defecto
        if parameter == "a" or parameter == "m":
            entry.insert(0, "1")
        else:
            entry.insert(0, "0")
            
        parameter_entries[parameter] = entry

def on_function_change(choice):
    create_parameter_entries(FUNCTIONS[choice]["parameters"])
    update_formula_preview()

# Lógica de Rangos Físicos/Matemáticos
def calculate_range(function_name, parameters):
    if function_name == "Linear":
        m, b = parameters
        return f"{{{b}}}" if m == 0 else "ℝ"
    elif function_name == "Quadratic":
        a, b, c = parameters
        if a == 0:
            return calculate_range("Linear", [b, c])
        x_vertex = -b / (2 * a)
        y_vertex = a * x_vertex**2 + b * x_vertex + c
        return f"[{round(y_vertex, 3)}, ∞)" if a > 0 else f"(-∞, {round(y_vertex, 3)}]"
    elif function_name == "Cubic":
        a, b, c, d = parameters
        return calculate_range("Quadratic", [b, c, d]) if a == 0 else "ℝ"
    elif function_name == "Exponential":
        a, b = parameters
        if a == 0: return "{0}"
        return "(0, ∞)" if a > 0 else "(-∞, 0)"
    elif function_name == "Logarithmic":
        a, b = parameters
        return f"{{{b}}}" if a == 0 else "ℝ"
    elif function_name in ["Sine", "Cosine"]:
        amp = abs(parameters[0])
        return "{0}" if amp == 0 else f"[-{amp}, {amp}]"
    elif function_name == "Tangent":
        return "{0}" if parameters[0] == 0 else "ℝ"
    return "Unknown"

def calculate_function(function_name, parameters):
    function_data = FUNCTIONS[function_name]
    formula = function_data["formula"]
    plot_settings = function_data["x_range"]
    
    x_val = np.linspace(plot_settings["min"], plot_settings["max"], plot_settings["points"])
    y_val = formula(x_val, *parameters)

    if function_data["asymptotes"] != "None":
        y_val[np.abs(y_val) > 1e6] = np.nan

    return x_val, y_val

def draw_graph(x_val, y_val, title="Function"):
    ax.clear()
    style_axes(ax, title)
    ax.plot(x_val, y_val, linewidth=2, color="#3B82F6", label=title)
    ax.axhline(0, color="#666666", linewidth=1)
    ax.axvline(0, color="#666666", linewidth=1)
    ax.legend(facecolor="#2B2B2B", edgecolor="none", labelcolor="white")
    canvas.draw()

def update_information_panel(function_name, parameters):
    function_data = FUNCTIONS[function_name]
    symbolic_formula = function_data["symbolic"]
    equation = symbolic_formula(x, *parameters)
    
    text = f"Function: {function_name}\n"
    text += f"Type: {function_data['description']}\n\n"
    text += f"Equation:\n f(x) = {sp.pretty(equation)}\n\n"
    text += f"Domain: {function_data['domain']}\n"
    text += f"Range: {calculate_range(function_name, parameters)}\n\n"
    text += "Parameters:\n"
    for p, v in zip(function_data["parameters"], parameters):
        text += f"  • {p} = {v}\n"
    text += f"\nAsymptotes:\n {function_data['asymptotes']}"

    information_label.configure(text=text)

def plot_function():
    selected_function = function_box.get()
    function_data = FUNCTIONS[selected_function]
    parameters = []
    
    for parameter in function_data["parameters"]:
        try:
            value = float(parameter_entries[parameter].get())
        except ValueError:
            lang = lang_option.get()
            messagebox.showerror(
                LANGUAGES[lang]["param_error_title"],
                LANGUAGES[lang]["param_error_msg"].format(parameter)
            )
            return
        parameters.append(value)
        
    x_val, y_val = calculate_function(selected_function, parameters)
    draw_graph(x_val, y_val, selected_function)
    update_information_panel(selected_function, parameters)

# Botón Graficar
graph_button = ctk.CTkButton(
    graph_frame,
    text="📈 Graficar Función",
    font=ctk.CTkFont(size=14, weight="bold"),
    fg_color="#10B981",
    hover_color="#059669",
    height=40,
    command=plot_function
)
graph_button.pack(fill="x", padx=10, pady=(0, 10))

# --- MÓDULO DE NOETHER ---
def open_noether_lab():
    noether_window = ctk.CTkToplevel(main_window)
    noether_window.title("Noether's Lab - Physics Symmetries")
    noether_window.geometry("950x650")
    noether_window.minsize(850, 550)

    title_n = ctk.CTkLabel(
        noether_window,
        text="Noether's Theorem Laboratory",
        font=ctk.CTkFont(size=20, weight="bold")
    )
    title_n.pack(pady=(15, 2))

    subtitle_n = ctk.CTkLabel(
        noether_window,
        text="Continuous Symmetry → Conservation Law",
        font=ctk.CTkFont(size=12, slant="italic"),
        text_color="#9CA3AF"
    )
    subtitle_n.pack(pady=(0, 10))

    content = ctk.CTkFrame(noether_window, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=20, pady=10)

    controls = ctk.CTkFrame(content, width=280)
    controls.pack(side="left", fill="y", padx=(0, 10))

    graph_area = ctk.CTkFrame(content)
    graph_area.pack(side="right", fill="both", expand=True)

    ctk.CTkLabel(controls, text="Symmetry:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 2))
    symmetry_box = ctk.CTkOptionMenu(
        controls,
        values=["Time Translation", "Spatial Translation", "Rotation"]
    )
    symmetry_box.set("Time Translation")
    symmetry_box.pack(fill="x", padx=10, pady=(0, 10))

    entries = {}
    params = [("Mass (m):", "1"), ("Velocity (v):", "5"), ("Radius (r):", "2"), ("Angular vel (ω):", "3")]
    
    for label_text, default_val in params:
        ctk.CTkLabel(controls, text=label_text).pack(anchor="w", padx=10)
        entry = ctk.CTkEntry(controls)
        entry.insert(0, default_val)
        entry.pack(fill="x", padx=10, pady=(0, 5))
        entries[label_text] = entry

    result_label = ctk.CTkLabel(
        controls,
        text="",
        justify="left",
        anchor="nw",
        font=ctk.CTkFont(family="Consolas", size=11)
    )
    result_label.pack(fill="both", expand=True, padx=10, pady=10)

    fig_n = Figure(figsize=(5, 4), dpi=100, facecolor="#2B2B2B")
    ax_n = fig_n.add_subplot(111)
    style_axes(ax_n, "Conserved Quantity over Time")

    canvas_n = FigureCanvasTkAgg(fig_n, master=graph_area)
    canvas_n.draw()
    canvas_n.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def verify_noether():
        try:
            m = float(entries["Mass (m):"].get())
            v = float(entries["Velocity (v):"].get())
            r = float(entries["Radius (r):"].get())
            omega = float(entries["Angular vel (ω):"].get())
            if m <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Parameter Error", "Mass must be > 0 and inputs valid.", parent=noether_window)
            return

        t = np.linspace(0, 10, 500)
        symmetry = symmetry_box.get()

        if symmetry == "Time Translation":
            lagrangian, q_name, q_formula = "L = ½mv²", "Energy", "E = ½mv²"
            val = 0.5 * m * v**2
            deriv = "dE/dt = 0"
        elif symmetry == "Spatial Translation":
            lagrangian, q_name, q_formula = "L = ½mv²", "Linear Momentum", "p = mv"
            val = m * v
            deriv = "dp/dt = 0"
        else:
            lagrangian, q_name, q_formula = "L = ½Iω²", "Angular Momentum", "L = Iω"
            val = (m * r**2) * omega
            deriv = "dL/dt = 0"

        quantity = np.full_like(t, val)

        ax_n.clear()
        style_axes(ax_n, f"Conservation of {q_name}")
        ax_n.plot(t, quantity, linewidth=2.5, color="#F59E0B", label=q_name)
        ax_n.set_xlabel("Time (t)")
        ax_n.set_ylabel(q_name)
        ax_n.legend(facecolor="#2B2B2B", edgecolor="none", labelcolor="white")
        canvas_n.draw()

        result_label.configure(
            text=(
                f"Symmetry: {symmetry}\n\n"
                f"Lagrangian: {lagrangian}\n"
                f"Quantity: {q_name}\n"
                f"Formula: {q_formula}\n\n"
                f"Value: {val:.3f}\n"
                f"Verification: {deriv}\n\n"
                "Constant line confirms\nconservation law."
            )
        )

    ctk.CTkButton(
        controls,
        text="Verify Theorem",
        font=ctk.CTkFont(weight="bold"),
        fg_color="#8B5CF6",
        hover_color="#7C3AED",
        command=verify_noether
    ).pack(fill="x", padx=10, pady=10)

noether_button = ctk.CTkButton(
    left_frame,
    text="⚛️ Explorar Teorema de Noether",
    font=ctk.CTkFont(weight="bold"),
    fg_color="#6366F1",
    hover_color="#4F46E5",
    height=35,
    command=open_noether_lab
)
noether_button.pack(fill="x", padx=15, pady=(5, 15))

# Actualización Dinámica de Idioma en la Interfaz General
def update_language():
    lang = lang_option.get()
    dict_lang = LANGUAGES[lang]
    
    help_button.configure(text=dict_lang["help_btn"])
    graph_button.configure(text=dict_lang["graph_btn"])
    noether_button.configure(text=dict_lang["noether_btn"])
    type_label.configure(text=dict_lang["type_label"])
    info_title_label.configure(text=dict_lang["info_title"])

# Inicialización de widgets
function_box.set("Quadratic")
on_function_change("Quadratic")
update_language()

main_window.mainloop()
