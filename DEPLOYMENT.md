# Nasazení Xpense na Android

## Příprava prostředí

### 1. Instalace Android SDK
```bash
# Stažení a instalace Android SDK
# Doporučujeme Android Studio pro jednoduchost
```

### 2. Nastavení proměnných prostředí
```bash
# Windows
set ANDROIDSDK=C:\path\to\android-sdk
set ANDROIDNDK=C:\path\to\android-ndk
set ANDROIDAPI=33
set ANDROIDMINAPI=21
```

### 3. Instalace Java JDK
```bash
# Stažení Oracle JDK 8 nebo OpenJDK 8
# Nastavení JAVA_HOME
```

## Build proces

### 1. Inicializace buildozer (pouze jednou)
```bash
buildozer init
```

### 2. Vytvoření debug APK
```bash
buildozer android debug
```

### 3. Vytvoření release APK
```bash
buildozer android release
```

## Optimalizace pro produkci

### 1. Podepsání APK
```bash
# Vytvoření keystore
keytool -genkey -v -keystore xpense.keystore -alias xpense -keyalg RSA -keysize 2048 -validity 10000

# Podepsání APK
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore xpense.keystore bin/xpense-*-release-unsigned.apk xpense
```

### 2. Optimalizace APK
```bash
# Zarovnání APK pro optimalizaci
zipalign -v 4 bin/xpense-*-release-unsigned.apk bin/xpense-release.apk
```

## Řešení problémů

### Build chyby
- Zkontrolujte verze SDK, NDK a API level v buildozer.spec
- Ujistěte se, že máte dostatek místa na disku (min. 5GB)
- Vyčistěte build cache: `buildozer clean`

### Runtime chyby
- Kontrola logů: `adb logcat | grep python`
- Debug na zařízení: `buildozer android debug deploy run logcat`

### Výkon
- Použijte release build pro lepší výkon
- Optimalizujte obrázky a resources
- Minimalizujte importy v main.py

## Testování na zařízení

### 1. Povolení Developer Options
- Nastavení > O telefonu > Klepněte 7x na Build number
- Povolte USB debugging

### 2. Instalace APK
```bash
# Instalace přes ADB
adb install bin/xpense-*-debug.apk

# Nebo přenos APK na zařízení a ruční instalace
```

### 3. Debugging
```bash
# Sledování logů aplikace
adb logcat | grep -i xpense
```

## Distribuce

### Google Play Store
1. Vytvořte release APK s podpisem
2. Vyplňte metadata aplikace
3. Nahrajte APK do Play Console
4. Nastavte cenu a dostupnost
5. Publikujte aplikaci

### Alternativní distribuce
- F-Droid (open-source aplikace)
- Amazon Appstore
- Přímé stažení APK ze stránek

## Aktualizace aplikace

### Postup aktualizace
1. Zvyšte verzi v buildozer.spec
2. Proveďte změny v kódu
3. Otestujte funkčnost
4. Vytvořte nový release build
5. Nahrajte do obchodu

### Správa verzí
```bash
# buildozer.spec
version = 1.1
version.regex = __version__ = ['"]([^'"]*)['"‌]
version.filename = %(source.dir)s/main.py
```

---

*Tento dokument poskytuje kompletní návod pro nasazení Xpense aplikace na Android zařízení.*
