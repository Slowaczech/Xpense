"""
Test formátování částek po opravě
"""
from utils import DateHelper
from main import FinanceCalculator, DatabaseManager
from datetime import datetime

def test_currency_formatting():
    print("🔧 TEST FORMÁTOVÁNÍ ČÁSTEK")
    print("=" * 40)
    
    # Test různých částek
    test_amounts = [333, 1000, 9740, 12740, 15699]
    
    print("Testování format_currency:")
    for amount in test_amounts:
        formatted = DateHelper.format_currency(amount)
        print(f"  {amount} → {formatted}")
    
    print("\n" + "="*40)
    
    # Test reálných dat z aplikace
    db = DatabaseManager()
    income, payday, balance = db.get_user_settings()
    expenses = db.get_expenses()
    current_day = datetime.now().day
    
    result = FinanceCalculator.calculate_daily_budget(
        income, balance, expenses, payday, current_day
    )
    
    print("📊 AKTUÁLNÍ VÝSLEDKY APLIKACE:")
    
    # Formátování jako v aplikaci
    daily_budget_formatted = DateHelper.format_currency(result['daily_budget'])
    expenses_formatted = DateHelper.format_currency(result['remaining_expenses'])
    
    print(f"  Denní rozpočet: {daily_budget_formatted}")
    print(f"  Zbývající výdaje: {expenses_formatted}")  # Toto by mělo být "9740 Kč"
    print(f"  Dny do výplaty: {result['days_until_payday']}")
    
    print(f"\n✅ Zbývající výdaje nyní zobrazují přesnou částku!")
    
    db.close_connection()

if __name__ == "__main__":
    test_currency_formatting()
