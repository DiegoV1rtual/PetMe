import tkinter as tk
import math
import random

class Roulette:
    def __init__(self, parent_window, sectors, callback, title="Ruleta"):
        """Ruleta en ventana INDEPENDIENTE - SIEMPRE EN PRIMERA PANTALLA"""
        self.callback = callback
        self.sectors = sectors[:]
        self.n = len(self.sectors)
        self.title = title
        
        # Crear ventana NUEVA e independiente
        self.window = tk.Toplevel()
        self.window.title(title)
        
        # CRÍTICO: Ventana SIEMPRE en frente
        self.window.attributes("-topmost", True)
        self.window.attributes("-fullscreen", False)
        self.window.focus_force()
        self.window.grab_set()  # Modal
        
        # Tamaño y posición centrada
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        width = 900
        height = 700
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        self.window.configure(bg="#1a1a1a")
        
        # Canvas para la ruleta
        self.canvas = tk.Canvas(self.window, bg="#1a1a1a", 
                               highlightthickness=0, width=width, height=height)
        self.canvas.pack(fill="both", expand=True)
        
        self.size = 350
        self.radius = 130
        self.angle = 0
        self.v = 0
        self.dec = 0
        self.spinning = False
        
        self.center_x = width // 2
        self.center_y = height // 2
        
        self.widgets = []
        self.draw_roulette(0)
    
    def draw_roulette(self, rotation_angle):
        """Dibuja la ruleta"""
        # Limpiar widgets anteriores
        for widget_id in self.widgets:
            try:
                self.canvas.delete(widget_id)
            except:
                pass
        self.widgets.clear()
        
        # Título
        title_id = self.canvas.create_text(
            self.center_x, self.center_y - 250,
            text=self.title, font=("Arial", 24, "bold"),
            fill="white"
        )
        self.widgets.append(title_id)
        
        cx = cy = self.center_x, self.center_y
        per_sector = 360.0 / self.n
        
        # Colores
        colors = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#A8E6CF", "#FF8B94", "#C7CEEA"]
        
        for i, (label, payload) in enumerate(self.sectors):
            start_angle = (i * per_sector - rotation_angle) % 360
            
            # Crear polígono
            points = [self.center_x, self.center_y]
            for step in range(0, 37):
                angle_rad = math.radians(start_angle + step * (per_sector / 36))
                x = self.center_x + math.cos(angle_rad) * self.radius
                y = self.center_y + math.sin(angle_rad) * self.radius
                points.extend([x, y])
            
            color = colors[i % len(colors)]
            sector_id = self.canvas.create_polygon(
                points, fill=color, outline="white", width=2
            )
            self.widgets.append(sector_id)
            
            # Texto
            mid_angle = math.radians(start_angle + per_sector / 2)
            text_distance = self.radius * 0.65
            tx = self.center_x + math.cos(mid_angle) * text_distance
            ty = self.center_y + math.sin(mid_angle) * text_distance
            
            text_id = self.canvas.create_text(
                tx, ty, text=label, font=("Arial", 11, "bold"),
                fill="white", width=80, justify="center"
            )
            self.widgets.append(text_id)
        
        # Círculo central
        circle_id = self.canvas.create_oval(
            self.center_x - 20, self.center_y - 20,
            self.center_x + 20, self.center_y + 20,
            fill="#FFD700", outline="white", width=2
        )
        self.widgets.append(circle_id)
        
        # Flecha indicador
        arrow_points = [
            self.center_x - 15, self.center_y - self.radius - 20,
            self.center_x + 15, self.center_y - self.radius - 20,
            self.center_x, self.center_y - self.radius + 5
        ]
        arrow_id = self.canvas.create_polygon(
            arrow_points, fill="#FF0000", outline="white", width=2
        )
        self.widgets.append(arrow_id)
        
        # Botón girar (si no está girando)
        if not self.spinning:
            btn_rect = self.canvas.create_rectangle(
                self.center_x - 80, self.center_y + self.radius + 40,
                self.center_x + 80, self.center_y + self.radius + 90,
                fill="#4CAF50", outline="white", width=3
            )
            self.widgets.append(btn_rect)
            
            btn_text = self.canvas.create_text(
                self.center_x, self.center_y + self.radius + 65,
                text="GIRAR", font=("Arial", 18, "bold"),
                fill="white"
            )
            self.widgets.append(btn_text)
            
            # Bind click
            self.canvas.tag_bind(btn_rect, "<Button-1>", lambda e: self.start())
            self.canvas.tag_bind(btn_text, "<Button-1>", lambda e: self.start())
    
    def start(self):
        """Inicia el giro"""
        if self.spinning:
            return
        
        self.spinning = True
        self.v = random.uniform(20, 35)
        self.dec = random.uniform(0.15, 0.25)
        self._animate()
    
    def _animate(self):
        """Animación del giro"""
        if self.v > 0.1:
            self.angle += self.v
            self.v -= self.dec
            
            if self.v < 0:
                self.v = 0
            
            self.draw_roulette(self.angle)
            self.canvas.after(16, self._animate)
        else:
            # Giro terminado
            self.spinning = False
            idx = self._get_winning_sector()
            label, payload = self.sectors[idx]
            
            # Esperar y ejecutar callback
            self.canvas.after(800, lambda: self._finish(payload))
    
    def _get_winning_sector(self):
        """Determina el sector ganador"""
        normalized = self.angle % 360
        pointer_angle = (90 - normalized) % 360
        per_sector = 360.0 / self.n
        sector_index = int(pointer_angle / per_sector) % self.n
        return sector_index
    
    def _finish(self, payload):
        """Finaliza y limpia"""
        self.close()
        try:
            self.callback(payload)
        except:
            pass
    
    def close(self):
        """Cierra la ruleta"""
        try:
            self.window.destroy()
        except:
            pass
