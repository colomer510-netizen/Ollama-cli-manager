import os
import subprocess
import time
import sys

# Habilitar códigos ANSI en Windows (cmd y powershell)
if os.name == 'nt':
    os.system('color')

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    clear_screen()
    print(f"{Colors.CYAN}{Colors.BOLD}=================================================={Colors.ENDC}")
    print(f"{Colors.CYAN}{Colors.BOLD} {title.center(48)} {Colors.ENDC}")
    print(f"{Colors.CYAN}{Colors.BOLD}=================================================={Colors.ENDC}\n")

def pause():
    input(f"\n{Colors.WARNING}Presiona Enter para volver al menú principal...{Colors.ENDC}")

def run_ollama_command(args, capture=False):
    """Ejecuta un comando de Ollama y maneja los errores comunes."""
    try:
        if capture:
            result = subprocess.run(['ollama'] + args, check=True, text=True, capture_output=True)
            return True, result.stdout
        else:
            subprocess.run(['ollama'] + args, check=True)
            return True, None
    except subprocess.CalledProcessError as e:
        print(f"\n{Colors.RED}✖ Error al ejecutar el comando en Ollama.{Colors.ENDC}")
        if e.stderr:
            print(f"{Colors.RED}Detalles: {e.stderr.strip()}{Colors.ENDC}")
        return False, None
    except FileNotFoundError:
        print(f"\n{Colors.RED}✖ No se encuentra el comando 'ollama'.{Colors.ENDC}")
        print(f"{Colors.RED}Por favor, asegúrate de que Ollama está instalado y agregado al PATH del sistema.{Colors.ENDC}")
        return False, None
    except Exception as e:
        print(f"\n{Colors.RED}✖ Error inesperado: {e}{Colors.ENDC}")
        return False, None

def check_ollama_service():
    """Verifica silenciosamente si el servicio de Ollama responde."""
    try:
        # Se verifica solo ejecutando un comando básico y capturando la salida para no llenar la pantalla
        subprocess.run(['ollama', 'list'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        print(f"{Colors.RED}Advertencia: El servicio de Ollama no parece estar respondiendo o instalado.{Colors.ENDC}")
        print(f"{Colors.RED}Intenta iniciar el servidor (Opción 9).{Colors.ENDC}\n")

def list_models():
    print_header("MODELOS INSTALADOS")
    success, output = run_ollama_command(['list'], capture=True)
    if success:
        if output.strip():
            print(f"{Colors.GREEN}{output}{Colors.ENDC}")
        else:
            print(f"{Colors.WARNING}No hay modelos instalados actualmente.{Colors.ENDC}")

def run_model():
    print_header("EJECUTAR / HABLAR CON UN MODELO")
    success, output = run_ollama_command(['list'], capture=True)
    if success and output.strip():
        print(f"{Colors.GREEN}Modelos disponibles:{Colors.ENDC}")
        lines = output.strip().split('\n')[1:]
        for line in lines:
            if line:
                model_name = line.split()[0]
                print(f"  - {model_name}")
        
        print()
        model = input(f"{Colors.BLUE}Ingresa el nombre del modelo a ejecutar (ej. llama3): {Colors.ENDC}").strip()
        if model:
            print(f"\n{Colors.GREEN}Iniciando chat con '{model}'... (Escribe '/bye' para salir del chat){Colors.ENDC}\n")
            # Para run, queremos interacción directa, no capturamos salida
            run_ollama_command(['run', model], capture=False)
        else:
            print(f"{Colors.WARNING}Nombre de modelo no válido.{Colors.ENDC}")
    elif success:
        print(f"{Colors.WARNING}No tienes modelos instalados. ¡Descarga uno primero (Opción 3)!{Colors.ENDC}")

def pull_model():
    print_header("DESCARGAR MODELO OFICIAL")
    print(f"{Colors.GREEN}Ejemplos: llama3, mistral, gemma, phi3, llava, qwen...{Colors.ENDC}")
    model = input(f"{Colors.BLUE}Ingresa el nombre del modelo a descargar: {Colors.ENDC}").strip()
    if model:
        print(f"\n{Colors.CYAN}Descargando '{model}'... Esto puede tardar varios minutos según tu conexión y el tamaño del modelo.{Colors.ENDC}")
        success, _ = run_ollama_command(['pull', model], capture=False)
        if success:
            print(f"\n{Colors.GREEN}✔ Modelo '{model}' descargado exitosamente.{Colors.ENDC}")
    else:
         print(f"{Colors.WARNING}Nombre de modelo no válido.{Colors.ENDC}")

def install_local_model():
    print_header("INSTALAR MODELO DESDE ARCHIVO .GGUF")
    model_name = input(f"{Colors.BLUE}Ingresa el nombre que le darás al modelo en Ollama: {Colors.ENDC}").strip()
    if not model_name:
        print(f"{Colors.WARNING}Nombre inválido. Cancelando.{Colors.ENDC}")
        return

    # Ollama no permite espacios ni mayúsculas en los nombres de modelo
    model_name = model_name.replace(' ', '-').lower()

    gguf_path = input(f"{Colors.BLUE}Ingresa la ruta completa del archivo .gguf (ej. C:\\descargas\\modelo.gguf): {Colors.ENDC}").strip()
    
    # Limpiar la ruta por si el usuario la arrastró y soltó (puede contener comillas)
    gguf_path = gguf_path.strip('\"\'')
    
    if not os.path.isfile(gguf_path):
        print(f"\n{Colors.RED}✖ Error: No se encontró el archivo en la ruta especificada: {gguf_path}{Colors.ENDC}")
        return

    print(f"\n{Colors.CYAN}Generando Modelfile temporal...{Colors.ENDC}")
    modelfile_path = 'Modelfile_temp.txt'
    try:
        # En Windows, usar barras normales para el path dentro del Modelfile funciona bien
        # pero para asegurar, escapamos las barras invertidas
        formatted_path = gguf_path.replace('\\', '\\\\')
        with open(modelfile_path, 'w', encoding='utf-8') as f:
            f.write(f'FROM "{formatted_path}"\n')
        
        print(f"{Colors.CYAN}Creando el modelo '{model_name}' en Ollama (esto puede tomar un momento)...{Colors.ENDC}")
        success, _ = run_ollama_command(['create', model_name, '-f', modelfile_path], capture=False)
        
        if success:
            print(f"\n{Colors.GREEN}✔ Modelo local '{model_name}' instalado exitosamente.{Colors.ENDC}")
            
    except Exception as e:
        print(f"\n{Colors.RED}✖ Error al crear el modelo: {e}{Colors.ENDC}")
    finally:
        # Eliminar el archivo Modelfile temporal independientemente del resultado
        if os.path.exists(modelfile_path):
            try:
                os.remove(modelfile_path)
                print(f"{Colors.CYAN}Archivo temporal eliminado correctamente.{Colors.ENDC}")
            except Exception as e:
                 print(f"{Colors.WARNING}No se pudo eliminar el archivo temporal: {e}{Colors.ENDC}")

def show_model():
    print_header("INFORMACIÓN DEL MODELO")
    model = input(f"{Colors.BLUE}Ingresa el nombre del modelo a inspeccionar: {Colors.ENDC}").strip()
    if model:
        print()
        success, output = run_ollama_command(['show', model], capture=True)
        if success and output:
            print(f"{Colors.GREEN}{output}{Colors.ENDC}")
    else:
        print(f"{Colors.WARNING}Nombre de modelo no válido.{Colors.ENDC}")

def copy_model():
    print_header("COPIAR / DUPLICAR MODELO")
    src = input(f"{Colors.BLUE}Modelo de origen (ej. llama3): {Colors.ENDC}").strip()
    dest = input(f"{Colors.BLUE}Nuevo nombre del modelo (ej. mi_llama3): {Colors.ENDC}").strip()
    
    if src and dest:
        print(f"\n{Colors.CYAN}Copiando '{src}' a '{dest}'...{Colors.ENDC}")
        success, _ = run_ollama_command(['cp', src, dest], capture=False)
        if success:
            print(f"\n{Colors.GREEN}✔ Modelo copiado exitosamente.{Colors.ENDC}")
    else:
        print(f"{Colors.WARNING}Nombres inválidos. Cancelando.{Colors.ENDC}")

def remove_model():
    print_header("ELIMINAR UN MODELO")
    model = input(f"{Colors.BLUE}Ingresa el nombre del modelo a eliminar: {Colors.ENDC}").strip()
    if model:
        confirm = input(f"{Colors.WARNING}¿Estás seguro de que deseas eliminar '{model}' de tu sistema? (s/n): {Colors.ENDC}").strip().lower()
        if confirm == 's':
            print(f"\n{Colors.CYAN}Eliminando '{model}'...{Colors.ENDC}")
            success, _ = run_ollama_command(['rm', model], capture=False)
            if success:
                print(f"\n{Colors.GREEN}✔ Modelo '{model}' eliminado exitosamente.{Colors.ENDC}")
        else:
            print(f"\n{Colors.CYAN}Operación cancelada.{Colors.ENDC}")
    else:
        print(f"{Colors.WARNING}Nombre de modelo no válido.{Colors.ENDC}")

def push_model():
    print_header("SUBIR UN MODELO (PUSH)")
    print(f"{Colors.GREEN}Nota: El modelo debe tener el formato <tu_usuario>/<nombre_modelo>{Colors.ENDC}")
    model = input(f"{Colors.BLUE}Ingresa el nombre del modelo a subir: {Colors.ENDC}").strip()
    if model:
        print(f"\n{Colors.CYAN}Subiendo '{model}' al registro...{Colors.ENDC}")
        success, _ = run_ollama_command(['push', model], capture=False)
        if success:
            print(f"\n{Colors.GREEN}✔ Modelo '{model}' subido exitosamente.{Colors.ENDC}")
    else:
        print(f"{Colors.WARNING}Nombre de modelo no válido.{Colors.ENDC}")

def serve_ollama():
    print_header("INICIAR SERVIDOR OLLAMA")
    print(f"{Colors.CYAN}Iniciando el servidor 'ollama serve'...{Colors.ENDC}")
    try:
        if os.name == 'nt':
            # Ejecuta en una nueva ventana cmd que persiste
            subprocess.Popen('start cmd /k ollama serve', shell=True)
        else:
            # En Linux/Mac lo lanza en background
            subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print(f"\n{Colors.GREEN}✔ Se ha solicitado el inicio del servidor.{Colors.ENDC}")
        print(f"{Colors.GREEN}Si estás en Windows, se ha abierto una nueva ventana. Puedes cerrarla cuando quieras detener el servidor.{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.RED}✖ Error al intentar iniciar el servidor: {e}{Colors.ENDC}")

def main():
    while True:
        clear_screen()
        print(f"{Colors.BLUE}{Colors.BOLD}")
        print(r"""
   ____  _ _                        __  __                                   
  / __ \| | |                      |  \/  |                                  
 | |  | | | | __ _ _ __ ___   __ _ | \  / | __ __ __   __ _  __ _  ___ _ __  
 | |  | | | |/ _` | '_ ` _ \ / _` || |\/| |/ _` '_ \ / _` |/ _` |/ _ \ '__| 
 | |__| | | | (_| | | | | | | (_| || |  | | (_| | | | | (_| | (_| |  __/ |    
  \____/|_|_|\__,_|_| |_| |_|\__,_||_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|    
                                                              __/ |          
                                                             |___/           
        """)
        print(f"{Colors.ENDC}")
        print(f"{Colors.CYAN}{Colors.BOLD}=== Sistema de Gestión Total para Ollama ==={Colors.ENDC}\n")
        
        check_ollama_service()
        
        print(f"{Colors.BOLD}1.{Colors.ENDC} Listar modelos instalados {Colors.GREEN}(ollama list){Colors.ENDC}")
        print(f"{Colors.BOLD}2.{Colors.ENDC} Ejecutar / Hablar con un modelo {Colors.GREEN}(ollama run){Colors.ENDC}")
        print(f"{Colors.BOLD}3.{Colors.ENDC} Descargar un modelo oficial {Colors.GREEN}(ollama pull){Colors.ENDC}")
        print(f"{Colors.BOLD}4.{Colors.ENDC} Instalar un modelo desde archivo {Colors.GREEN}.gguf{Colors.ENDC}")
        print(f"{Colors.BOLD}5.{Colors.ENDC} Mostrar información detallada {Colors.GREEN}(ollama show){Colors.ENDC}")
        print(f"{Colors.BOLD}6.{Colors.ENDC} Copiar o duplicar un modelo {Colors.GREEN}(ollama cp){Colors.ENDC}")
        print(f"{Colors.BOLD}7.{Colors.ENDC} Eliminar un modelo {Colors.GREEN}(ollama rm){Colors.ENDC}")
        print(f"{Colors.BOLD}8.{Colors.ENDC} Subir un modelo {Colors.GREEN}(ollama push){Colors.ENDC}")
        print(f"{Colors.BOLD}9.{Colors.ENDC} Iniciar el servidor de Ollama {Colors.GREEN}(ollama serve){Colors.ENDC}")
        print(f"{Colors.BOLD}10.{Colors.ENDC} {Colors.RED}Salir{Colors.ENDC}\n")

        opcion = input(f"{Colors.BLUE}Selecciona una opción (1-10): {Colors.ENDC}").strip()

        if opcion == '1':
            list_models()
        elif opcion == '2':
            run_model()
        elif opcion == '3':
            pull_model()
        elif opcion == '4':
            install_local_model()
        elif opcion == '5':
            show_model()
        elif opcion == '6':
            copy_model()
        elif opcion == '7':
            remove_model()
        elif opcion == '8':
            push_model()
        elif opcion == '9':
            serve_ollama()
        elif opcion == '10':
            clear_screen()
            print(f"{Colors.GREEN}¡Gracias por usar el Sistema de Gestión para Ollama! Hasta luego.{Colors.ENDC}")
            break
        else:
            print(f"\n{Colors.RED}✖ Opción no válida. Por favor, selecciona un número del 1 al 10.{Colors.ENDC}")
        
        pause()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print(f"\n{Colors.GREEN}Saliendo del programa...{Colors.ENDC}")
        sys.exit(0)
