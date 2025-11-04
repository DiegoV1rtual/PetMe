import tkinter as tk
import random
import time

class MemoryGame:
    def __init__(self, parent_window, callback):
        """Juego de memoria"""
        self.callback = callback
        self.sequence = []
        self.player_sequence = []
        self.level = 1
        self.max_level = 10
        self.colors = ["ROJO", "AZUL", "VERDE", "AMARILLO"]
        self.color_hex = {
            "ROJO": "#f44336",
            "AZUL": "#2196F3",
            "VERDE": "#4CAF50",
            "AMARILLO": "#FFC107"
        }
        self.game_closed = False
        self.waiting_player = False
        self.button_rects = {}
        
        # Crear ventana INDEPENDIENTE
        self.window = tk.Toplevel()
        self.window.title("Juego de Memoria")
        
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
        
        # Título
        title = self.canvas.create_text(
            center_x, center_y - 150,
            text="JUEGO DE MEMORIA",
            font=("Arial", 28, "bold"),
            fill="white"
        )
        self.widgets.append(title)
        
        # Instrucciones
        inst = self.canvas.create_text(
            center_x, center_y - 70,
            text="Memoriza la secuencia de colores\ny repitela correctamente",
            font=("Arial", 18),
            fill="yellow",
            justify="center"
        )
        self.widgets.append(inst)
        
        # Botón comenzar
        btn_rect = self.canvas.create_rectangle(
            center_x - 100, center_y + 70,
            center_x + 100, center_y + 130,
            fill="#4CAF50", outline="white", width=3
        )
        self.widgets.append(btn_rect)
        
        btn_text = self.canvas.create_text(
            center_x, center_y + 100,
            text="COMENZAR",
            font=("Arial", 16, "bold"),
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
        
        # Nivel
        level_text = self.canvas.create_text(
            center_x, 60,
            text=f"Nivel {self.level} / {self.max_level}",
            font=("Arial", 20, "bold"),
            fill="white"
        )
        self.widgets.append(level_text)
        
        # Status
        self.status_id = self.canvas.create_text(
            center_x, 110,
            text="Memoriza la secuencia...",
            font=("Arial", 16),
            fill="#aaaaaa"
        )
        self.widgets.append(self.status_id)
        
        # Botones de colores (2x2)
        positions = [
            (center_x - 130, center_y - 70),
            (center_x + 130, center_y - 70),
            (center_x - 130, center_y + 100),
            (center_x + 130, center_y + 100)
        ]
        
        self.button_rects = {}
        for color, pos in zip(self.colors, positions):
            rect = self.canvas.create_rectangle(
                pos[0] - 80, pos[1] - 50,
                pos[0] + 80, pos[1] + 50,
                fill=self.color_hex[color], outline="white", width=4
            )
            self.widgets.append(rect)
            
            text = self.canvas.create_text(
                pos[0], pos[1],
                text=color,
                font=("Arial", 14, "bold"),
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
                    self.canvas.itemconfig(self.status_id, text="Tu turno - Repite la secuencia")
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
        
        # Resultado
        if won:
            result = self.canvas.create_text(
                center_x, center_y - 100,
                text="VICTORIA",
                font=("Arial", 40, "bold"),
                fill="#4CAF50"
            )
            details = self.canvas.create_text(
                center_x, center_y - 30,
                text=f"Completaste los 10 niveles",
                font=("Arial", 18),
                fill="white"
            )
        else:
            result = self.canvas.create_text(
                center_x, center_y - 100,
                text="Derrota",
                font=("Arial", 40, "bold"),
                fill="#f44336"
            )
            details = self.canvas.create_text(
                center_x, center_y - 30,
                text=f"Llegaste al nivel {self.level}",
                font=("Arial", 18),
                fill="white"
            )
        self.widgets.append(result)
        self.widgets.append(details)
        
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
        self.button_rects.clear()
    
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
