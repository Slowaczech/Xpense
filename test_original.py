"""
Test s původním příkladem uživatele
"""
from main import FinanceCalculator
from datetime import datetime

def test_original_example():
    """Test s původním příkladem"""
    
    # Původní data
    current_balance = 12740
    payday = 15
    current_day = 6
    
    # Původní výdaje (celkem 9740)
    expenses = [
        (1, "Nájem", 5000, 1),     # Už zaplaceno (1. < 6.)
        (2, "Jídlo", 3000, 10),    # Zbývá zaplatit (6. <= 10 <= 15)
        (3, "Doprava", 1740, 20),  # Příští měsíc (20 > 15)
    ]
    
    result = FinanceCalculator.calculate_daily_budget(
        income=0,
        balance=current_balance,
        expenses=expenses,
        payday=payday,
        current_day=current_day
    )
    
    print(f"=== PŮVODNÍ PŘÍKLAD ===")
    print(f"Vstup:")
    print(f"  Aktuální zůstatek: {current_balance}")
    print(f"  Den výplaty: {payday}")
    print(f"  Aktuální den: {current_day}")
    print()
    
    print(f"Rozpis výdajů:")
    remaining_manual = 0
    for _, name, amount, day in expenses:
        status = ""
        if current_day <= day <= payday:
            status = "ZBÝVÁ"
            remaining_manual += amount
        elif day < current_day:
            status = "ZAPLACENO"
        else:
            status = "PŘÍŠTÍ MĚSÍC (ZBÝVÁ)"
            remaining_manual += amount
        print(f"  {name}: {amount} Kč (den {day}) - {status}")
    
    print(f"\nVýsledky:")
    print(f"  Zbývající výdaje: {result['remaining_expenses']} Kč (očekáváno: {remaining_manual} Kč)")
    print(f"  Dnů do výplaty: {result['days_until_payday']}")
    print(f"  Denní rozpočet: {result['daily_budget']:.0f} Kč")
    print(f"  Dostupné peníze celkem: {result['available_money']} Kč")

if __name__ == "__main__":
    test_original_example()
