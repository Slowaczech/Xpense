"""
Demonstrace nové logiky výdajů s různými scénáři
"""
from main import FinanceCalculator
from datetime import datetime

def demonstrate_new_logic():
    print("🧮 DEMONSTRACE NOVÉ LOGIKY VÝDAJŮ")
    print("=" * 60)
    print("Pravidlo: Započítávají se výdaje od aktuálního dne včetně")
    print("          do 15. dne příštího měsíce včetně")
    print()
    
    # Simulace různých dat
    test_scenarios = [
        {"current_day": 1, "description": "1. den v měsíci"},
        {"current_day": 6, "description": "6. den v měsíci (AKTUÁLNÍ)"},
        {"current_day": 10, "description": "10. den v měsíci"},
        {"current_day": 15, "description": "15. den v měsíci"},
        {"current_day": 20, "description": "20. den v měsíci"},
        {"current_day": 28, "description": "28. den v měsíci"},
    ]
    
    # Testovací výdaje
    test_expenses = [
        ("Výdaj 1", 1000, 1),    # 1. den
        ("Výdaj 2", 1500, 5),    # 5. den
        ("Výdaj 3", 2000, 10),   # 10. den
        ("Výdaj 4", 2500, 15),   # 15. den
        ("Výdaj 5", 3000, 20),   # 20. den
        ("Výdaj 6", 3500, 25),   # 25. den
    ]
    
    total_all_expenses = sum(expense[1] for expense in test_expenses)
    print(f"📊 TESTOVACÍ VÝDAJE (celkem {total_all_expenses} Kč):")
    for name, amount, day in test_expenses:
        print(f"  {name}: {amount} Kč (den {day})")
    print()
    
    print("🔍 ANALÝZA PRO RŮZNÉ AKTUÁLNÍ DNY:")
    print("=" * 60)
    
    for scenario in test_scenarios:
        current_day = scenario["current_day"]
        description = scenario["description"]
        
        print(f"📅 SCÉNÁŘ: {description}")
        print(f"   Období: od {current_day}. tohoto měsíce do 15. příštího měsíce")
        
        remaining_expenses = 0
        included_expenses = []
        excluded_expenses = []
        
        for name, amount, expense_day in test_expenses:
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
                reason = f"mimo období (den {expense_day})"
            
            if expense_in_period:
                remaining_expenses += amount
                included_expenses.append((name, amount, expense_day, reason))
            else:
                excluded_expenses.append((name, amount, expense_day, reason))
        
        print(f"   ✅ ZAPOČÍTANÉ VÝDAJE:")
        for name, amount, day, reason in included_expenses:
            print(f"      {name}: {amount} Kč - {reason}")
        
        if excluded_expenses:
            print(f"   ❌ NEZAPOČÍTANÉ VÝDAJE:")
            for name, amount, day, reason in excluded_expenses:
                print(f"      {name}: {amount} Kč - {reason}")
        
        print(f"   💰 ZBÝVAJÍCÍ VÝDAJE: {remaining_expenses} Kč")
        print()

if __name__ == "__main__":
    demonstrate_new_logic()
