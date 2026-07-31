# Código Batch para Ollama Manager

Puedes copiar el bloque de código de abajo y usarlo directamente en tu programa **Bat To Exe Converter**.

```bat
@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul

:: Definir colores ANSI
for /f %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"
set "CYAN=%ESC%[96m"
set "BLUE=%ESC%[94m"
set "GREEN=%ESC%[92m"
set "WARNING=%ESC%[93m"
set "RED=%ESC%[91m"
set "ENDC=%ESC%[0m"
set "BOLD=%ESC%[1m"

:main_menu
cls
echo %BLUE%%BOLD%
echo    ____  _ _                        __  __
echo   / __ \^| ^| ^|                      ^|  \/  ^|
echo  ^| ^|  ^| ^| ^| ^| __ _ _ __ ___   __ _ ^| \  / ^| __ __ __   __ _  __ _  ___ _ __ 
echo  ^| ^|  ^| ^| ^| ^|/ _` ^| '_ ` _ \ / _` ^|^| ^|\/^| ^|/ _` '_ \ / _` ^|/ _` ^|/ _ \ '__^|
echo  ^| ^|__^| ^| ^| ^| (_^| ^| ^| ^| ^| ^| ^| ^| (_^| ^|^| ^|  ^| ^| (_^| ^| ^| ^| ^| (_^| ^| (_^| ^|  __/ ^|
echo   \____/^|_^|_^|\__,_^|_^| ^|_^| ^|_^|\__,_^|^|_^|  ^|_^|\__,_^|_^| ^|_^|\__,_^|\__, ^|\___^|_^|
echo                                                               __/ ^|
echo                                                              ^|___/
echo %ENDC%
echo %CYAN%%BOLD%=== Sistema de Gestion Total para Ollama ===%ENDC%
echo.

echo %BOLD%1.%ENDC% Listar modelos instalados %GREEN%(ollama list)%ENDC%
echo %BOLD%2.%ENDC% Ejecutar / Hablar con un modelo %GREEN%(ollama run)%ENDC%
echo %BOLD%3.%ENDC% Descargar un modelo oficial %GREEN%(ollama pull)%ENDC%
echo %BOLD%4.%ENDC% Instalar un modelo desde archivo %GREEN%.gguf%ENDC%
echo %BOLD%5.%ENDC% Mostrar informacion detallada %GREEN%(ollama show)%ENDC%
echo %BOLD%6.%ENDC% Copiar o duplicar un modelo %GREEN%(ollama cp)%ENDC%
echo %BOLD%7.%ENDC% Eliminar un modelo %GREEN%(ollama rm)%ENDC%
echo %BOLD%8.%ENDC% Subir un modelo %GREEN%(ollama push)%ENDC%
echo %BOLD%9.%ENDC% Iniciar el servidor de Ollama %GREEN%(ollama serve)%ENDC%
echo %BOLD%10.%ENDC% %RED%Salir%ENDC%
echo.

set "opcion="
set /p "opcion=%BLUE%Selecciona una opcion (1-10): %ENDC%"

if "%opcion%"=="1" goto list_models
if "%opcion%"=="2" goto run_model
if "%opcion%"=="3" goto pull_model
if "%opcion%"=="4" goto install_local_model
if "%opcion%"=="5" goto show_model
if "%opcion%"=="6" goto copy_model
if "%opcion%"=="7" goto remove_model
if "%opcion%"=="8" goto push_model
if "%opcion%"=="9" goto serve_ollama
if "%opcion%"=="10" goto end_script

echo.
echo %RED%✖ Opcion no valida.%ENDC%
goto pause_menu

:list_models
call :print_header "MODELOS INSTALADOS"
ollama list
goto pause_menu

:run_model
call :print_header "EJECUTAR / HABLAR CON UN MODELO"
ollama list
echo.
set /p "model=%BLUE%Ingresa el nombre del modelo a ejecutar: %ENDC%"
if "%model%"=="" goto pause_menu
echo.
echo %GREEN%Iniciando chat con '%model%'... (Escribe '/bye' para salir)%ENDC%
echo.
ollama run "%model%"
goto pause_menu

:pull_model
call :print_header "DESCARGAR MODELO OFICIAL"
echo %GREEN%Ejemplos: llama3, mistral, gemma...%ENDC%
set /p "model=%BLUE%Ingresa el nombre del modelo a descargar: %ENDC%"
if "%model%"=="" goto pause_menu
echo.
echo %CYAN%Descargando '%model%'...%ENDC%
ollama pull "%model%"
goto pause_menu

:install_local_model
call :print_header "INSTALAR MODELO DESDE ARCHIVO .GGUF"
set /p "model_name=%BLUE%Ingresa el nombre que le daras al modelo: %ENDC%"
if "%model_name%"=="" goto pause_menu

set /p "gguf_path=%BLUE%Ingresa la ruta completa del archivo .gguf: %ENDC%"
if "%gguf_path%"=="" goto pause_menu
:: Quitar comillas si las hay
set "gguf_path=%gguf_path:"=%"

if not exist "%gguf_path%" (
    echo.
    echo %RED%✖ Error: No se encontro el archivo en la ruta especificada.%ENDC%
    goto pause_menu
)

echo FROM "%gguf_path%" > Modelfile_temp.txt
echo.
echo %CYAN%Creando el modelo '%model_name%' en Ollama...%ENDC%
ollama create "%model_name%" -f Modelfile_temp.txt
if exist Modelfile_temp.txt del Modelfile_temp.txt
goto pause_menu

:show_model
call :print_header "INFORMACION DEL MODELO"
set /p "model=%BLUE%Ingresa el nombre del modelo a inspeccionar: %ENDC%"
if not "%model%"=="" (
    echo.
    ollama show "%model%"
)
goto pause_menu

:copy_model
call :print_header "COPIAR / DUPLICAR MODELO"
set /p "src=%BLUE%Modelo de origen: %ENDC%"
set /p "dest=%BLUE%Nuevo nombre del modelo: %ENDC%"
if not "%src%"=="" if not "%dest%"=="" (
    echo.
    echo %CYAN%Copiando '%src%' a '%dest%'...%ENDC%
    ollama cp "%src%" "%dest%"
)
goto pause_menu

:remove_model
call :print_header "ELIMINAR UN MODELO"
set /p "model=%BLUE%Ingresa el nombre del modelo a eliminar: %ENDC%"
if not "%model%"=="" (
    echo.
    set /p "confirm=%WARNING%¿Estas seguro de que deseas eliminar '%model%'? (s/n): %ENDC%"
    if /I "!confirm!"=="s" (
        echo %CYAN%Eliminando '%model%'...%ENDC%
        ollama rm "%model%"
    ) else (
        echo %CYAN%Operacion cancelada.%ENDC%
    )
)
goto pause_menu

:push_model
call :print_header "SUBIR UN MODELO (PUSH)"
set /p "model=%BLUE%Ingresa el nombre del modelo a subir: %ENDC%"
if not "%model%"=="" (
    echo.
    echo %CYAN%Subiendo '%model%' al registro...%ENDC%
    ollama push "%model%"
)
goto pause_menu

:serve_ollama
call :print_header "INICIAR SERVIDOR OLLAMA"
echo %CYAN%Iniciando el servidor 'ollama serve' en una nueva ventana...%ENDC%
start cmd /k "ollama serve"
echo.
echo %GREEN%✔ Se ha solicitado el inicio del servidor.%ENDC%
goto pause_menu

:print_header
cls
echo %CYAN%%BOLD%==================================================%ENDC%
echo %CYAN%%BOLD% %~1 %ENDC%
echo %CYAN%%BOLD%==================================================%ENDC%
echo.
exit /b

:pause_menu
echo.
set /p "dummy=%WARNING%Presiona Enter para volver al menu principal...%ENDC%"
goto main_menu

:end_script
cls
echo %GREEN%¡Gracias por usar el Sistema de Gestion para Ollama! Hasta luego.%ENDC%
exit /b
```
