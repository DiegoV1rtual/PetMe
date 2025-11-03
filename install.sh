#!/bin/bash
# Instalación rápida de CountdownPet

echo "=========================================="
echo "   🐾 CountdownPet - Instalación 🐾"
echo "=========================================="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no encontrado"
    echo "Por favor instala Python 3.7+"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"
echo ""

# Instalar Pillow
echo "📦 Instalando dependencias..."
pip3 install pillow

if [ $? -eq 0 ]; then
    echo "✅ Pillow instalado"
else
    echo "⚠️  Intentando con --user..."
    pip3 install --user pillow
fi

echo ""
echo "=========================================="
echo "   ✅ Instalación completada"
echo "=========================================="
echo ""
echo "Para ejecutar:"
echo "  python3 main.py"
echo ""
echo "⚠️  IMPORTANTE:"
echo "  - La ventana estará SIEMPRE VISIBLE (always on top)"
echo "  - NO se puede cerrar con X"
echo "  - Usa Panel Admin (admin123) → Salir para cerrar"
echo ""
echo "😴 Sistema de sueño:"
echo "  - Óptimo: 7-8 horas"
echo "  - Más de 8h: -10% felicidad por hora extra"
echo ""
