# Xpense - Aplikace pro správu financí

Moderní Android aplikace vyvinutá v Pythonu s Kivy frameworkem pro efektivní správu osobních financí.

## 📱 Funkce

- **Zadání základních údajů**: Výše příjmu, den výplaty, aktuální stav financí
- **Pravidelné výdaje**: Evidování až 20 pravidelných výdajů s názvem a dnem splatnosti
- **Denní rozpočet**: Automatický výpočet dostupných financí na každý den do výplaty
- **Responzivní design**: Optimalizované UI pro mobilní telefony
- **Offline funkcionalita**: Veškerá data uložena lokálně v SQLite databázi

## 🚀 Technologie

- **Python 3.9+**
- **Kivy 2.1.0** - Cross-platform GUI framework
- **KivyMD 1.1.1** - Material Design komponenty
- **SQLite** - Lokální databáze
- **Buildozer 1.5.0** - Build tool pro Android

## 📋 Požadavky

```bash
# Hlavní závislosti
pip install kivy==2.1.0
pip install kivymd==1.1.1
pip install buildozer==1.5.0
```

## 🔧 Instalace a spuštění

### Lokální testování
```bash
# Naklonování projektu
cd c:\Xpense

# Instalace závislostí
pip install -r requirements.txt

# Spuštění aplikace
python main.py

# Rychlý test layoutu (volitelné)
python layout_test.py
```

### Build pro Android
```bash
# Inicializace buildozer (pouze při prvním použití)
buildozer init

# Build debug APK
buildozer android debug

# Build release APK
buildozer android release
```

## 📊 Struktura projektu

```
Xpense/
├── main.py                 # Hlavní aplikační soubor
├── requirements.txt        # Python závislosti
├── buildozer.spec         # Konfigurace pro Android build
├── xpense.db              # SQLite databáze (vytvoří se automaticky)
├── README.md              # Dokumentace
└── .github/
    └── copilot-instructions.md
```

## 🎯 Použití

### 1. První spuštění
- Přejděte do **Nastavení** (ikona ozubeného kola)
- Zadejte měsíční příjem, den výplaty a aktuální zůstatek
- Uložte nastavení

### 2. Přidání výdajů
- Přejděte do **Pravidelné výdaje** (ikona kreditní karty)
- Klikněte na **+** pro přidání nového výdaje
- Zadejte název, částku a den splatnosti v měsíci

### 3. Sledování rozpočtu
- Na hlavní obrazovce vidíte:
  - **Denní rozpočet** - kolik můžete utratit denně
  - **Dny do výplaty** - zbývající dny do příští výplaty
  - **Zbývající výdaje** - suma všech nadcházejících pravidelných výdajů

## 💡 Logika výpočtu

Aplikace počítá denní rozpočet podle vzorce:
```
Denní rozpočet = (Aktuální zůstatek - Zbývající pravidelné výdaje) / Dny do výplaty
```

**Příklad:**
- Aktuální zůstatek: 15 000 Kč
- Zbývající výdaje do výplaty: 8 000 Kč  
- Dní do výplaty: 14
- **Denní rozpočet**: (15 000 - 8 000) / 14 = 500 Kč/den

## 🔒 Zabezpečení dat

- Všechna data jsou uložena lokálně na zařízení
- Žádné odesílání dat na servery
- Databáze je chráněna na úrovni file systému Android

## ⚡ Optimalizace

- **Databázové indexy** pro rychlé dotazy
- **Minimalistické UI** pro plynulý chod na slabších zařízeních
- **Lazy loading** komponent
- **Paměťově efektivní** SQLite operace

## 🐛 Řešení problémů

### Aplikace se nespustí
- Zkontrolujte instalaci Kivy: `pip show kivy`
- Ujistěte se, že máte Python 3.9+

### Build pro Android selhává
- Aktualizujte buildozer: `pip install --upgrade buildozer`
- Zkontrolujte Android SDK v `~/.buildozer/`

### Chyba databáze
- Smažte soubor `xpense.db` - vytvoří se nový při spuštění

## 📝 Plánované funkce

- [ ] Export dat do CSV
- [ ] Grafické přehledy výdajů
- [ ] Kategorie výdajů
- [ ] Notifikace před splatností výdajů
- [ ] Témata (tmavý/světlý režim)

## 📄 Licence

Tento projekt je open-source. Volně použitelný pro osobní i komerční účely.

## 👨‍💻 Autor

Vytvořeno pro efektivní správu osobních financí s důrazem na jednoduchost a rychlost.

---

*Verze 0.1 - Android aplikace pro správu denního rozpočtu*
