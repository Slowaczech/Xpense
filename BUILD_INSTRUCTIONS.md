# 🚀 Sestavení Android APK - Návod

## 📱 **3 způsoby jak sestavit APK:**

### **1. WSL (Windows Subsystem for Linux) - DOPORUČENO**

#### Po restartu počítače:
```powershell
# 1. Otevřete PowerShell jako Administrator a dokončete instalaci
wsl --install Ubuntu

# 2. Po instalaci Ubuntu spusťte WSL
wsl

# 3. V Ubuntu terminal nainstalujte závislosti:
sudo apt update
sudo apt install -y python3-pip python3-venv git openjdk-8-jdk \
  autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
  libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 4. Nastavte JAVA_HOME
echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64' >> ~/.bashrc
echo 'export PATH=$PATH:$JAVA_HOME/bin' >> ~/.bashrc
source ~/.bashrc

# 5. Instalujte buildozer
pip3 install buildozer

# 6. Přejděte do složky projektu (nahraďte cestu)
cd /mnt/c/Xpense

# 7. Sestavte APK
buildozer android debug
```

**✅ Výsledek:** APK bude v složce `bin/xpense-1.0-armeabi-v7a-debug.apk`

---

### **2. GitHub Actions - AUTOMATICKÉ**

#### Nahrajte projekt na GitHub:
```bash
# 1. Vytvořte nový repository na GitHub.com
# 2. V PowerShell:
cd c:\Xpense
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/VASHE_JMENO/xpense.git
git push -u origin main
```

**✅ Výsledek:** APK se automaticky sestaví a bude ke stažení v GitHub Releases

---

### **3. Docker - ALTERNATIVA**

```bash
# Pokud máte Docker Desktop
cd c:\Xpense
docker run --rm -v ${PWD}:/workspace kivy/buildozer android debug
```

---

## 📋 **Co budete potřebovat:**

### Pro WSL:
- ✅ Windows 10/11 s WSL2
- ✅ ~2GB volného místa
- ✅ Internetové připojení
- ⏰ Čas: 20-40 minut (první sestavení)

### Pro GitHub:
- ✅ GitHub účet (zdarma)
- ✅ Git nainstalovaný
- ⏰ Čas: 15-25 minut (automatické)

---

## 🎯 **Doporučený postup:**

1. **Restartujte počítač** (kvůli WSL)
2. **Zvolte WSL metodu** (nejspolehlivější)
3. **Backup GitHub** jako alternativu

---

## 📱 **Instalace APK na telefon:**

1. Přeneste APK na telefon (USB/email/cloud)
2. **Nastavení → Zabezpečení → Neznámé zdroje** ✅
3. Otevřete APK soubor
4. Potvrďte instalaci

---

## ⚠️ **Troubleshooting:**

### Chyba "JAVA_HOME not set":
```bash
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```

### Chyba při sestavování:
```bash
# Vyčistěte build cache
buildozer android clean
buildozer android debug
```

### WSL problémy:
```powershell
# Reset WSL
wsl --unregister Ubuntu
wsl --install Ubuntu
```

---

## 📊 **Očekávané výsledky:**

- **Velikost APK:** ~15-25 MB
- **Čas sestavení:** 20-40 minut (první vez)
- **Minimální Android:** 5.0 (API 21)
- **Target Android:** 11.0 (API 30)

---

**🎉 Úspěch!** Vaše aplikace bude připravena k instalaci na Android zařízení!
