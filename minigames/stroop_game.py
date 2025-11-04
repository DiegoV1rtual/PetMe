import tkinter as tk
import random

class StroopGame:
    """Efecto Stroop COMPLEJO: Palabra en color + Opciones en colores diferentes"""
    
    def __init__(self, callback):
        self.callback = callback
        self.rounds = 10
        self.current_round = 0
        self.correct_count = 0
        self.game_closed = False
        self.answer_given = False
        
        # Colores con contraste
        self.colors = {
            "ROJO": "#CC0000",
            "AZUL": "#0044CC",
            "VERDE": "#00AA00",
            "AMARILLO": "#CCAA00",
            "MORADO": "#6600AA",
            "NARANJA": "#CC5500"
        }
        
        self.color_names = list(self.colors.keys())
        
        # VENTANA FLOTANTE
        self.window = tk.Toplevel()
        self.window.title("")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        
        self.window.configure(bg="#1a1a1a")
        
        self.canvas = tk.Canvas(self.window, bg="#1a1a1a", 
                               highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # GEOMETRÍA después de pack
        w, h = 700, 500
        self.window.geometry(f"{w}x{h}")
        self.window.update_idletasks()
        self.window.update()
        
        # CENTRAR
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        self.window.geometry(f"+{x}+{y}")
        
        # Arrastrable
        self.canvas.bind("<Button-1>", self._start_drag)
        self.canvas.bind("<B1-Motion>", self._drag)
        
        self.widgets = []
    
    def _start_drag(self, event):
        self._drag_data = {"x": event.x, "y": event.y}
    
    def _drag(self, event):
        if hasattr(self, '_drag_data'):
            x = self.window.winfo_x() + event.x - self._drag_data["x"]
            y = self.window.winfo_y() + event.y - self._drag_data["y"]
            self.window.geometry(f"+{x}+{y}")
    
    def run(self):
        self.window.after(100, self._show_instructions)
    
    def _show_instructions(self):
        """INSTRUCCIONES CENTRADAS"""
        self._clear_widgets()
        
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        cx, cy = w // 2, h // 2
        
        # Título
        self.widgets.append(self.canvas.create_text(
            cx, cy - 180,
            text="EFECTO STROOP",
            font=("Arial", 28, "bold"),
            fill="white"))
        
        # Instrucciones CENTRADAS
        inst_text = """REGLAS DEL JUEGO:

1. Aparecera una PALABRA (ej: VERDE)
2. La palabra estara escrita en un COLOR diferente (ej: rojo)
3. Debes elegir el COLOR DE LA TINTA, NO lo que dice

OPCIONES:
- Son palabras de colores
- Cada opcion esta en color diferente al que dice
- Ejemplo: "ROJO" escrito en azul

OBJETIVO: Identifica el COLOR de la palabra principal
TIEMPO: 6 segundos por pregunta"""
        
        self.widgets.append(self.canvas.create_text(
            cx, cy - 30,
            text=inst_text,
            font=("Arial", 12),
            fill="yellow",
            justify="center"))
        
        # Botón
        rect = self.canvas.create_rectangle(
            cx - 100, cy + 140, cx + 100, cy + 190,
            fill="#4CAF50", outline="white", width=3)
        self.widgets.append(rect)
        
        text = self.canvas.create_text(
            cx, cy + 165,
            text="COMENZAR",
            font=("Arial", 16, "bold"),
            fill="white")
        self.widgets.append(text)
        
        self.canvas.tag_bind(rect, "<Button-1>", lambda e: self._next_round())
        self.canvas.tag_bind(text, "<Button-1>", lambda e: self._next_round())
    
    def _next_round(self):
        """Ronda con TIMER"""
        if self.game_closed or self.current_round >= self.rounds:
            self._finish_game()
            return
        
        self._clear_widgets()
        self.answer_given = False
        
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        cx, cy = w // 2, h // 2
        
        # Contador
        self.widgets.append(self.canvas.create_text(
            cx, 40,
            text=f"Ronda {self.current_round + 1} / {self.rounds}",
            font=("Arial", 18, "bold"),
            fill="white"))
        
        # Timer
        self.timer_label = self.canvas.create_text(
            cx, 80,
            text="Tiempo: 6s",
            font=("Arial", 14, "bold"),
            fill="#FFD700")
        self.widgets.append(self.timer_label)
        
        # PALABRA: texto != color
        word = random.choice(self.color_names)
        text_color_name = random.choice([c for c in self.color_names if c != word])
        text_color = self.colors[text_color_name]
        
        self.widgets.append(self.canvas.create_text(
            cx, cy - 80,
            text=word,
            font=("Arial", 56, "bold"),
            fill=text_color))
        
        # Instrucción
        self.widgets.append(self.canvas.create_text(
            cx, cy - 20,
            text="De que COLOR es el texto?",
            font=("Arial", 14),
            fill="white"))
        
        # OPCIONES: Palabras en colores diferentes
        options = random.sample(self.color_names, 4)
        if text_color_name not in options:
            options[random.randint(0, 3)] = text_color_name
        random.shuffle(options)
        
        positions = [
            (cx - 140, cy + 70),
            (cx + 140, cy + 70),
            (cx - 140, cy + 160),
            (cx + 140, cy + 160)
        ]
        
        for opt, pos in zip(options, positions):
            is_correct = (opt == text_color_name)
            
            # Color del texto de la opción DIFERENTE al que dice
            option_text_color_name = random.choice([c for c in self.color_names if c != opt])
            option_text_color = self.colors[option_text_color_name]
            
            # Fondo del botón gris oscuro para contraste
            rect = self.canvas.create_rectangle(
                pos[0] - 100, pos[1] - 32,
                pos[0] + 100, pos[1] + 32,
                fill="#2d2d2d", outline="white", width=3)
            self.widgets.append(rect)
            
            text = self.canvas.create_text(
                pos[0], pos[1],
                text=opt,
                font=("Arial", 14, "bold"),
                fill=option_text_color)
            self.widgets.append(text)
            
            self.canvas.tag_bind(rect, "<Button-1>", 
                               lambda e, c=is_correct: self._check_answer(c))
            self.canvas.tag_bind(text, "<Button-1>", 
                               lambda e, c=is_correct: self._check_answer(c))
        
        self._start_timer(6.0)
    
    def _start_timer(self, t):
        if self.game_closed or self.answer_given:
            return
        if t <= 0:
            self.answer_given = True
            self.current_round += 1
            self.canvas.after(500, self._next_round)
            return
        try:
            self.canvas.itemconfig(self.timer_label, 
                text=f"Tiempo: {int(t)}s",
                fill="#FFD700" if t > 3 else "#FF0000")
        except:
            pass
        self.canvas.after(100, lambda: self._start_timer(t - 0.1))
    
    def _check_answer(self, correct):
        if self.answer_given:
            return
        self.answer_given = True
        if correct:
            self.correct_count += 1
        self.current_round += 1
        self.canvas.after(200, self._next_round)
    
    def _finish_game(self):
        if self.game_closed:
            return
        self._clear_widgets()
        
        cx, cy = self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2
        won = self.correct_count >= 7
        
        self.widgets.append(self.canvas.create_text(
            cx, cy - 80,
            text="VICTORIA" if won else "Derrota",
            font=("Arial", 36, "bold"),
            fill="#4CAF50" if won else "#f44336"))
        
        self.widgets.append(self.canvas.create_text(
            cx, cy - 20,
            text=f"Aciertos: {self.correct_count} / {self.rounds}",
            font=("Arial", 18),
            fill="white"))
        
        rect = self.canvas.create_rectangle(
            cx - 80, cy + 50, cx + 80, cy + 100,
            fill="#2196F3", outline="white", width=2)
        self.widgets.append(rect)
        
        text = self.canvas.create_text(
            cx, cy + 75,
            text="CONTINUAR",
            font=("Arial", 14, "bold"),
            fill="white")
        self.widgets.append(text)
        
        self.canvas.tag_bind(rect, "<Button-1>", lambda e: self._close_result(won))
        self.canvas.tag_bind(text, "<Button-1>", lambda e: self._close_result(won))
    
    def _close_result(self, won):
        if not self.game_closed:
            self.game_closed = True
            self._clear_widgets()
            try:
                self.window.destroy()
            except:
                pass
            try:
                self.callback('won' if won else 'lost')
            except:
                pass
    
    def _clear_widgets(self):
        for wid in self.widgets:
            try:
                self.canvas.delete(wid)
            except:
                pass
        self.widgets.clear()
    
    def force_close(self):
        if not self.game_closed:
            self.game_closed = True
            self._clear_widgets()
            try:
                self.window.destroy()
            except:
                pass
            try:
                self.callback('closed')
            except:
                pass
