"""
Test nové logiky výpočtu zbývajících výdajů
Od aktuálního dne včetně do 15. dne příštího měsíce včetně
"""
from utils import DateHelper
from main import FinanceCalculator, DatabaseManager
from datetime import datetime

def test_new_expense_logic():
    print("🔧 TEST NOVÉ LOGIKY VÝDAJŮ")
    print("=" * 50)
    
    # Aktuální datum pro test
    today = datetime.now()
    current_day = today.day
    current_month = today.month
    
    print(f"📅 Aktuální datum: {current_day}.{current_month}")
    print(f"📊 Období výpočtu: od {current_day}. tohoto měsíce do 15. příštího měsíce")
    print()
    
    # Získání dat z databáze
    db = DatabaseManager()
    income, payday, balance = db.get_user_settings()
    expenses = db.get_expenses()
    
    print("💰 SEZNAM VÝDAJŮ:")
    total_all = 0
    for expense_id, name, amount, day in expenses:
        total_all += amount
        print(f"  {name}: {amount} Kč (den {day})")
    print(f"  CELKEM VŠECHNY: {total_all} Kč")
    print()
    
    # Test nové logiky
    print("🧮 ANALÝZA PODLE NOVÉ LOGIKY:")
    
    remaining_expenses = 0
    
    for _, name, amount, expense_day in expenses:
        expense_in_period = False
        reason = ""
        
        # Výdaj v aktuálním měsíci (od aktuálního dne včetně)
        if expense_day >= current_day:
            expense_in_period = True
            reason = f"aktuální měsíc (den {expense_day} >= {current_day})"
        
        # Výdaj v příštím měsíci (do 15. dne včetně)
        elif expense_day <= 15:
            expense_in_period = True
            reason = f"příští měsíc (den {expense_day} <= 15)"
        else:
            reason = f"MIMO období (den {expense_day})"
        
        status = "✅ ZAPOČÍTÁN" if expense_in_period else "❌ NEZAPOČÍTÁN"
        print(f"  {name}: {amount} Kč - {status} ({reason})")
        
        if expense_in_period:
            remaining_expenses += amount
    
    print()
    print(f"💡 ZBÝVAJÍCÍ VÝDAJE PODLE NOVÉ LOGIKY: {remaining_expenses} Kč")
    
    # Porovnání s výsledkem funkce
    result = FinanceCalculator.calculate_daily_budget(
        income, balance, expenses, payday, current_day
    )
    
    print(f"💡 VÝSLEDEK Z KALKULÁTORU: {result['remaining_expenses']} Kč")
    print()
    
    if remaining_expenses == result['remaining_expenses']:
        print("✅ LOGIKA JE SPRÁVNĚ IMPLEMENTOVÁNA!")
    else:
        print("❌ NESOULAD V LOGICE!")
    
    print()
    print("📊 KOMPLETNÍ VÝSLEDEK:")
    print(f"  Denní rozpočet: {DateHelper.format_currency(result['daily_budget'])}")
    print(f"  Zbývající výdaje: {DateHelper.format_currency(result['remaining_expenses'])}")
    print(f"  Dny do výplaty: {result['days_until_payday']}")
    
    db.close_connection()

if __name__ == "__main__":
    test_new_expense_logic()
