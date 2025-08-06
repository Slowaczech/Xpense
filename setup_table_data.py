"""
Naplnění databáze daty z tabulky pro test nové logiky
"""
from main import DatabaseManager
from datetime import datetime
import os

def setup_test_data():
    print("🔧 NASTAVENÍ TESTOVACÍCH DAT Z TABULKY")
    print("=" * 50)
    
    # Smazání staré databáze
    db_path = "xpense.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        print("✅ Stará databáze smazána")
    
    # Vytvoření nové databáze
    db = DatabaseManager()
    
    # Nastavení uživatele (příjem 10000, výplata 15., balance 3000)
    db.save_user_settings(income=10000, payday=15, balance=3000)
    print("✅ Uživatelská nastavení uložena")
    
    # Data z tabulky
    expenses_data = [
        ("Alza (notebook)", 326, 1),
        ("PS Plus", 235, 6),
        ("Alza (monitor)", 138, 10),
        ("Alza Plus", 25, 15),
        ("Daň z nem.", 90, 15),
        ("Elektřina", 1290, 15),
        ("Hypotéka", 7282, 15),
        ("Léky", 300, 15),
        ("Mapy", 25, 15),
        ("Plyn", 250, 15),
        ("VZP", 105, 15),
        ("Byt", 2725, 17),
        ("Fond oprav", 1805, 17),
        ("Tidal", 55, 17),
        ("Pojištění Pillow", 268, 19),
        ("Vodafone", 780, 26),
    ]
    
    # Přidání výdajů do databáze
    print("\n💰 PŘIDÁVÁNÍ VÝDAJŮ:")
    total = 0
    for name, amount, day in expenses_data:
        db.add_expense(name, amount, day)
        total += amount
        print(f"  ✅ {name}: {amount} Kč (den {day})")
    
    print(f"\n📊 CELKEM VÝDAJŮ: {total} Kč")
    print("✅ Databáze úspěšně naplněna")
    
    db.close_connection()

if __name__ == "__main__":
    setup_test_data()
