# 🚀 GitHub Actions Build - Krok za krokem

## 📋 **RYCHLÝ NÁVOD:**

### **1. Vytvořte GitHub repository**
1. Jděte na [github.com](https://github.com) a přihlaste se
2. Klikněte **"New repository"**
3. Název: `xpense` nebo `xpense-app`
4. Nastavte **Public** (pro GitHub Actions zdarma)
5. **NEVYTVÁŘEJTE** README, .gitignore, ani licenci
6. Klikněte **"Create repository"**

### **2. Nahrajte projekt z PowerShell:**

```powershell
# Přejděte do složky projektu
cd c:\Xpense

# Inicializujte git (pokud ještě není)
git init

# Přidejte všechny soubory
git add .

# Vytvořte první commit
git commit -m "🎉 Initial commit - Xpense Android app"

# Připojte k GitHub repository (ZMĚŇTE URL!)
git remote add origin https://github.com/VASE_JMENO/xpense.git

# Nahrajte na GitHub
git push -u origin main
```

### **3. Automatické sestavení se spustí!**

- ✅ **GitHub Actions se spustí automaticky**
- ⏱️ **Build trvá 15-25 minut**
- 📱 **APK bude ke stažení v "Releases"**

---

## 🎯 **CO SE STANE:**

### **Okamžitě po nahrání:**
1. **GitHub Actions se spustí** (záložka "Actions")
2. **Loguje se průběh** sestavení v reálném čase
3. **Instalují se závislosti** (Python, Java, Android SDK)

### **Po úspěšném sestavení:**
1. **APK se nahraje** do "Artifacts" (dočasně)
2. **Vytvoří se Release** s APK ke stažení
3. **Odešle se notifikace** (pokud máte zapnuté)

### **Pokud sestavení selže:**
1. **Chyba se zobrazí** v Actions logu
2. **Email notifikace** o chybě
3. **Můžete spustit znovu** tlačítkem "Re-run"

---

## 📱 **STAŽENÍ APK:**

### **Způsob 1 - GitHub Releases (doporučeno):**
1. Jděte na váš repository
2. Klikněte na **"Releases"** (vpravo)
3. Najděte nejnovější verzi
4. Stáhněte **`xpense-debug.apk`**

### **Způsob 2 - GitHub Actions Artifacts:**
1. Jděte na **"Actions"** záložku
2. Klikněte na úspěšný build (zelená ✅)
3. Scrollujte dolů na **"Artifacts"**
4. Stáhněte **"xpense-debug-apk"**

---

## 🔧 **TROUBLESHOOTING:**

### **Git není nainstalován:**
```powershell
# Stáhněte z: https://git-scm.com/download/win
# Nebo použijte chocolatey:
choco install git
```

### **Chyba "remote origin already exists":**
```powershell
git remote remove origin
git remote add origin https://github.com/VASE_JMENO/xpense.git
```

### **Build selže:**
- Zkontrolujte **Actions** log pro detaily
- Většinou pomůže **"Re-run failed jobs"**
- Může se stát při výpadku GitHub serverů

### **Nemáte GitHub účet:**
1. Registrace na [github.com](https://github.com) je **zdarma**
2. Žádná platba není potřeba
3. GitHub Actions má **2000 minut/měsíc zdarma**

---

## ⚡ **VÝHODY GITHUB ACTIONS:**

- ✅ **Žádné instalace** na vašem PC
- ✅ **Funguje na jakémkoliv** PC/Mac/Linux
- ✅ **Automatické** při každé změně
- ✅ **Zdarma** pro public repository
- ✅ **Profesionální** CI/CD řešení
- ✅ **Sdílení** APK s ostatními jednoduše

---

## 🎉 **VÝSLEDEK:**

- **Hotové APK** ready k instalaci
- **Professional Release** stránka
- **Automatic versioning** (v1.0.1, v1.0.2...)
- **Download statistics** (kolikrát staženo)
- **Changelog** pro každou verzi

**Vaše aplikace bude dostupná světu během 30 minut!** 🌍📱
