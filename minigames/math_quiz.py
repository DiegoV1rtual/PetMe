import tkinter as tk
import random
import json
import os
import time

class MathQuiz:
    def __init__(self, parent_window, callback):
        """Minijuego de matemáticas con TIMER de 6 segundos"""
        self.callback = callback
        self.questions = self.load_questions()
        self.selected = random.sample(self.questions, min(10, len(self.questions)))
        self.current_index = 0
        self.correct_count = 0
        self.game_closed = False
        
        # Crear ventana INDEPENDIENTE
        self.window = tk.Toplevel()
        self.window.title("Quiz Matematico")
        
        # CRÍTICO: SIEMPRE en frente
        self.window.attributes("-topmost", True)
        self.window.focus_force()
        self.window.grab_set()
        
        # Tamaño y posición centrada
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        width = 900
        height = 700
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        self.window.configure(bg="#1a1a1a")
        
        # Canvas
        self.canvas = tk.Canvas(self.window, bg="#1a1a1a", 
                               highlightthickness=0, width=width, height=height)
        self.canvas.pack(fill="both", expand=True)
        
        # GEOMETRÍA después de pack
        w, h = 700, 500
        self.window.geometry(f"{w}x{h}")
        self.window.update_idletasks()
        self.window.update()
        
        # CENTRAR después de todo
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        self.window.geometry(f"+{x}+{y}")
        
        self.widgets = []
        self.timer_running = False
        self.answer_given = False
    
    def load_questions(self):
        """Carga preguntas del JSON"""
        try:
            base_path = os.path.dirname(os.path.dirname(__file__))
            json_path = os.path.join(base_path, "data", "math_questions.json")
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return [
                {"question": "5 + 3 = ?", "options": ["7", "8", "9", "6"], "answer": "8"},
                {"question": "10 - 4 = ?", "options": ["5", "6", "7", "8"], "answer": "6"},
                {"question": "3 * 4 = ?", "options": ["10", "11", "12", "13"], "answer": "12"},
            ]
    
    def run(self):
        """Inicia el juego"""
        self._show_next_question()
    
    def _show_next_question(self):
        """Muestra la siguiente pregunta con TIMER"""
        if self.game_closed or self.current_index >= len(self.selected):
            self._finish_game()
            return
        
        self._clear_widgets()
        self.answer_given = False
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        question_data = self.selected[self.current_index]
        
        # Contador
        counter = self.canvas.create_text(
            center_x, 60,
            text=f"Quiz Matematico - Pregunta {self.current_index + 1}/{len(self.selected)}",
            font=("Arial", 18, "bold"),
            fill="white"
        )
        self.widgets.append(counter)
        
        # TIMER - 6 segundos
        self.timer_label = self.canvas.create_text(
            center_x, 110,
            text="Tiempo: 6s",
            font=("Arial", 16, "bold"),
            fill="#FFD700"
        )
        self.widgets.append(self.timer_label)
        
        # Pregunta
        question_text = self.canvas.create_text(
            center_x, center_y - 100,
            text=question_data["question"],
            font=("Arial", 32, "bold"),
            fill="#2196F3"
        )
        self.widgets.append(question_text)
        
        # Opciones
        options = question_data["options"]
        positions = [
            (center_x - 140, center_y + 40),
            (center_x + 140, center_y + 40),
            (center_x - 140, center_y + 130),
            (center_x + 140, center_y + 130)
        ]
        
        for opt, pos in zip(options, positions):
            is_correct = (opt == question_data["answer"])
            
            btn_rect = self.canvas.create_rectangle(
                pos[0] - 90, pos[1] - 30,
                pos[0] + 90, pos[1] + 30,
                fill="#4CAF50",
                outline="white", width=3
            )
            self.widgets.append(btn_rect)
            
            btn_text = self.canvas.create_text(
                pos[0], pos[1],
                text=opt,
                font=("Arial", 18, "bold"),
                fill="white"
            )
            self.widgets.append(btn_text)
            
            self.canvas.tag_bind(btn_rect, "<Button-1>",
                               lambda e, correct=is_correct: self._check_answer(correct))
            self.canvas.tag_bind(btn_text, "<Button-1>",
                               lambda e, correct=is_correct: self._check_answer(correct))
        
        # Iniciar timer
        self._start_timer(6.0)
    
    def _start_timer(self, time_left):
        """Inicia el countdown de 6 segundos"""
        if self.game_closed or self.answer_given:
            return
        
        if time_left <= 0:
            # Tiempo agotado - contar como incorrecto
            self.answer_given = True
            self.current_index += 1
            self.canvas.after(500, self._show_next_question)
            return
        
        try:
            self.canvas.itemconfig(self.timer_label, 
                                 text=f"Tiempo: {int(time_left)}s",
                                 fill="#FFD700" if time_left > 3 else "#FF0000")
        except:
            pass
        
        self.canvas.after(100, lambda: self._start_timer(time_left - 0.1))
    
    def _check_answer(self, is_correct):
        """Verifica respuesta"""
        if self.answer_given:
            return
        
        self.answer_given = True
        
        if is_correct:
            self.correct_count += 1
        
        self.current_index += 1
        self.canvas.after(200, self._show_next_question)
    
    def _finish_game(self):
        """Finaliza el juego"""
        if self.game_closed:
            return
        
        self._clear_widgets()
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        won = self.correct_count >= 5
        
        # Resultado
        if won:
            result = self.canvas.create_text(
                center_x, center_y - 100,
                text="VICTORIA",
                font=("Arial", 40, "bold"),
                fill="#4CAF50"
            )
        else:
            result = self.canvas.create_text(
                center_x, center_y - 100,
                text="Derrota",
                font=("Arial", 40, "bold"),
                fill="#f44336"
            )
        self.widgets.append(result)
        
        # Puntuación
        score = self.canvas.create_text(
            center_x, center_y - 30,
            text=f"Aciertos: {self.correct_count} / {len(self.selected)}",
            font=("Arial", 20),
            fill="white"
        )
        self.widgets.append(score)
        
        # Botón continuar
        btn_rect = self.canvas.create_rectangle(
            center_x - 100, center_y + 70,
            center_x + 100, center_y + 130,
            fill="#2196F3", outline="white", width=3
        )
        self.widgets.append(btn_rect)
        
        btn_text = self.canvas.create_text(
            center_x, center_y + 100,
            text="CONTINUAR",
            font=("Arial", 16, "bold"),
            fill="white"
        )
        self.widgets.append(btn_text)
        
        self.canvas.tag_bind(btn_rect, "<Button-1>",
                           lambda e: self._close_result(won))
        self.canvas.tag_bind(btn_text, "<Button-1>",
                           lambda e: self._close_result(won))
    
    def _close_result(self, won):
        """Cierra resultado"""
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
        """Limpia widgets"""
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
                self.window.destroy()
            except:
                pass
            try:
                self.callback('closed')
            except:
                pass
