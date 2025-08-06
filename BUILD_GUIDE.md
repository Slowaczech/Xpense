# Xpense APK Build - Návod

## Možnosti build

Máte teď několik způsobů, jak zkusit vytvořit APK:

### 1. 🌐 GitHub Actions (Specialized)
Nejnovější workflow s marketplace akcí:
```bash
# Jděte na GitHub → Actions → "Build APK (Specialized Action)"
# Spusťte manuálně tlačítkem "Run workflow"
```

### 2. 🐧 Lokální build ve WSL
Nový automatizovaný script pro WSL:

**Windows PowerShell:**
```powershell
# Spusťte helper script
.\build_helper.bat
```

**Nebo manuálně ve WSL:**
```bash
# Kopírování do WSL
wsl
cd ~
mkdir xpense
cp /mnt/c/Xpense/*.py xpense/
cp /mnt/c/Xpense/local_build.sh xpense/
cd xpense
chmod +x local_build.sh

# Spuštění build
./local_build.sh
```

### 3. 🐳 GitHub Actions (Docker)
```bash
# Jděte na GitHub → Actions → "Build APK (Docker)"
# Spusťte manuálně
```

### 4. 🔧 GitHub Actions (Template)  
```bash
# Jděte na GitHub → Actions → "Build APK (Template)"
# Spusťte manuálně
```

## Co dělat při chybách

### GitHub Actions chyby
1. Stáhněte celý log ze záložky Actions
2. Hledejte konkrétní error message (ne jen exit code)
3. Zkontrolujte Requirements vs buildozer.spec

### WSL chyby
1. Ujistěte se, že máte WSL2 s Ubuntu
2. Zkontrolujte internet připojení
3. První build trvá 30-60 minut (downloading Android SDK)

### Obecné tipy
- Používejte Python 3.9 pro build (ne 3.13)
- Android API 30, NDK 23b jsou testované verze
- Minimální aplikace `test_app.py` by měla fungovat

## Testování APK
```bash
# Instalace na Android zařízení
adb install xpense.apk

# Nebo upload na telefon a instalace ručně
# (nezapomeňte povolit "Neznámé zdroje")
```

## Status workflows
- ✅ Standard workflow: Vytvořen, ale exit code 102
- ✅ Docker workflow: Vytvořen, čeká na test
- ✅ Specialized workflow: Vytvořen, čeká na test  
- ✅ Template workflow: Vytvořen, čeká na test
- ✅ Local WSL script: Vytvořen, připraven k použití

Doporučuji zkusit **lokální WSL build** - je to nejrychlejší způsob, jak získat pracovní APK.
