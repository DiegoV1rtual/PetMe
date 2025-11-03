import tkinter as tk
import random
import time

class MemoryGame:
    def __init__(self, parent_canvas, callback):
        self.canvas = parent_canvas
        self.callback = callback
        self.sequence = []
        self.player_sequence = []
        self.level = 1
        self.max_level = 5
        self.colors = ["ROJO", "AZUL", "VERDE", "AMARILLO"]
        self.color_hex = {
            "ROJO": "#f44336",
            "AZUL": "#2196F3",
            "VERDE": "#4CAF50",
            "AMARILLO": "#FFC107"
        }
        self.game_closed = False
        self.widgets = []
        self.waiting_player = False
        self.button_rects = {}
    
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
            center_x, center_y - 120,
            text="🧠 Juego de Memoria 🧠",
            font=("Arial", 24, "bold"),
            fill="white"
        )
        self.widgets.append(title)
        
        # Instrucciones
        inst = self.canvas.create_text(
            center_x, center_y - 50,
            text="Memoriza la secuencia de colores\ny repítela correctamente",
            font=("Arial", 16),
            fill="white",
            justify="center"
        )
        self.widgets.append(inst)
        
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
        
        self.canvas.tag_bind(btn_rect, "<Button-1>", lambda e: self._next_level())
        self.canvas.tag_bind(btn_text, "<Button-1>", lambda e: self._next_level())
    
    def _next_level(self):
        """Genera siguiente nivel"""
        if self.game_closed:
            return
        
        self.player_sequence = []
        self.sequence.append(random.choice(self.colors))
        self.waiting_player = False
        
        self._draw_game_screen()
        self.canvas.after(1000, lambda: self._show_sequence(0))
    
    def _draw_game_screen(self):
        """Dibuja pantalla de juego"""
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
        
        # Nivel
        level_text = self.canvas.create_text(
            center_x, 40,
            text=f"Nivel {self.level} / {self.max_level}",
            font=("Arial", 18, "bold"),
            fill="white"
        )
        self.widgets.append(level_text)
        
        # Status
        self.status_id = self.canvas.create_text(
            center_x, 80,
            text="Memoriza la secuencia...",
            font=("Arial", 14),
            fill="#aaaaaa"
        )
        self.widgets.append(self.status_id)
        
        # Botones de colores (2x2)
        positions = [
            (center_x - 100, center_y - 50),
            (center_x + 100, center_y - 50),
            (center_x - 100, center_y + 80),
            (center_x + 100, center_y + 80)
        ]
        
        self.button_rects = {}
        for color, pos in zip(self.colors, positions):
            rect = self.canvas.create_rectangle(
                pos[0] - 60, pos[1] - 40,
                pos[0] + 60, pos[1] + 40,
                fill=self.color_hex[color], outline="white", width=3
            )
            self.widgets.append(rect)
            
            text = self.canvas.create_text(
                pos[0], pos[1],
                text=color,
                font=("Arial", 12, "bold"),
                fill="white"
            )
            self.widgets.append(text)
            
            self.button_rects[color] = (rect, text)
            
            self.canvas.tag_bind(rect, "<Button-1>",
                               lambda e, c=color: self._player_click(c))
            self.canvas.tag_bind(text, "<Button-1>",
                               lambda e, c=color: self._player_click(c))
    
    def _show_sequence(self, index):
        """Muestra la secuencia"""
        if self.game_closed or index >= len(self.sequence):
            if index >= len(self.sequence):
                try:
                    self.canvas.itemconfig(self.status_id, text="¡Tu turno! Repite la secuencia")
                except:
                    pass
                self.waiting_player = True
            return
        
        color = self.sequence[index]
        self._flash_button(color)
        self.canvas.after(800, lambda: self._show_sequence(index + 1))
    
    def _flash_button(self, color):
        """Hace parpadear un botón"""
        if self.game_closed or color not in self.button_rects:
            return
        
        rect, text = self.button_rects[color]
        try:
            self.canvas.itemconfig(rect, fill="white")
            self.canvas.after(300, lambda: self.canvas.itemconfig(rect, fill=self.color_hex[color]))
        except:
            pass
    
    def _player_click(self, color):
        """Maneja clic del jugador"""
        if not self.waiting_player or self.game_closed:
            return
        
        self._flash_button(color)
        self.player_sequence.append(color)
        
        # Verificar
        if self.player_sequence[-1] != self.sequence[len(self.player_sequence) - 1]:
            # Error
            self._game_over(False)
            return
        
        # Completó la secuencia
        if len(self.player_sequence) == len(self.sequence):
            self.level += 1
            if self.level > self.max_level:
                # Victoria
                self._game_over(True)
            else:
                # Siguiente nivel
                self.waiting_player = False
                self.canvas.after(1000, self._next_level)
    
    def _game_over(self, won):
        """Finaliza el juego"""
        if self.game_closed:
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
        
        # Resultado
        if won:
            result = self.canvas.create_text(
                center_x, center_y - 80,
                text="🎉 ¡VICTORIA! 🎉",
                font=("Arial", 32, "bold"),
                fill="#4CAF50"
            )
            details = self.canvas.create_text(
                center_x, center_y - 20,
                text=f"¡Completaste los {self.max_level} niveles!",
                font=("Arial", 16),
                fill="white"
            )
        else:
            result = self.canvas.create_text(
                center_x, center_y - 80,
                text="😔 Derrota 😔",
                font=("Arial", 32, "bold"),
                fill="#f44336"
            )
            details = self.canvas.create_text(
                center_x, center_y - 20,
                text=f"Llegaste al nivel {self.level}",
                font=("Arial", 16),
                fill="white"
            )
        self.widgets.append(result)
        self.widgets.append(details)
        
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
        self.button_rects.clear()
    
    def force_close(self):
        """Cierre forzado"""
        if not self.game_closed:
            self.game_closed = True
            self._clear_widgets()
            try:
                self.callback('closed')
            except:
                pass
