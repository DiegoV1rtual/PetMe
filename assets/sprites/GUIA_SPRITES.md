# Sprites de la Mascota

## 📁 Ubicación
Todos los sprites van en esta carpeta: `assets/sprites/`

## 🎨 Sprites Necesarios

Cada sprite debe ser un archivo PNG de 150x150px.

### Estados Emocionales:

1. **normal.png** - Estado normal (verde)
2. **hambriento.png** - Con hambre (rojo claro)
3. **muy_hambriento.png** - Muriendo de hambre (rojo oscuro)
4. **gordo.png** - Sobrealimentado >90% (naranja)
5. **sucio.png** - Necesita ducha (marrón claro)
6. **muy_sucio.png** - Muy sucio (marrón oscuro)
7. **cansado.png** - Necesita dormir (gris claro)
8. **agotado.png** - Agotamiento extremo (gris oscuro)
9. **feliz.png** - Feliz (amarillo brillante)
10. **muy_feliz.png** - Muy feliz (dorado)
11. **triste.png** - Triste (azul claro)
12. **muy_triste.png** - Muy triste (azul oscuro)
13. **durmiendo.png** - Durmiendo (morado)
14. **enfermo.png** - 2+ stats bajas (verde enfermizo)
15. **muriendo.png** - 3+ stats críticas (negro)

## 🎯 Lógica de Estados

La mascota cambia de sprite automáticamente según:

- **Hambre ≥ 90%** → gordo
- **Hambre ≤ 10%** → muy_hambriento
- **Hambre ≤ 30%** → hambriento
- **Higiene ≤ 10%** → muy_sucio
- **Higiene ≤ 30%** → sucio
- **Sueño ≤ 10%** → agotado
- **Sueño ≤ 30%** → cansado
- **Felicidad ≤ 10%** → muy_triste
- **Felicidad ≤ 30%** → triste
- **Felicidad ≥ 80%** → muy_feliz
- **Felicidad ≥ 60%** → feliz
- **Durmiendo** → durmiendo
- **3+ stats < 40%** → muriendo
- **2+ stats < 40%** → enfermo
- **Resto** → normal

## 💡 Si no tienes sprites

El juego usará **cuadrados de colores con texto** automáticamente.

Los sprites son opcionales pero recomendados para mejor experiencia visual.

## 🎨 Formato Recomendado

- **Tamaño**: 150x150px
- **Formato**: PNG con transparencia
- **Estilo**: Pixel art, cartoon, lo que quieras
- **Fondo**: Transparente

## 📝 Ejemplo de Nombres

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
└── muriendo.png
```

¡El juego detectará y usará automáticamente los sprites que coloques aquí!
