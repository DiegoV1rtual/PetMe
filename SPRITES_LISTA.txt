# SPRITES REQUERIDOS PARA MINI-DIEGO

## Ubicacion
Todos los sprites van en: `assets/sprites/`

## Formato
- Tamano: 150x150px
- Formato: PNG con transparencia
- Estilo: Libre (pixel art, cartoon, etc)

---

## LISTA COMPLETA DE SPRITES (20 TOTAL)

### Estados Normales (15 sprites)

1. **normal.png** - Estado normal, saludable
2. **hambriento.png** - Con hambre (hambre < 30%)
3. **muy_hambriento.png** - Muriendo de hambre (hambre < 10%)
4. **gordo.png** - Sobrealimentado (hambre > 90%)
5. **sucio.png** - Necesita ducha (higiene < 30%)
6. **muy_sucio.png** - Muy sucio (higiene < 10%)
7. **cansado.png** - Necesita dormir (sueno < 30%)
8. **agotado.png** - Agotamiento extremo (sueno < 10%)
9. **feliz.png** - Feliz (felicidad >= 60%)
10. **muy_feliz.png** - Muy feliz (felicidad >= 80%)
11. **triste.png** - Triste (felicidad < 30%)
12. **muy_triste.png** - Muy triste (felicidad < 10%)
13. **durmiendo.png** - Durmiendo
14. **enfermo.png** - 2+ stats bajas (< 40%)
15. **muriendo.png** - 3+ stats criticas (< 40%)

### Sprites de Muerte Especificos (5 sprites NUEVOS)

16. **muerte_obesidad.png** - Muerte por sobrealimentacion (hambre > 90%)
17. **muerte_hambre.png** - Muerte por inanicion (hambre = 0%)
18. **muerte_sueno.png** - Muerte por falta de sueno (sueno = 0%)
19. **muerte_higiene.png** - Muerte por falta de higiene (higiene = 0%)
20. **muerte_tristeza.png** - Suicidio por tristeza extrema (felicidad = 0%)

---

## COLORES SUGERIDOS

### Estados Normales
- **normal**: Verde (#4CAF50)
- **hambriento**: Rojo claro (#FF6B6B)
- **muy_hambriento**: Rojo oscuro (#D32F2F)
- **gordo**: Naranja (#FF9800)
- **sucio**: Marron claro (#8B4513)
- **muy_sucio**: Marron oscuro (#5D4037)
- **cansado**: Gris claro (#9E9E9E)
- **agotado**: Gris oscuro (#616161)
- **feliz**: Amarillo (#FFD700)
- **muy_feliz**: Dorado (#FFC107)
- **triste**: Azul claro (#2196F3)
- **muy_triste**: Azul oscuro (#1565C0)
- **durmiendo**: Morado (#7E57C2)
- **enfermo**: Verde enfermizo (#66BB6A)
- **muriendo**: Negro/Gris muy oscuro (#424242)

### Sprites de Muerte
- **muerte_obesidad**: Rojo anaranjado (#FF5722)
- **muerte_hambre**: Marron grisaceo (#8D6E63)
- **muerte_sueno**: Gris azulado oscuro (#37474F)
- **muerte_higiene**: Marron muy oscuro (#3E2723)
- **muerte_tristeza**: Azul marino (#0D47A1)

---

## NOTAS IMPORTANTES

1. **SIN SPRITES**: Si no colocas sprites, el juego usa cuadrados de colores automaticamente
2. **OBLIGATORIOS**: Los 5 sprites de muerte son CRITICOS para mostrar correctamente el Game Over
3. **NOMBRES**: Los nombres de archivo DEBEN ser exactos (minusculas, guiones bajos)
4. **FUTURO**: Este sistema esta preparado para expandirse hasta 20+ minijuegos

---

## EJEMPLO DE ESTRUCTURA

```
assets/sprites/
├── normal.png
├── hambriento.png
├── muy_hambriento.png
├── gordo.png
├── sucio.png
├── muy_sucio.png
├── cansado.png
├── agotado.png
├── feliz.png
├── muy_feliz.png
├── triste.png
├── muy_triste.png
├── durmiendo.png
├── enfermo.png
├── muriendo.png
├── muerte_obesidad.png      [NUEVO]
├── muerte_hambre.png         [NUEVO]
├── muerte_sueno.png          [NUEVO]
├── muerte_higiene.png        [NUEVO]
└── muerte_tristeza.png       [NUEVO]
```

---

## GENERADOR AUTOMATICO

Ejecuta `python3 generate_sprites.py` para crear sprites de ejemplo automaticamente.
