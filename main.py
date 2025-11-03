import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time
import threading
import os
from modules.config import *
from modules.roulette import Roulette
from minigames.math_quiz import MathQuiz
from minigames.memory_game import MemoryGame
from minigames.stroop_game import StroopGame
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except:
    HAS_PIL = False
    print("⚠️ Pillow no instalado - usando sprite simple")

class PetOverlay:
    """MASCOTA FLOTANTE que se sobrepone a TODO el sistema - CARGA DESDE assets/sprites/"""
    def __init__(self, parent_app):
        self.app = parent_app
        self.window = tk.Toplevel()
        self.window.title("")
        
        # CRÍTICO: Ventana transparente y SIEMPRE SOBRE TODO
        self.window.attributes("-topmost", True)
        self.window.attributes("-transparentcolor", "black")
        self.window.overrideredirect(True)  # Sin bordes
        
        # Obtener tamaño de pantalla
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Tamaño del sprite
        self.size = 150
        
        # Posición inicial (centro de pantalla)
        x = screen_width // 2 - self.size // 2
        y = screen_height // 2 - self.size // 2
        self.window.geometry(f"{self.size}x{self.size}+{x}+{y}")
        
        # Canvas transparente (fondo negro = transparente)
        self.canvas = tk.Canvas(self.window, bg="black", 
                               highlightthickness=0, width=self.size, height=self.size)
        self.canvas.pack()
        
        # Cargar sprite desde assets/sprites/
        self.load_sprite()
        
        # Hacer arrastrable
        self.canvas.bind("<Button-1>", self._start_drag)
        self.canvas.bind("<B1-Motion>", self._drag)
        
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def load_sprite(self, state="normal"):
        """Carga sprite según el estado emocional"""
        # Limpiar canvas
        self.canvas.delete("all")
        
        # Intentar cargar imagen desde assets/sprites/{state}.png
        sprite_path = os.path.join("assets", "sprites", f"{state}.png")
        
        if HAS_PIL and os.path.exists(sprite_path):
            try:
                img = Image.open(sprite_path)
                img = img.resize((self.size, self.size), Image.Resampling.LANCZOS)
                self.sprite_img = ImageTk.PhotoImage(img)
                self.sprite_id = self.canvas.create_image(
                    self.size//2, self.size//2, image=self.sprite_img
                )
                return
            except Exception as e:
                print(f"⚠️ Error cargando {sprite_path}: {e}")
        
        # Sprite simple según estado
        self._draw_simple_sprite(state)
    
    def _draw_simple_sprite(self, state):
        """Dibuja sprite simple (cuadrado con texto) según el estado"""
        center = self.size // 2
        
        # Configuración por estado
        states_config = {
            "normal": {"color": "#4CAF50", "text": "😊\nNORMAL", "text_color": "white"},
            "hambriento": {"color": "#FF6B6B", "text": "😫\nHAMBRE", "text_color": "white"},
            "muy_hambriento": {"color": "#D32F2F", "text": "😵\nMUERO DE\nHAMBRE", "text_color": "white"},
            "gordo": {"color": "#FF9800", "text": "🤢\nGORDO", "text_color": "white"},
            "sucio": {"color": "#8B4513", "text": "🤮\nSUCIO", "text_color": "white"},
            "muy_sucio": {"color": "#5D4037", "text": "💩\nASQUEROSO", "text_color": "white"},
            "cansado": {"color": "#9E9E9E", "text": "😴\nCANSADO", "text_color": "white"},
            "agotado": {"color": "#616161", "text": "💤\nAGOTADO", "text_color": "white"},
            "feliz": {"color": "#FFD700", "text": "😄\n¡FELIZ!", "text_color": "black"},
            "muy_feliz": {"color": "#FFC107", "text": "🤩\n¡SÚPER\nFELIZ!", "text_color": "black"},
            "triste": {"color": "#2196F3", "text": "😢\nTRISTE", "text_color": "white"},
            "muy_triste": {"color": "#1565C0", "text": "😭\nMUY\nTRISTE", "text_color": "white"},
            "durmiendo": {"color": "#7E57C2", "text": "😴\nZzz...", "text_color": "white"},
            "enfermo": {"color": "#66BB6A", "text": "🤢\nENFERMO", "text_color": "white"},
            "muriendo": {"color": "#424242", "text": "☠️\nMURIENDO", "text_color": "white"}
        }
        
        config = states_config.get(state, states_config["normal"])
        
        # Cuadrado de fondo
        self.canvas.create_rectangle(
            10, 10, self.size-10, self.size-10,
            fill=config["color"], outline="white", width=4
        )
        
        # Texto del estado
        self.canvas.create_text(
            center, center,
            text=config["text"],
            font=("Arial", 16, "bold"),
            fill=config["text_color"],
            justify="center"
        )
    
    def update_state(self, state):
        """Actualiza el sprite según el estado"""
        self.load_sprite(state)
    
    def _start_drag(self, event):
        self._drag_data = {"x": event.x, "y": event.y}
    
    def _drag(self, event):
        """Arrastra la mascota por la pantalla"""
        if hasattr(self, '_drag_data'):
            x = self.window.winfo_x() + event.x - self._drag_data["x"]
            y = self.window.winfo_y() + event.y - self._drag_data["y"]
            self.window.geometry(f"{self.size}x{self.size}+{x}+{y}")
    
    def move_to(self, x, y):
        """Mueve la mascota a posición específica de LA PANTALLA"""
        # Limitar a bordes de pantalla
        x = max(0, min(x, self.screen_width - self.size))
        y = max(0, min(y, self.screen_height - self.size))
        self.window.geometry(f"{self.size}x{self.size}+{x}+{y}")
    
    def get_position(self):
        """Obtiene posición actual en la pantalla"""
        return self.window.winfo_x(), self.window.winfo_y()
    
    def random_move(self):
        """Mueve la mascota a una posición aleatoria de LA PANTALLA de forma gradual"""
        target_x = random.randint(0, self.screen_width - self.size)
        target_y = random.randint(0, self.screen_height - self.size)
        self._animate_move_to(target_x, target_y)
    
    def _animate_move_to(self, target_x, target_y):
        """Anima el movimiento gradual hacia una posición"""
        current_x = self.window.winfo_x()
        current_y = self.window.winfo_y()
        
        steps = 30  # Pasos de animación
        dx = (target_x - current_x) / steps
        dy = (target_y - current_y) / steps
        
        for _ in range(steps):
            current_x += dx
            current_y += dy
            self.window.geometry(f"{self.size}x{self.size}+{int(current_x)}+{int(current_y)}")
            self.window.update()
            time.sleep(0.03)  # Velocidad de movimiento

class GameOverlay:
    """Overlay para minijuegos y ruletas - SE SOBREPONE A TODO como la mascota"""
    def __init__(self, parent_app):
        self.app = parent_app
        self.window = None
        self.canvas = None
    
    def create(self):
        """Crea overlay de juego"""
        if self.window:
            return self.canvas
        
        self.window = tk.Toplevel()
        self.window.title("")
        
        # Overlay transparente PERO menos que la mascota
        self.window.attributes("-topmost", True)
        self.window.attributes("-alpha", 0.98)  # Casi opaco
        self.window.overrideredirect(True)  # Sin bordes
        
        # Pantalla completa centrada
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        width = 900
        height = 700
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Canvas oscuro
        self.canvas = tk.Canvas(self.window, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Asegurar que la mascota siga estando encima
        self.app.pet_overlay.window.lift()
        
        return self.canvas
    
    def destroy(self):
        """Destruye overlay"""
        if self.window:
            try:
                self.window.destroy()
            except:
                pass
            self.window = None
            self.canvas = None
            
            # Asegurar que la mascota siga encima
            self.app.pet_overlay.window.lift()

class CountdownPet:
    def __init__(self, root):
        self.root = root
        self.root.title("CountdownPet - Panel de Control")
        self.root.geometry("400x350")  # Más alto para el contador
        self.root.configure(bg="#2d2d2d")
        
        # ALWAYS ON TOP
        if ALWAYS_ON_TOP:
            self.root.attributes("-topmost", True)
        
        # Sin cerrar con X
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Estados
        self.hambre = 50  # Empiezan en 50%
        self.sueno = 50
        self.higiene = 50
        self.felicidad = 50
        self.alive = True
        self.paused = False
        self.sleeping = False
        self.sleep_start_time = None
        
        # Contador de 168 horas (7 días)
        self.game_start_time = time.time()
        self.total_time = 168 * 3600  # 168 horas en segundos
        self.pause_time_used = 0  # Tiempo de pausa usado hoy
        self.pause_time_limit = 7 * 3600  # 7 horas de pausa al día
        self.last_day_reset = time.time()  # Para resetear pausa diaria
        
        # Crear mascota flotante SOBRE TODO EL SISTEMA
        self.pet_overlay = PetOverlay(self)
        
        # Overlay para juegos (bajo la mascota pero sobre todo lo demás)
        self.game_overlay = GameOverlay(self)
        self.current_game = None
        self.minigame_popup = None
        
        # Crear panel de control
        self.create_control_panel()
        
        # Iniciar threads
        threading.Thread(target=self._decay_loop, daemon=True).start()
        threading.Thread(target=self._pet_movement_loop, daemon=True).start()
        threading.Thread(target=self._minigame_event_loop, daemon=True).start()
        threading.Thread(target=self._sleep_monitor_loop, daemon=True).start()
    
    def create_control_panel(self):
        """Panel de control con barras"""
        # Título
        title = tk.Label(self.root, text="🐾 COUNTDOWN PET 🐾",
                        font=("Arial", 13, "bold"), bg="#2d2d2d", fg="white")
        title.pack(pady=8)
        
        # Contador de 168 horas
        self.time_frame = tk.Frame(self.root, bg="#1a1a1a", relief="sunken", bd=2)
        self.time_frame.pack(fill="x", padx=10, pady=5)
        
        self.time_label = tk.Label(self.time_frame, text="⏱️ Tiempo: 168:00:00",
                                   font=("Arial", 11, "bold"), bg="#1a1a1a", fg="#00FF00")
        self.time_label.pack(side="left", padx=10, pady=5)
        
        # Botón de pausa
        self.pause_button = tk.Button(self.time_frame, text="⏸️ PAUSAR (7h/día)",
                                      command=self.toggle_pause,
                                      font=("Arial", 9, "bold"), bg="#FFC107", fg="black",
                                      relief="raised", cursor="hand2")
        self.pause_button.pack(side="right", padx=10, pady=5)
        
        # Frame para stats
        stats_container = tk.Frame(self.root, bg="#2d2d2d")
        stats_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Crear cada estadística (incluyendo felicidad CON cuadradito)
        self.stat_widgets = {}
        stats = [
            ("hambre", "🍔 Alimentar", "#FF6B6B", self.feed_pet),
            ("sueno", "😴 Dormir", "#4ECDC4", self.toggle_sleep),
            ("higiene", "🛁 Duchar", "#95E1D3", self.shower_pet),
            ("felicidad", "💛 Felicidad", "#FFE66D", None)  # También con cuadradito
        ]
        
        for stat_name, btn_text, color, command in stats:
            self._create_stat_row(stats_container, stat_name, btn_text, color, command)
        
        # Separador
        sep = tk.Frame(self.root, height=2, bg="#555")
        sep.pack(fill="x", pady=8)
        
        # Botón admin
        admin_btn = tk.Button(self.root, text="⚙️ Admin",
                             command=self.open_admin,
                             font=("Arial", 10, "bold"), bg="#FF5722", fg="white",
                             relief="raised", cursor="hand2", pady=5)
        admin_btn.pack(fill="x", padx=10, pady=5)
        
        # Iniciar thread del contador
        threading.Thread(target=self._countdown_loop, daemon=True).start()
    
    def _create_stat_row(self, parent, stat_name, btn_text, color, command):
        """Crea fila con botón/label a la izquierda y barras a la derecha en CUADRADITO"""
        row_frame = tk.Frame(parent, bg="#2d2d2d")
        row_frame.pack(fill="x", pady=4)
        
        # Botón o label a la izquierda
        if command:
            btn = tk.Button(row_frame, text=btn_text,
                           command=command,
                           font=("Arial", 9, "bold"), bg=color, fg="white",
                           width=13, relief="raised", cursor="hand2")
            btn.pack(side="left", padx=(0, 8))
            
            # Guardar referencia al botón si es dormir
            if stat_name == "sueno":
                self.sleep_button = btn
        else:
            # Para felicidad, crear un cuadradito igual que los botones
            lbl = tk.Label(row_frame, text=btn_text,
                          font=("Arial", 9, "bold"), bg=color, fg="white",
                          width=13, anchor="center", relief="raised", bd=2)
            lbl.pack(side="left", padx=(0, 8))
        
        # Frame con borde para las barras (cuadradito)
        bars_container = tk.Frame(row_frame, bg="#1a1a1a", relief="sunken", bd=2)
        bars_container.pack(side="left")
        
        bars_frame = tk.Frame(bars_container, bg="#1a1a1a")
        bars_frame.pack(padx=2, pady=2)
        
        bars = []
        for i in range(10):
            bar = tk.Label(bars_frame, text="█", font=("Arial", 11),
                          bg="#1a1a1a", fg="#333", padx=0)
            bar.pack(side="left", padx=1)
            bars.append(bar)
        
        self.stat_widgets[stat_name] = {'bars': bars, 'color': color}
    
    def update_display(self):
        """Actualiza las barras"""
        stats = {
            'hambre': self.hambre,
            'sueno': self.sueno,
            'higiene': self.higiene,
            'felicidad': self.felicidad
        }
        
        for stat_name, value in stats.items():
            if stat_name in self.stat_widgets:
                bars_data = self.stat_widgets[stat_name]
                bars = bars_data['bars']
                color = bars_data['color']
                
                filled = int(value / 10)
                
                for i, bar in enumerate(bars):
                    if i < filled:
                        bar.config(fg=color, bg="#1a1a1a")
                    else:
                        bar.config(fg="#333", bg="#1a1a1a")
        
        # Actualizar sprite de la mascota según estado emocional
        self._update_pet_sprite()
        
        # Actualizar color del botón de dormir
        self._update_sleep_button_color()
    
    def _update_sleep_button_color(self):
        """Actualiza el color del botón de dormir según el estado"""
        if hasattr(self, 'sleep_button'):
            if self.sleeping:
                self.sleep_button.config(bg="#9C27B0", text="☀️ Despertar")  # Morado cuando duerme
            else:
                self.sleep_button.config(bg="#4ECDC4", text="😴 Dormir")  # Cian normal
    
    def toggle_pause(self):
        """Activa/desactiva la pausa del juego"""
        if self.paused:
            # Reanudar
            self.paused = False
            self.pause_button.config(text="⏸️ PAUSAR", bg="#FFC107")
        else:
            # Verificar si tiene tiempo de pausa disponible
            if self.pause_time_used >= self.pause_time_limit:
                messagebox.showwarning("Pausa", 
                    "⚠️ Ya usaste las 7 horas de pausa de hoy.\n"
                    "Se resetea en 24 horas.")
                return
            
            # Pausar
            self.paused = True
            self.pause_button.config(text="▶️ REANUDAR", bg="#4CAF50")
    
    def _countdown_loop(self):
        """Loop del contador de 168 horas"""
        while True:
            try:
                if self.alive:
                    # Calcular tiempo transcurrido
                    elapsed = time.time() - self.game_start_time
                    remaining = self.total_time - elapsed
                    
                    if remaining <= 0:
                        # ¡Victoria! Completó las 168 horas
                        self.root.after(0, self._game_won)
                        break
                    
                    # Actualizar display
                    hours = int(remaining // 3600)
                    minutes = int((remaining % 3600) // 60)
                    seconds = int(remaining % 60)
                    
                    time_str = f"⏱️ Tiempo: {hours:03d}:{minutes:02d}:{seconds:02d}"
                    
                    if self.paused:
                        time_str += " [PAUSADO]"
                        self.time_label.config(text=time_str, fg="#FFC107")
                    else:
                        self.time_label.config(text=time_str, fg="#00FF00")
                    
                    # Resetear pausa diaria
                    if time.time() - self.last_day_reset >= 86400:  # 24 horas
                        self.pause_time_used = 0
                        self.last_day_reset = time.time()
                
                time.sleep(1)
            except:
                time.sleep(1)
    
    def _game_won(self):
        """El jugador ganó - completó las 168 horas"""
        messagebox.showinfo("🎉 ¡VICTORIA! 🎉",
            "¡Felicidades! Mantuviste viva a tu mascota durante 7 días.\n\n"
            "🏆 ¡Has ganado!\n\n"
            "Aquí recibirías tu recompensa de Steam.")
        self.root.quit()
    
    def _get_emotional_state(self):
        """Determina el estado emocional según las estadísticas"""
        if self.sleeping:
            return "durmiendo"
        
        # Prioridad a estados críticos
        if self.hambre >= 90:
            return "gordo"
        elif self.hambre <= 10:
            return "muy_hambriento"
        elif self.hambre <= 30:
            return "hambriento"
        
        if self.higiene <= 10:
            return "muy_sucio"
        elif self.higiene <= 30:
            return "sucio"
        
        if self.sueno <= 10:
            return "agotado"
        elif self.sueno <= 30:
            return "cansado"
        
        if self.felicidad <= 10:
            return "muy_triste"
        elif self.felicidad <= 30:
            return "triste"
        elif self.felicidad >= 80:
            return "muy_feliz"
        elif self.felicidad >= 60:
            return "feliz"
        
        # Estado enfermo si múltiples stats bajas
        stats_bajas = sum([
            self.hambre < 40,
            self.sueno < 40,
            self.higiene < 40,
            self.felicidad < 40
        ])
        
        if stats_bajas >= 3:
            return "muriendo"
        elif stats_bajas >= 2:
            return "enfermo"
        
        return "normal"
    
    def _update_pet_sprite(self):
        """Actualiza el sprite de la mascota"""
        state = self._get_emotional_state()
        self.pet_overlay.update_state(state)
    
    def change_stat(self, stat_name, amount):
        """Cambia estadística"""
        if stat_name == 'hambre':
            self.hambre = max(0, min(100, self.hambre + amount))
            if self.hambre > HUNGER_DEATH_MAX:
                self.die("Sobrealimentación (>90%)")
        elif stat_name == 'sueno':
            self.sueno = max(0, min(100, self.sueno + amount))
        elif stat_name == 'higiene':
            self.higiene = max(0, min(100, self.higiene + amount))
        elif stat_name == 'felicidad':
            self.felicidad = max(0, min(100, self.felicidad + amount))
        
        self.update_display()
        self._check_death()
    
    def _decay_loop(self):
        """Desgaste de estadísticas"""
        while True:
            try:
                if self.alive and not self.paused:
                    if self.sleeping:
                        time.sleep(3600)
                        self.change_stat('hambre', -HUNGER_DECAY_PER_HOUR * 0.2)
                        self.change_stat('higiene', -HYGIENE_DECAY_PER_2HOURS * 0.5 * 0.2)
                    else:
                        time.sleep(3600)
                        self.change_stat('hambre', -HUNGER_DECAY_PER_HOUR)
                        self.change_stat('sueno', -SLEEP_DECAY_PER_HOUR)
                        time.sleep(3600)
                        self.change_stat('higiene', -HYGIENE_DECAY_PER_2HOURS)
                else:
                    time.sleep(5)
            except:
                time.sleep(5)
    
    def _pet_movement_loop(self):
        """Mascota se mueve sola por LA PANTALLA"""
        while True:
            try:
                if self.alive and not self.sleeping and random.random() < 0.4:
                    self.pet_overlay.random_move()
                time.sleep(random.randint(5, 15))
            except:
                time.sleep(5)
    
    def _sleep_monitor_loop(self):
        """Monitorea el sueño y lo aumenta gradualmente"""
        while True:
            try:
                if self.sleeping and self.sleep_start_time:
                    elapsed = time.time() - self.sleep_start_time
                    hours = elapsed / 3600
                    
                    # Aumentar sueño gradualmente (aproximadamente 14% por hora)
                    # Para llegar a 100% en 7 horas
                    if self.sueno < 100:
                        self.change_stat('sueno', 1)  # +1% cada verificación
                    
                    # Después de 8 horas, empieza a perder felicidad
                    if hours >= 8.0:
                        overtime_minutes = (hours - 8.0) * 60
                        if overtime_minutes >= 6:
                            penalty = int(overtime_minutes / 6)
                            self.change_stat('felicidad', -penalty)
                            self.sleep_start_time = time.time() - (8 * 3600)
                
                time.sleep(360)  # Verificar cada 6 minutos
            except:
                time.sleep(60)
    
    def _minigame_event_loop(self):
        """Loop de minijuegos"""
        next_event = time.time() + EVENT_INTERVAL_SECONDS
        
        while True:
            try:
                if self.alive and not self.paused and not self.sleeping and not self.current_game:
                    now = time.time()
                    if now >= next_event:
                        self.root.after(0, self.show_minigame_popup)
                        next_event = now + EVENT_INTERVAL_SECONDS
                time.sleep(1)
            except:
                time.sleep(2)
    
    def show_minigame_popup(self):
        """Popup de minijuego (ÚNICO CON X)"""
        if self.minigame_popup or self.current_game:
            return
        
        self.minigame_popup = tk.Toplevel(self.root)
        self.minigame_popup.title("¡Minijuego!")
        self.minigame_popup.geometry("350x180+500+300")
        self.minigame_popup.attributes("-topmost", True)
        self.minigame_popup.resizable(False, False)
        self.minigame_popup.protocol("WM_DELETE_WINDOW", self._popup_closed)
        
        response = {'value': None}
        
        tk.Label(self.minigame_popup,
                text="🎮 ¡Tu mascota quiere jugar! 🎮",
                font=("Arial", 14, "bold"),
                fg="#2196F3").pack(pady=15)
        
        tk.Label(self.minigame_popup,
                text="¿Aceptas?",
                font=("Arial", 12)).pack(pady=10)
        
        def accept():
            response['value'] = True
            self.minigame_popup.destroy()
            self.minigame_popup = None
        
        def decline():
            response['value'] = False
            self.minigame_popup.destroy()
            self.minigame_popup = None
        
        btn_frame = tk.Frame(self.minigame_popup)
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="✓ Aceptar", command=accept,
                 font=("Arial", 11, "bold"), bg="#4CAF50", fg="white",
                 width=10, pady=5).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="✗ Rechazar", command=decline,
                 font=("Arial", 11), bg="#f44336", fg="white",
                 width=10, pady=5).pack(side="right", padx=10)
        
        def wait_response():
            start = time.time()
            while time.time() - start < POPUP_RESPONSE_TIMEOUT and response['value'] is None:
                time.sleep(0.5)
            
            if response['value'] is None:
                try:
                    self.minigame_popup.destroy()
                    self.minigame_popup = None
                except:
                    pass
                self.change_stat('felicidad', -20)
                return
            
            if response['value'] is False:
                self.change_stat('felicidad', -10)
                return
            
            self.change_stat('felicidad', 10)
            self.root.after(100, self.launch_minigame)
        
        threading.Thread(target=wait_response, daemon=True).start()
    
    def _popup_closed(self):
        """Cerró popup con X"""
        try:
            self.minigame_popup.destroy()
            self.minigame_popup = None
        except:
            pass
        self.change_stat('felicidad', -20)
    
    def launch_minigame(self, specific_game=None):
        """Lanza minijuego"""
        if self.current_game:
            return
        
        canvas = self.game_overlay.create()
        
        games = [MathQuiz, MemoryGame, StroopGame]
        game_class = specific_game if specific_game else random.choice(games)
        
        try:
            self.current_game = game_class(canvas, self._minigame_callback)
            self.current_game.run()
        except Exception as e:
            print(f"Error: {e}")
            self.current_game = None
            self.game_overlay.destroy()
    
    def _minigame_callback(self, result):
        """Callback de minijuego"""
        self.current_game = None
        self.game_overlay.destroy()
        
        if result == 'won':
            self.open_good_roulette()
        elif result == 'lost':
            self.change_stat('felicidad', -10)
            self.open_bad_roulette()
    
    def open_good_roulette(self):
        """Ruleta buena"""
        canvas = self.game_overlay.create()
        sectors = [
            ("+10% felicidad", ('felicidad', 10)),
            ("+25% felicidad", ('felicidad', 25)),
            ("Restaura hambre", ('hambre', 15)),
            ("Restaura higiene", ('higiene', 15)),
            ("Restaura sueño", ('sueno', 10)),
            ("Inmunidad 1h", ('immunity', 0))
        ]
        Roulette(canvas, sectors, self._roulette_callback, "🎉 RULETA PREMIO 🎉")
    
    def open_bad_roulette(self):
        """Ruleta mala"""
        canvas = self.game_overlay.create()
        sectors = [
            ("-15% felicidad", ('felicidad', -15)),
            ("-30% felicidad", ('felicidad', -30)),
            ("-50% felicidad", ('felicidad', -50)),
            ("Bloqueo comida", ('block', 0)),
            ("Bloqueo higiene", ('block', 0)),
            ("Bloqueo sueño", ('block', 0)),
            ("💀 MUERTE", ('death', 0))
        ]
        Roulette(canvas, sectors, self._roulette_callback, "💀 RULETA CASTIGO 💀")
    
    def _roulette_callback(self, payload):
        """Callback ruleta"""
        action, value = payload
        
        if action in ['felicidad', 'hambre', 'higiene', 'sueno']:
            self.change_stat(action, value)
        elif action == 'death':
            self.die("Ruleta de mala suerte")
        
        self.game_overlay.destroy()
    
    def _check_death(self):
        """Verifica muerte"""
        if not self.alive:
            return
        
        if self.hambre <= HUNGER_DEATH_MIN:
            self.die("Hambre (0%)")
        elif self.hambre > HUNGER_DEATH_MAX:
            self.die("Sobrealimentación (>90%)")
        elif self.sueno <= 0:
            self.die("Agotamiento")
        elif self.higiene <= 0:
            self.die("Falta de higiene")
        elif self.felicidad <= 0:
            self.die("Tristeza - Suicidio")
    
    def die(self, cause):
        """Muerte"""
        self.alive = False
        messagebox.showerror("GAME OVER", f"💀 Mascota muerta 💀\n\nCausa: {cause}")
        self.root.quit()
    
    def feed_pet(self):
        """Alimentar"""
        if not self.alive or self.sleeping:
            return
        self.change_stat('hambre', FEED_INCREASE)
    
    def shower_pet(self):
        """Duchar"""
        if not self.alive or self.sleeping:
            return
        self.change_stat('higiene', SHOWER_INCREASE)
    
    def toggle_sleep(self):
        """Dormir ON/OFF"""
        if not self.alive:
            return
        
        if self.sleeping:
            # Despertar
            elapsed = time.time() - self.sleep_start_time
            hours = elapsed / 3600
            
            messagebox.showinfo("Despertar", 
                f"⏰ Durmió {hours:.1f} horas\n"
                f"💤 Sueño actual: {self.sueno}%\n\n"
                f"{'✅ Buen descanso' if 6 <= hours <= 8 else '⚠️ Tiempo no óptimo'}")
            
            self.sleeping = False
            self.sleep_start_time = None
        else:
            # Dormir
            self.sleeping = True
            self.sleep_start_time = time.time()
            messagebox.showinfo("Dormir", 
                "💤 La mascota está durmiendo...\n\n"
                "⏰ El sueño aumentará gradualmente\n"
                "⏰ Óptimo: 7-8 horas\n"
                "⚠️ >8h = Pierde felicidad\n\n"
                "Usa el botón 'Despertar' para levantarla")
        
        self._update_sleep_button_color()
    
    def open_admin(self):
        """Panel admin"""
        password = simpledialog.askstring("Admin", "Clave:", show="*")
        
        if password != ADMIN_CODE:
            messagebox.showerror("Error", "Clave incorrecta")
            return
        
        admin_win = tk.Toplevel(self.root)
        admin_win.title("Panel Admin")
        admin_win.geometry("300x350")
        admin_win.attributes("-topmost", True)
        
        tk.Label(admin_win, text="🔧 ADMIN 🔧",
                font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(admin_win, text="Forzar minijuego:",
                font=("Arial", 10, "bold")).pack(pady=5)
        
        tk.Button(admin_win, text="📚 Quiz", command=lambda: self.launch_minigame(MathQuiz), width=20).pack(pady=3)
        tk.Button(admin_win, text="🧠 Memoria", command=lambda: self.launch_minigame(MemoryGame), width=20).pack(pady=3)
        tk.Button(admin_win, text="⚡ Stroop", command=lambda: self.launch_minigame(StroopGame), width=20).pack(pady=3)
        
        tk.Frame(admin_win, height=2, bg="#555").pack(fill="x", pady=10)
        
        tk.Button(admin_win, text="💚 Restaurar 100%", command=self.restore_stats, width=20, bg="#4CAF50", fg="white").pack(pady=5)
        tk.Button(admin_win, text="☀️ Despertar", command=lambda: setattr(self, 'sleeping', False), width=20, bg="#FF9800", fg="white").pack(pady=5)
        tk.Button(admin_win, text="❌ SALIR", command=self.root.quit, width=20, bg="#f44336", fg="white").pack(pady=5)
    
    def restore_stats(self):
        """Restaurar stats"""
        self.hambre = 100
        self.sueno = 100
        self.higiene = 100
        self.felicidad = 100
        self.update_display()
        messagebox.showinfo("Admin", "Stats al 100%")

def main():
    root = tk.Tk()
    app = CountdownPet(root)
    app.update_display()
    
    print("\n" + "="*60)
    print("🐾 COUNTDOWN PET INICIADO")
    print("="*60)
    print("✅ Panel de control: Visible")
    print("✅ Mascota flotante: SOBRE TODA LA PANTALLA")
    print("📁 Sprite: assets/sprites/pet.png")
    print("="*60 + "\n")
    
    root.mainloop()

if __name__ == "__main__":
    main()
