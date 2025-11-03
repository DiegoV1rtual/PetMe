import tkinter as tk
import random
import time

class StroopGame:
    """Efecto Stroop: Di el COLOR del texto, no lo que dice la palabra"""
    
    def __init__(self, parent_canvas, callback):
        self.canvas = parent_canvas
        self.callback = callback
        self.rounds = 10
        self.current_round = 0
        self.correct_count = 0
        self.game_closed = False
        self.widgets = []
        
        self.colors = {
            "ROJO": "#FF0000",
            "AZUL": "#0000FF",
            "VERDE": "#00FF00",
            "AMARILLO": "#FFFF00",
            "MORADO": "#800080",
            "NARANJA": "#FF8800"
        }
        
        self.color_names = list(self.colors.keys())
    
    def run(self):
        """Inicia el juego"""
        self._show_instructions()
    
    def _show_instructions(self):
        """Muestra instrucciones"""
        self._clear_widgets()
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        # Fondo
        bg = self.canvas.create_rectangle(
            0, 0, canvas_width, canvas_height,
            fill="#1a1a1a", outline=""
        )
        self.widgets.append(bg)
        
        # Título
        title = self.canvas.create_text(
            center_x, center_y - 150,
            text="⚡ EFECTO STROOP ⚡",
            font=("Arial", 24, "bold"),
            fill="white"
        )
        self.widgets.append(title)
        
        # Instrucciones
        inst = self.canvas.create_text(
            center_x, center_y - 80,
            text="Selecciona el COLOR del texto\n¡NO lo que dice la palabra!",
            font=("Arial", 16),
            fill="yellow",
            justify="center"
        )
        self.widgets.append(inst)
        
        # Ejemplo
        example = self.canvas.create_text(
            center_x, center_y - 20,
            text='Si ves "ROJO" en color azul\n→ Selecciona AZUL',
            font=("Arial", 14, "italic"),
            fill="#aaaaaa",
            justify="center"
        )
        self.widgets.append(example)
        
        # Botón comenzar
        btn_rect = self.canvas.create_rectangle(
            center_x - 80, center_y + 60,
            center_x + 80, center_y + 110,
            fill="#4CAF50", outline="white", width=2
        )
        self.widgets.append(btn_rect)
        
        btn_text = self.canvas.create_text(
            center_x, center_y + 85,
            text="COMENZAR",
            font=("Arial", 14, "bold"),
            fill="white"
        )
        self.widgets.append(btn_text)
        
        self.canvas.tag_bind(btn_rect, "<Button-1>", lambda e: self._next_round())
        self.canvas.tag_bind(btn_text, "<Button-1>", lambda e: self._next_round())
    
    def _next_round(self):
        """Muestra la siguiente ronda"""
        if self.game_closed or self.current_round >= self.rounds:
            self._finish_game()
            return
        
        self._clear_widgets()
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        # Fondo
        bg = self.canvas.create_rectangle(
            0, 0, canvas_width, canvas_height,
            fill="#1a1a1a", outline=""
        )
        self.widgets.append(bg)
        
        # Contador
        counter = self.canvas.create_text(
            center_x, 40,
            text=f"Ronda {self.current_round + 1} / {self.rounds}",
            font=("Arial", 16, "bold"),
            fill="white"
        )
        self.widgets.append(counter)
        
        # Elegir palabra y color aleatorios (diferentes)
        word = random.choice(self.color_names)
        text_color_name = random.choice([c for c in self.color_names if c != word])
        text_color = self.colors[text_color_name]
        
        # Mostrar palabra en color diferente
        word_text = self.canvas.create_text(
            center_x, center_y - 80,
            text=word,
            font=("Arial", 48, "bold"),
            fill=text_color
        )
        self.widgets.append(word_text)
        
        # Instrucción
        inst = self.canvas.create_text(
            center_x, center_y - 20,
            text="¿De qué COLOR es el texto?",
            font=("Arial", 14),
            fill="white"
        )
        self.widgets.append(inst)
        
        # Botones de opciones (4 colores aleatorios incluyendo el correcto)
        options = random.sample(self.color_names, 4)
        if text_color_name not in options:
            options[random.randint(0, 3)] = text_color_name
        
        random.shuffle(options)
        
        # Crear botones en 2 filas de 2
        positions = [
            (center_x - 120, center_y + 60),
            (center_x + 120, center_y + 60),
            (center_x - 120, center_y + 140),
            (center_x + 120, center_y + 140)
        ]
        
        for i, (opt, pos) in enumerate(zip(options, positions)):
            is_correct = (opt == text_color_name)
            
            btn_rect = self.canvas.create_rectangle(
                pos[0] - 80, pos[1] - 25,
                pos[0] + 80, pos[1] + 25,
                fill=self.colors[opt], outline="white", width=2
            )
            self.widgets.append(btn_rect)
            
            btn_text = self.canvas.create_text(
                pos[0], pos[1],
                text=opt,
                font=("Arial", 12, "bold"),
                fill="white"
            )
            self.widgets.append(btn_text)
            
            self.canvas.tag_bind(btn_rect, "<Button-1>", 
                               lambda e, correct=is_correct: self._check_answer(correct))
            self.canvas.tag_bind(btn_text, "<Button-1>", 
                               lambda e, correct=is_correct: self._check_answer(correct))
    
    def _check_answer(self, is_correct):
        """Verifica la respuesta"""
        if is_correct:
            self.correct_count += 1
        
        self.current_round += 1
        self.canvas.after(100, self._next_round)
    
    def _finish_game(self):
        """Finaliza el juego"""
        if self.game_closed:
            return
        
        self._clear_widgets()
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        won = self.correct_count >= 7  # Necesita 7+ aciertos
        
        # Fondo
        bg = self.canvas.create_rectangle(
            0, 0, canvas_width, canvas_height,
            fill="#1a1a1a", outline=""
        )
        self.widgets.append(bg)
        
        # Resultado
        if won:
            result = self.canvas.create_text(
                center_x, center_y - 80,
                text="🎉 ¡VICTORIA! 🎉",
                font=("Arial", 32, "bold"),
                fill="#4CAF50"
            )
        else:
            result = self.canvas.create_text(
                center_x, center_y - 80,
                text="😔 Derrota 😔",
                font=("Arial", 32, "bold"),
                fill="#f44336"
            )
        self.widgets.append(result)
        
        # Puntuación
        score = self.canvas.create_text(
            center_x, center_y - 20,
            text=f"Aciertos: {self.correct_count} / {self.rounds}",
            font=("Arial", 18),
            fill="white"
        )
        self.widgets.append(score)
        
        # Botón continuar
        btn_rect = self.canvas.create_rectangle(
            center_x - 80, center_y + 60,
            center_x + 80, center_y + 110,
            fill="#2196F3", outline="white", width=2
        )
        self.widgets.append(btn_rect)
        
        btn_text = self.canvas.create_text(
            center_x, center_y + 85,
            text="CONTINUAR",
            font=("Arial", 14, "bold"),
            fill="white"
        )
        self.widgets.append(btn_text)
        
        self.canvas.tag_bind(btn_rect, "<Button-1>", 
                           lambda e: self._close_result(won))
        self.canvas.tag_bind(btn_text, "<Button-1>", 
                           lambda e: self._close_result(won))
    
    def _close_result(self, won):
        """Cierra el resultado"""
        if not self.game_closed:
            self.game_closed = True
            self._clear_widgets()
            try:
                self.callback('won' if won else 'lost')
            except:
                pass
    
    def _clear_widgets(self):
        """Limpia los widgets del canvas"""
        for widget_id in self.widgets:
            try:
                self.canvas.delete(widget_id)
            except:
                pass
        self.widgets.clear()
    
    def force_close(self):
        """Cierre forzado"""
        if not self.game_closed:
            self.game_closed = True
            self._clear_widgets()
            try:
                self.callback('closed')
            except:
                pass
