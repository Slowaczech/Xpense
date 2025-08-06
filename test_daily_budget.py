"""
Jednoduchý test denního rozpočtu s aktuálními daty
"""
from main import FinanceCalculator, DatabaseManager
from utils import DateHelper

def test_daily_budget():
    print("🔧 TEST DENNÍHO ROZPOČTU")
    print("=" * 40)
    
    # Získání aktuálních dat
    db = DatabaseManager()
    income, payday, balance = db.get_user_settings()
    expenses = db.get_expenses()
    
    print(f"📊 AKTUÁLNÍ NASTAVENÍ:")
    print(f"  Příjem: {income} Kč")
    print(f"  Balance: {balance} Kč")
    print(f"  Den výplaty: {payday}")
    print()
    
    # Výpočet s aktuálním dnem (6)
    result = FinanceCalculator.calculate_daily_budget(
        income, balance, expenses, payday, 6
    )
    
    print(f"📊 VÝSLEDKY VÝPOČTU:")
    print(f"  Zbývající výdaje: {result['remaining_expenses']} Kč")
    print(f"  Dostupné peníze: {result['available_money']} Kč")
    print(f"  Dny do výplaty: {result['days_until_payday']}")
    print(f"  Denní rozpočet: {result['daily_budget']} Kč")
    print()
    
    # Ruční výpočet pro kontrolu
    manual_available = balance - result['remaining_expenses']
    manual_daily = manual_available / result['days_until_payday'] if result['days_until_payday'] > 0 else 0
    manual_daily_capped = max(0, manual_daily)
    
    print(f"🧮 RUČNÍ KONTROLA:")
    print(f"  {balance} - {result['remaining_expenses']} = {manual_available} Kč")
    print(f"  {manual_available} / {result['days_until_payday']} = {manual_daily:.2f} Kč")
    print(f"  max(0, {manual_daily:.2f}) = {manual_daily_capped:.2f} Kč")
    
    if abs(result['daily_budget'] - manual_daily_capped) < 0.01:
        print("  ✅ VÝPOČET JE SPRÁVNÝ")
    else:
        print("  ❌ NESOULAD VE VÝPOČTU")
    
    db.close_connection()

if __name__ == "__main__":
    test_daily_budget()
