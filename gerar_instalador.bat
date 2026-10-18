@echo off
setlocal
cd /d "%~dp0"

set "APP_DIR=C:\PyCompostaBuild\dist\PyComposta"
set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" set "ISCC=%ProgramFiles%\Inno Setup 7\ISCC.exe"

if not exist "%APP_DIR%\PyComposta.exe" (
    echo ERRO: Executavel nao encontrado em:
    echo %APP_DIR%\PyComposta.exe
    pause
    exit /b 1
)
if not exist "instalador.iss" (
    echo ERRO: instalador.iss nao encontrado na mesma pasta deste BAT.
    pause
    exit /b 1
)
if not exist "%ISCC%" (
    echo ERRO: Inno Setup 6 nao encontrado.
    echo Abra instalador.iss no Inno Setup e compile manualmente.
    pause
    exit /b 1
)

echo Gerando instalador do PyComposta...
"%ISCC%" "instalador.iss"
if errorlevel 1 (
    echo ERRO: Falha na compilacao do instalador.
    pause
    exit /b 1
)
echo.
echo Instalador gerado com sucesso. Confira o OutputDir do instalador.iss.
pause
endlocal
