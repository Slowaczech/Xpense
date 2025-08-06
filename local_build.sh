#!/bin/bash
# Lokální build script pro WSL Ubuntu

set -e

echo "🚀 Xpense APK Build Script pro WSL"
echo "=================================="

# Kontrola prostředí
if [[ ! "$OSTYPE" =~ ^linux ]]; then
    echo "❌ Tento script je určen pro Linux/WSL!"
    exit 1
fi

# Instalace závislostí
echo "📦 Instalace systémových závislostí..."
sudo apt update
sudo apt install -y \
    python3-pip \
    python3-dev \
    python3-setuptools \
    git \
    zip \
    unzip \
    default-jdk \
    build-essential \
    libffi-dev \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    autotools-dev \
    autoconf \
    libtool

# Instalace Python balíčků
echo "🐍 Instalace Python balíčků..."
pip3 install --user --upgrade pip setuptools wheel
pip3 install --user buildozer==1.4.0
pip3 install --user cython==0.29.33
pip3 install --user kivy==2.1.0
pip3 install --user kivymd==1.1.1

# Přidání do PATH
export PATH=$PATH:~/.local/bin

# Vytvoření minimální buildozer.spec
echo "⚙️ Vytváření buildozer.spec..."
cat > buildozer.spec << 'EOF'
[app]
title = Xpense
package.name = xpense  
package.domain = org.example.xpense

source.dir = .
source.main = test_app.py

version = 1.0

requirements = python3,kivy

orientation = portrait

[app:android]
android.api = 30
android.minapi = 21
android.ndk = 23b
android.accept_sdk_license = True
android.arch = armeabi-v7a

[buildozer]
log_level = 2
EOF

# Test aplikace
echo "🧪 Test aplikace..."
if [[ ! -f "test_app.py" ]]; then
    cat > test_app.py << 'EOF'
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

class TestApp(MDApp):
    def build(self):
        return MDLabel(text="Hello from Xpense!", halign="center")

TestApp().run()
EOF
fi

# Build
echo "🔨 Spouštění buildozer..."
echo "Toto může trvat 20-60 minut při prvním spuštění..."

~/.local/bin/buildozer android debug --verbose

echo "✅ Build dokončen!"
echo "APK soubor je v: bin/"
ls -la bin/

echo ""
echo "📱 Pro instalaci na Android zařízení:"
echo "adb install bin/*.apk"
