# Configuración del juego CountdownPet

# Intervalos de tiempo (en segundos)
EVENT_INTERVAL_SECONDS = 60   # Intervalo entre minijuegos (60s para pruebas, 14400 para 4h reales)
POPUP_RESPONSE_TIMEOUT = 60   # Timeout para responder popup (60s pruebas, 300s para 5min)

# Admin
ADMIN_CODE = "admin123"

# Desgaste de estadísticas (por hora)
HUNGER_DECAY_PER_HOUR = 5     # -5% hambre por hora
SLEEP_DECAY_PER_HOUR = 15     # -15% sueño por hora  
HYGIENE_DECAY_PER_2HOURS = 10 # -10% higiene cada 2 horas

# Reducción durante el sueño
SLEEP_DECAY_REDUCTION = 0.80  # 80% menos desgaste mientras duerme

# Límites
HUNGER_DEATH_MIN = 0
HUNGER_DEATH_MAX = 90  # Muerte por sobrealimentación
SLEEP_MIN_HOURS = 7    # Horas mínimas de sueño necesarias cada 24h
HAPPINESS_PENALTY_OVERSLEEP = 10  # -10% por cada hora extra de sueño

# Acciones
FEED_INCREASE = 25     # +25% hambre al alimentar
SHOWER_INCREASE = 40   # +40% higiene al duchar
SLEEP_RESTORE = 100    # Restaura sueño al 100%

# Configuración de ventana
ALWAYS_ON_TOP = True
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
