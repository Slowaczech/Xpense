"""
Diagnostika aktuálního stavu aplikace
"""
import sqlite3
from main import FinanceCalculator, DatabaseManager
from datetime import datetime

def diagnose_current_state():
    print("🔍 DIAGNOSTIKA AKTUÁLNÍHO STAVU APLIKACE")
    print("=" * 50)
    
    # Připojení k databázi
    db = DatabaseManager()
    
    # Načtení nastavení
    income, payday, balance = db.get_user_settings()
    print(f"📊 NASTAVENÍ Z DATABÁZE:")
    print(f"   Příjem: {income} Kč")
    print(f"   Den výplaty: {payday}")
    print(f"   Aktuální zůstatek: {balance} Kč")
    
    # Načtení výdajů
    expenses = db.get_expenses()
    print(f"\n💰 VÝDAJE Z DATABÁZE:")
    total_expenses = 0
    for exp_id, name, amount, day in expenses:
        print(f"   {name}: {amount} Kč (den {day})")
        total_expenses += amount
    print(f"   CELKEM: {total_expenses} Kč")
    
    # Výpočet podle aktuální logiky
    current_day = datetime.now().day
    result = FinanceCalculator.calculate_daily_budget(
        income, balance, expenses, payday, current_day
    )
    
    print(f"\n🧮 VÝPOČET PODLE AKTUÁLNÍ LOGIKY:")
    print(f"   Aktuální den: {current_day}")
    print(f"   Dny do výplaty: {result['days_until_payday']}")
    print(f"   Zbývající výdaje: {result['remaining_expenses']} Kč")
    print(f"   Denní rozpočet: {result['daily_budget']:.0f} Kč")
    print(f"   Dostupné peníze: {result['available_money']} Kč")
    
    print(f"\n🎯 OČEKÁVANÉ HODNOTY:")
    print(f"   Denní rozpočet: 333 Kč")
    print(f"   Zbývající výdaje: 9740 Kč")
    print(f"   Dny do výplaty: 9")
    
    # Analýza problému
    print(f"\n❓ ANALÝZA PROBLÉMU:")
    if result['daily_budget'] == 0:
        print("   ⚠️  Denní rozpočet je 0 - možná chyba ve výpočtu nebo nastaveních")
    if result['remaining_expenses'] != 9740:
        print(f"   ⚠️  Zbývající výdaje {result['remaining_expenses']} ≠ očekáváno 9740")
    if total_expenses == 0:
        print("   ⚠️  Nejsou žádné výdaje v databázi!")
    if balance == 0:
        print("   ⚠️  Zůstatek je 0!")
    
    db.close_connection()

if __name__ == "__main__":
    diagnose_current_state()
