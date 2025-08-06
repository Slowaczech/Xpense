"""
Podrobná analýza nové logiky s daty z tabulky
"""
from utils import DateHelper
from main import FinanceCalculator, DatabaseManager
from datetime import datetime

def detailed_analysis():
    print("🔍 PODROBNÁ ANALÝZA S DATY Z TABULKY")
    print("=" * 60)
    
    # Získání dat
    db = DatabaseManager()
    income, payday, balance = db.get_user_settings()
    expenses = db.get_expenses()
    
    print(f"💰 NASTAVENÍ:")
    print(f"  Příjem: {income} Kč")
    print(f"  Balance: {balance} Kč")
    print(f"  Den výplaty: {payday}.")
    print()
    
    # Test pro různé aktuální dny
    test_days = [1, 6, 15, 16, 17, 20, 26, 28]
    
    print("📊 VÝDAJE PODLE DNŮ:")
    expenses_by_day = {}
    total_all = 0
    for _, name, amount, day in expenses:
        if day not in expenses_by_day:
            expenses_by_day[day] = []
        expenses_by_day[day].append((name, amount))
        total_all += amount
    
    for day in sorted(expenses_by_day.keys()):
        day_total = sum(amount for _, amount in expenses_by_day[day])
        print(f"  Den {day:2d}: {day_total:5.0f} Kč - {', '.join(name for name, _ in expenses_by_day[day])}")
    print(f"  CELKEM: {total_all} Kč")
    print()
    
    print("🧮 ANALÝZA PRO RŮZNÉ AKTUÁLNÍ DNY:")
    print("=" * 60)
    
    for current_day in test_days:
        print(f"📅 AKTUÁLNÍ DEN: {current_day}")
        print(f"   Období: od {current_day}. tohoto měsíce do 15. příštího měsíce")
        
        # Výpočet zbývajících výdajů
        remaining_expenses = 0
        included_days = []
        excluded_days = []
        
        for day in sorted(expenses_by_day.keys()):
            day_total = sum(amount for _, amount in expenses_by_day[day])
            expense_in_period = False
            reason = ""
            
            # Výdaj v aktuálním měsíci (od aktuálního dne včetně)
            if day >= current_day:
                expense_in_period = True
                reason = f"aktuální měsíc (den {day} >= {current_day})"
            
            # Výdaj v příštím měsíci (do 15. dne včetně)
            elif day <= 15:
                expense_in_period = True
                reason = f"příští měsíc (den {day} <= 15)"
            else:
                reason = f"mimo období (den {day})"
            
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
        
        # Výpočet denního rozpočtu
        available_money = balance - total_all  # Pro denní rozpočet používáme všechny výdaje
        
        # Výpočet dnů do výplaty
        if current_day <= payday:
            days_until_payday = payday - current_day + 1
        else:
            days_until_payday = (31 - current_day) + payday + 1  # Aproximace
        
        daily_budget = available_money / days_until_payday if days_until_payday > 0 else 0
        
        print(f"   💡 ZBÝVAJÍCÍ VÝDAJE: {remaining_expenses} Kč")
        print(f"   💡 DENNÍ ROZPOČET: {max(0, daily_budget):.0f} Kč ({available_money} / {days_until_payday})")
        print()
    
    db.close_connection()

if __name__ == "__main__":
    detailed_analysis()
