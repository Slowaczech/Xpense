"""
Test správné logiky - od aktuálního dne do příštího dne výplaty
"""
from utils import DateHelper
from main import FinanceCalculator, DatabaseManager
from datetime import datetime

def test_correct_logic():
    print("🔧 TEST SPRÁVNÉ LOGIKY VÝDAJŮ")
    print("=" * 60)
    print("Pravidlo: Počítáme od aktuálního dne včetně do příštího dne výplaty včetně")
    print("Den výplaty je 15. každého měsíce")
    print()
    
    # Získání dat z databáze
    db = DatabaseManager()
    income, payday, balance = db.get_user_settings()
    expenses = db.get_expenses()
    
    print(f"📅 TESTOVACÍ SCÉNÁŘE:")
    test_scenarios = [
        {"current_day": 6, "month": 8, "description": "6.8. → 15.8. (stejný měsíc)"},
        {"current_day": 16, "month": 9, "description": "16.9. → 15.10. (přes měsíc)"},
        {"current_day": 11, "month": 11, "description": "11.11. → 15.11. (stejný měsíc)"},
        {"current_day": 20, "month": 8, "description": "20.8. → 15.9. (přes měsíc)"},
    ]
    
    # Výdaje podle dnů pro lepší orientaci
    expenses_by_day = {}
    total_all = 0
    for _, name, amount, day in expenses:
        if day not in expenses_by_day:
            expenses_by_day[day] = []
        expenses_by_day[day].append((name, amount))
        total_all += amount
    
    print("💰 VÝDAJE PODLE DNŮ:")
    for day in sorted(expenses_by_day.keys()):
        day_total = sum(amount for _, amount in expenses_by_day[day])
        items = [f"{name} ({amount})" for name, amount in expenses_by_day[day]]
        print(f"  Den {day:2d}: {day_total:5.0f} Kč - {', '.join(items)}")
    print()
    
    for scenario in test_scenarios:
        current_day = scenario["current_day"]
        description = scenario["description"]
        
        print(f"🧮 SCÉNÁŘ: {description}")
        
        # Simulace výpočtu pro daný scénář
        remaining_expenses = 0
        included_days = []
        excluded_days = []
        
        for day in sorted(expenses_by_day.keys()):
            day_total = sum(amount for _, amount in expenses_by_day[day])
            expense_in_period = False
            reason = ""
            
            if current_day <= payday:  # payday = 15
                # Výplata je v tomto měsíci - počítáme výdaje od aktuálního dne do dne výplaty
                if day >= current_day and day <= payday:
                    expense_in_period = True
                    reason = f"stejný měsíc (den {day} v rozsahu {current_day}-{payday})"
                else:
                    reason = f"mimo rozsah {current_day}-{payday}"
            else:
                # Výplata je až příští měsíc
                if day >= current_day or day <= payday:
                    expense_in_period = True
                    if day >= current_day:
                        reason = f"aktuální měsíc (den {day} >= {current_day})"
                    else:
                        reason = f"příští měsíc (den {day} <= {payday})"
                else:
                    reason = f"mimo rozsah (den {day})"
            
            if expense_in_period:
                remaining_expenses += day_total
                included_days.append((day, day_total, reason))
            else:
                excluded_days.append((day, day_total, reason))
        
        print(f"   ✅ ZAPOČÍTANÉ DNY:")
        for day, amount, reason in included_days:
            print(f"      Den {day:2d}: {amount:5.0f} Kč - {reason}")
        
        if excluded_days:
            print(f"   ❌ NEZAPOČÍTANÉ DNY:")
            for day, amount, reason in excluded_days:
                print(f"      Den {day:2d}: {amount:5.0f} Kč - {reason}")
        
        print(f"   💰 ZBÝVAJÍCÍ VÝDAJE: {remaining_expenses} Kč")
        print()
    
    # Test s aktuálním dnem (6. srpna)
    print("🎯 TEST S AKTUÁLNÍM DNEM (6.8.):")
    result = FinanceCalculator.calculate_daily_budget(
        income, balance, expenses, payday, 6
    )
    
    print(f"   Zbývající výdaje: {result['remaining_expenses']} Kč")
    print(f"   Denní rozpočet: {result['daily_budget']:.0f} Kč")
    print(f"   Dny do výplaty: {result['days_until_payday']}")
    
    # Očekávaný výsledek pro 6.8. → 15.8.
    expected_expenses = 0
    for day in sorted(expenses_by_day.keys()):
        if 6 <= day <= 15:  # Od 6. do 15. srpna
            expected_expenses += sum(amount for _, amount in expenses_by_day[day])
    
    print(f"   Očekávané zbývající výdaje (6.-15.8.): {expected_expenses} Kč")
    
    if result['remaining_expenses'] == expected_expenses:
        print("   ✅ LOGIKA JE SPRÁVNĚ IMPLEMENTOVÁNA!")
    else:
        print("   ❌ NESOULAD V LOGICE!")
    
    db.close_connection()

if __name__ == "__main__":
    test_correct_logic()
