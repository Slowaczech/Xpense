"""
Test opravené logiky podle požadavků uživatele
"""
from main import FinanceCalculator
from datetime import datetime

def test_corrected_logic():
    """Test opravené logiky"""
    
    # Data podle uživatele
    current_balance = 12740
    payday = 15
    current_day = 6  # 6. srpna
    
    # Všechny výdaje (celkem 9740)
    expenses = [
        (1, "Nájem", 5000, 1),     
        (2, "Jídlo", 3000, 10),   
        (3, "Doprava", 1740, 20),  
    ]
    
    result = FinanceCalculator.calculate_daily_budget(
        income=0,
        balance=current_balance,
        expenses=expenses,
        payday=payday,
        current_day=current_day
    )
    
    print(f"=== TEST OPRAVENÉ LOGIKY ===")
    print(f"Vstupní data:")
    print(f"  Aktuální zůstatek: {current_balance} Kč")
    print(f"  Den výplaty: {payday}")
    print(f"  Aktuální den: {current_day}")
    print(f"  Celkové výdaje: {sum(amount for _, _, amount, day in expenses)} Kč")
    print()
    
    print(f"Výsledky:")
    print(f"  Zbývající výdaje: {result['remaining_expenses']} Kč")
    print(f"  Dnů do výplaty: {result['days_until_payday']}")
    print(f"  Denní rozpočet: {result['daily_budget']:.0f} Kč")
    print(f"  Dostupné peníze: {result['available_money']} Kč")
    print()
    
    # Kontrola požadavků
    print(f"Kontrola požadavků:")
    print(f"  Denní rozpočet = 333 Kč: {'✅' if abs(result['daily_budget'] - 333) < 1 else '❌'}")
    print(f"  Zbývající výdaje = 9740 Kč: {'✅' if result['remaining_expenses'] == 9740 else '❌'}")
    print(f"  Dnů do výplaty = 9: {'✅' if result['days_until_payday'] == 9 else '❌'}")
    
    # Matematická kontrola
    expected_budget = (current_balance - 9740) / result['days_until_payday']
    print(f"\nMatematická kontrola:")
    print(f"  ({current_balance} - 9740) / {result['days_until_payday']} = {expected_budget:.0f} Kč")
    print(f"  Odpovídá výpočtu: {'✅' if abs(expected_budget - result['daily_budget']) < 1 else '❌'}")

if __name__ == "__main__":
    test_corrected_logic()
