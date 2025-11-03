import tkinter as tk
import math
import random

class Roulette:
    def __init__(self, parent_canvas, sectors, callback, title="Ruleta"):
        """Ruleta superpuesta en el canvas principal"""
        self.parent_canvas = parent_canvas
        self.callback = callback
        self.sectors = sectors[:]
        self.n = len(self.sectors)
        self.title = title
        
        self.size = 350
        self.radius = 130
        self.angle = 0
        self.v = 0
        self.dec = 0
        self.spinning = False
        
        # Posición centrada en el canvas
        canvas_width = parent_canvas.winfo_width()
        canvas_height = parent_canvas.winfo_height()
        self.center_x = canvas_width // 2
        self.center_y = canvas_height // 2
        
        self.widgets = []
        self.draw_roulette(0)
    
    def draw_roulette(self, rotation_angle):
        """Dibuja la ruleta en el canvas padre"""
        # Limpiar widgets anteriores
        for widget_id in self.widgets:
            try:
                self.parent_canvas.delete(widget_id)
            except:
                pass
        self.widgets.clear()
        
        # Fondo semi-transparente
        bg = self.parent_canvas.create_rectangle(
            0, 0, 
            self.parent_canvas.winfo_width(), 
            self.parent_canvas.winfo_height(),
            fill="#000000", stipple="gray50", outline=""
        )
        self.widgets.append(bg)
        
        # Título
        title_id = self.parent_canvas.create_text(
            self.center_x, self.center_y - 200,
            text=self.title, font=("Arial", 20, "bold"),
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
            sector_id = self.parent_canvas.create_polygon(
                points, fill=color, outline="white", width=2
            )
            self.widgets.append(sector_id)
            
            # Texto
            mid_angle = math.radians(start_angle + per_sector / 2)
            text_distance = self.radius * 0.65
            tx = self.center_x + math.cos(mid_angle) * text_distance
            ty = self.center_y + math.sin(mid_angle) * text_distance
            
            text_id = self.parent_canvas.create_text(
                tx, ty, text=label, font=("Arial", 10, "bold"),
                fill="white", width=80, justify="center"
            )
            self.widgets.append(text_id)
        
        # Círculo central
        circle_id = self.parent_canvas.create_oval(
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
        arrow_id = self.parent_canvas.create_polygon(
            arrow_points, fill="#FF0000", outline="white", width=2
        )
        self.widgets.append(arrow_id)
        
        # Botón girar (si no está girando)
        if not self.spinning:
            btn_text = self.parent_canvas.create_text(
                self.center_x, self.center_y + self.radius + 40,
                text="GIRAR", font=("Arial", 16, "bold"),
                fill="white"
            )
            self.widgets.append(btn_text)
            
            btn_rect = self.parent_canvas.create_rectangle(
                self.center_x - 60, self.center_y + self.radius + 20,
                self.center_x + 60, self.center_y + self.radius + 60,
                fill="#4CAF50", outline="white", width=2
            )
            self.widgets.append(btn_rect)
            
            # Re-dibujar texto encima
            self.parent_canvas.tag_raise(btn_text)
            
            # Bind click
            self.parent_canvas.tag_bind(btn_rect, "<Button-1>", lambda e: self.start())
            self.parent_canvas.tag_bind(btn_text, "<Button-1>", lambda e: self.start())
    
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
            self.parent_canvas.after(16, self._animate)
        else:
            # Giro terminado
            self.spinning = False
            idx = self._get_winning_sector()
            label, payload = self.sectors[idx]
            
            # Esperar y ejecutar callback
            self.parent_canvas.after(800, lambda: self._finish(payload))
    
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
        for widget_id in self.widgets:
            try:
                self.parent_canvas.delete(widget_id)
            except:
                pass
        self.widgets.clear()
