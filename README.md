# Ollama CLI Manager

Una herramienta interactiva de consola (CLI) escrita en Python para gestionar, ejecutar e instalar fácilmente modelos de Inteligencia Artificial locales usando [Ollama](https://ollama.com/).

## 🚀 Características
- **Interfaz colorida y profesional**: Fácil de leer y navegar usando menús.
- **Instalación fácil de archivos `.gguf` locales**: Automatiza la creación y limpieza del `Modelfile`. Además formatea correctamente los nombres para evitar errores en Ollama.
- **Descargas oficiales**: Descarga modelos directamente desde la biblioteca oficial.
- **Gestión total**: Lista, ejecuta, copia, elimina e inspecciona detalles de tus modelos de IA.
- **Servidor local**: Inicia el servidor de Ollama con un solo botón en caso de que esté apagado.

## 🛠️ Requisitos
- [Ollama](https://ollama.com/download) instalado en tu sistema y configurado en tus variables de entorno (PATH).
- *Opcional:* Python 3 si deseas ejecutar el script original, aunque no es necesario si usas la versión `.exe`.

## 💻 Instalación y Uso Rápido

### Opción 1: Archivo Ejecutable Portátil (Recomendada para Windows)
Simplemente descarga o compila el archivo `ollama_manager.exe` y haz doble clic sobre él. ¡Es totalmente portátil y no requiere Python!

### Opción 2: Ejecutar el script fuente de Python
Abre tu terminal y ejecuta:
```bash
python ollama_manager.py
```

## ⚙️ ¿Cómo compilar tu propio .exe?
Puedes generar el ejecutable a partir del código fuente usando `PyInstaller`.
1. Abre tu consola y navega hasta la carpeta del proyecto.
2. Instala la librería necesaria:
```bash
pip install pyinstaller
```
3. Ejecuta el comando de compilación:
```bash
pyinstaller --onefile --icon=NONE ollama_manager.py
```
El archivo final `.exe` aparecerá automáticamente dentro de una nueva carpeta llamada `dist`.

## 📜 Licencia
Este proyecto utiliza la Licencia MIT. Puedes modificarlo y distribuirlo libremente.
