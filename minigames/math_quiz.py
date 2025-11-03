import tkinter as tk
import random
import json
import os

class MathQuiz:
    def __init__(self, parent_canvas, callback):
        self.canvas = parent_canvas
        self.callback = callback
        self.questions = self.load_questions()
        self.selected = random.sample(self.questions, min(10, len(self.questions)))
        self.current_index = 0
        self.correct_count = 0
        self.game_closed = False
        self.widgets = []
    
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
        """Muestra la siguiente pregunta"""
        if self.game_closed or self.current_index >= len(self.selected):
            self._finish_game()
            return
        
        self._clear_widgets()
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        question_data = self.selected[self.current_index]
        
        # Fondo
        bg = self.canvas.create_rectangle(
            0, 0, canvas_width, canvas_height,
            fill="#1a1a1a", outline=""
        )
        self.widgets.append(bg)
        
        # Contador
        counter = self.canvas.create_text(
            center_x, 40,
            text=f"📚 Quiz Matemático - Pregunta {self.current_index + 1}/{len(self.selected)}",
            font=("Arial", 16, "bold"),
            fill="white"
        )
        self.widgets.append(counter)
        
        # Pregunta
        question_text = self.canvas.create_text(
            center_x, center_y - 100,
            text=question_data["question"],
            font=("Arial", 28, "bold"),
            fill="#2196F3"
        )
        self.widgets.append(question_text)
        
        # Opciones
        options = question_data["options"]
        positions = [
            (center_x - 120, center_y + 20),
            (center_x + 120, center_y + 20),
            (center_x - 120, center_y + 100),
            (center_x + 120, center_y + 100)
        ]
        
        for opt, pos in zip(options, positions):
            is_correct = (opt == question_data["answer"])
            
            btn_rect = self.canvas.create_rectangle(
                pos[0] - 70, pos[1] - 25,
                pos[0] + 70, pos[1] + 25,
                fill="#4CAF50" if not is_correct else "#4CAF50",
                outline="white", width=2
            )
            self.widgets.append(btn_rect)
            
            btn_text = self.canvas.create_text(
                pos[0], pos[1],
                text=opt,
                font=("Arial", 16, "bold"),
                fill="white"
            )
            self.widgets.append(btn_text)
            
            self.canvas.tag_bind(btn_rect, "<Button-1>",
                               lambda e, correct=is_correct: self._check_answer(correct))
            self.canvas.tag_bind(btn_text, "<Button-1>",
                               lambda e, correct=is_correct: self._check_answer(correct))
    
    def _check_answer(self, is_correct):
        """Verifica respuesta"""
        if is_correct:
            self.correct_count += 1
        
        self.current_index += 1
        self.canvas.after(100, self._show_next_question)
    
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
            text=f"Aciertos: {self.correct_count} / {len(self.selected)}",
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
        """Cierra resultado"""
        if not self.game_closed:
            self.game_closed = True
            self._clear_widgets()
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
                self.callback('closed')
            except:
                pass
