@echo off
echo 🚀 Xpense APK Build Helper pro Windows
echo ====================================

echo.
echo Tento script vám pomůže spustit build ve WSL.
echo.

echo 🔍 Kontrola WSL...
wsl --list --verbose > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ WSL není nainstalováno!
    echo Nainstalujte WSL2 s Ubuntu:
    echo wsl --install -d Ubuntu
    echo.
    pause
    exit /b 1
)

echo ✅ WSL nalezeno

echo.
echo 📁 Kopírování souborů do WSL...
wsl cp /mnt/c/Xpense/*.py ~/xpense/ 2>nul || wsl mkdir -p ~/xpense
wsl cp /mnt/c/Xpense/*.py ~/xpense/
wsl cp /mnt/c/Xpense/local_build.sh ~/xpense/
wsl chmod +x ~/xpense/local_build.sh

echo.
echo 🚀 Spouštění build scriptu ve WSL...
echo POZOR: První build může trvat 30-60 minut!
echo.
wsl cd ~/xpense && ./local_build.sh

echo.
echo 📱 Kopírování APK zpět do Windows...
wsl cp ~/xpense/bin/*.apk /mnt/c/Xpense/ 2>nul
if exist "*.apk" (
    echo ✅ APK úspěšně vytvořen!
    dir *.apk
) else (
    echo ❌ APK nebyl nalezen. Zkontrolujte logy výše.
)

echo.
pause
