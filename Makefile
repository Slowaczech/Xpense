# Makefile pro Xpense aplikaci

# Instalace závislostí
install:
	pip install -r requirements.txt

# Spuštění aplikace
run:
	python main.py

# Spuštění testů
test:
	python -m unittest test_xpense.py -v

# Vytvoření debug APK pro Android
build-debug:
	buildozer android debug

# Vytvoření release APK pro Android  
build-release:
	buildozer android release

# Vyčištění build souborů
clean:
	buildozer clean
	rm -rf .buildozer/
	rm -rf bin/
	rm -f *.db

# Inicializace buildozer
init:
	buildozer init

# Kontrola kódu
lint:
	python -m flake8 main.py --max-line-length=100

# Všechny hlavní příkazy
.PHONY: install run test build-debug build-release clean init lint
