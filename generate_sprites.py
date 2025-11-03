#!/usr/bin/env python3
"""
Generador de sprites de ejemplo para CountdownPet
Genera cuadrados de colores con texto para cada estado emocional
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    # Configuración de sprites
    SIZE = 150
    SPRITES = {
        "normal": {"color": (76, 175, 80), "text": "😊\nNORMAL", "text_color": (255, 255, 255)},
        "hambriento": {"color": (255, 107, 107), "text": "😫\nHAMBRE", "text_color": (255, 255, 255)},
        "muy_hambriento": {"color": (211, 47, 47), "text": "😵\nMUERO DE\nHAMBRE", "text_color": (255, 255, 255)},
        "gordo": {"color": (255, 152, 0), "text": "🤢\nGORDO", "text_color": (255, 255, 255)},
        "sucio": {"color": (139, 69, 19), "text": "🤮\nSUCIO", "text_color": (255, 255, 255)},
        "muy_sucio": {"color": (93, 64, 55), "text": "💩\nASQUEROSO", "text_color": (255, 255, 255)},
        "cansado": {"color": (158, 158, 158), "text": "😴\nCANSADO", "text_color": (255, 255, 255)},
        "agotado": {"color": (97, 97, 97), "text": "💤\nAGOTADO", "text_color": (255, 255, 255)},
        "feliz": {"color": (255, 215, 0), "text": "😄\n¡FELIZ!", "text_color": (0, 0, 0)},
        "muy_feliz": {"color": (255, 193, 7), "text": "🤩\n¡SÚPER\nFELIZ!", "text_color": (0, 0, 0)},
        "triste": {"color": (33, 150, 243), "text": "😢\nTRISTE", "text_color": (255, 255, 255)},
        "muy_triste": {"color": (21, 101, 192), "text": "😭\nMUY\nTRISTE", "text_color": (255, 255, 255)},
        "durmiendo": {"color": (126, 87, 194), "text": "😴\nZzz...", "text_color": (255, 255, 255)},
        "enfermo": {"color": (102, 187, 106), "text": "🤢\nENFERMO", "text_color": (255, 255, 255)},
        "muriendo": {"color": (66, 66, 66), "text": "☠️\nMURIENDO", "text_color": (255, 255, 255)}
    }
    
    def create_sprite(name, config):
        """Crea un sprite simple"""
        # Crear imagen con transparencia
        img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Dibujar cuadrado de fondo
        margin = 10
        draw.rectangle(
            [margin, margin, SIZE-margin, SIZE-margin],
            fill=config["color"] + (255,),
            outline=(255, 255, 255, 255),
            width=4
        )
        
        # Intentar cargar fuente
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        # Dibujar texto
        text = config["text"]
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (SIZE - text_width) // 2
        y = (SIZE - text_height) // 2
        
        draw.text((x, y), text, fill=config["text_color"] + (255,), font=font, align="center")
        
        return img
    
    # Crear directorio si no existe
    os.makedirs("assets/sprites", exist_ok=True)
    
    # Generar todos los sprites
    print("Generando sprites de ejemplo...")
    for name, config in SPRITES.items():
        img = create_sprite(name, config)
        filepath = f"assets/sprites/{name}.png"
        img.save(filepath)
        print(f"✅ Creado: {filepath}")
    
    print(f"\n🎉 ¡{len(SPRITES)} sprites generados correctamente!")
    print("📁 Ubicación: assets/sprites/")
    print("\n💡 Puedes reemplazarlos con tus propios diseños.")

except ImportError:
    print("❌ Error: Pillow no está instalado")
    print("Instala con: pip install pillow")
except Exception as e:
    print(f"❌ Error: {e}")
