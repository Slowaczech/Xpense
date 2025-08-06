"""
Test výpočtu zbývajících výdajů do výplaty
"""
from main import FinanceCalculator
from datetime import datetime

def test_remaining_expenses():
    """Test výpočtu zbývajících výdajů"""
    
    # Vstupní data
    current_balance = 12740
    payday = 15
    current_day = 6  # 6. srpna
    
    # Simulace výdajů s různými dny splatnosti
    expenses = [
        (1, "Nájem", 5000, 1),     # Už zaplaceno (1. < 6.)
        (2, "Jídlo", 3000, 10),    # Zbývá zaplatit (6. <= 10 <= 15)
        (3, "Doprava", 1740, 5),   # Už zaplaceno (5. < 6.)
        (4, "Internet", 500, 12),  # Zbývá zaplatit (6. <= 12 <= 15)
        (5, "Telefon", 800, 20),   # Zbývá zaplatit (20 > 15, takže příští měsíc)
    ]
    
    # Výpočet
    result = FinanceCalculator.calculate_daily_budget(
        income=0,
        balance=current_balance,
        expenses=expenses,
        payday=payday,
        current_day=current_day
    )
    
    print(f"=== TEST ZBÝVAJÍCÍCH VÝDAJŮ ===")
    print(f"Aktuální den: {current_day}")
    print(f"Den výplaty: {payday}")
    print()
    print(f"Rozpis výdajů:")
    total_expenses = 0
    remaining_manual = 0
    
    for _, name, amount, day in expenses:
        total_expenses += amount
        status = ""
        
        if current_day < payday:
            if current_day <= day <= payday:
                status = "ZBÝVÁ"
                remaining_manual += amount
            elif day < current_day:
                status = "ZAPLACENO"
            else:  # day > payday
                status = "PŘÍŠTÍ MĚSÍC (ZBÝVÁ)"
                remaining_manual += amount
        else:
            status = "ZBÝVÁ (příští měsíc)"
            remaining_manual += amount
            
        print(f"  {name}: {amount} Kč (den {day}) - {status}")
    
    print(f"\nSoučty:")
    print(f"  Celkové měsíční výdaje: {total_expenses} Kč")
    print(f"  Zbývající výdaje (ruční výpočet): {remaining_manual} Kč")
    print(f"  Zbývající výdaje (aplikace): {result['remaining_expenses']} Kč")
    print(f"  Denní rozpočet: {result['daily_budget']:.0f} Kč")
    print(f"  Dnů do výplaty: {result['days_until_payday']}")
    
    print(f"\n✅ Test {'ÚSPĚŠNÝ' if remaining_manual == result['remaining_expenses'] else 'NEÚSPĚŠNÝ'}")

if __name__ == "__main__":
    test_remaining_expenses()
