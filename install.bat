@echo off
echo ==========================================
echo    CountdownPet - Instalacion
echo ==========================================
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python no encontrado
    echo Por favor instala Python 3.7+
    pause
    exit /b 1
)

echo + Python encontrado
python --version
echo.

:: Instalar Pillow
echo Instalando dependencias...
pip install pillow

if errorlevel 1 (
    echo Intentando con --user...
    pip install --user pillow
)

echo.
echo ==========================================
echo    + Instalacion completada
echo ==========================================
echo.
echo Para ejecutar:
echo   python main.py
echo.
echo IMPORTANTE:
echo   - La ventana estara SIEMPRE VISIBLE
echo   - NO se puede cerrar con X
echo   - Usa Panel Admin (admin123) - Salir
echo.
echo Sistema de sueno:
echo   - Optimo: 7-8 horas
echo   - Mas de 8h: -10%% felicidad por hora extra
echo.
pause
