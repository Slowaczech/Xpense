"""
Test podle nových požadavků uživatele - výdaje od aktuálního dne do výplaty
"""
from main import FinanceCalculator
from datetime import datetime

def test_user_requirements():
    """Test podle požadavků uživatele - zbývající výdaje 9740 Kč"""
    
    # Data podle uživatele
    current_balance = 12740
    payday = 15
    current_day = 6
    
    # Všechny výdaje (podle screenshotu uživatele - celkem 9740)
    # Předpokládám strukturu výdajů, které by daly součet 9740
    expenses = [
        (1, "Nájem", 5000, 6),     # Aktuální den - ZBÝVÁ
        (2, "Jídlo", 3000, 10),    # Do výplaty - ZBÝVÁ  
        (3, "Doprava", 1740, 15),  # Den výplaty - ZBÝVÁ
    ]
    
    result = FinanceCalculator.calculate_daily_budget(
        income=0,
        balance=current_balance,
        expenses=expenses,
        payday=payday,
        current_day=current_day
    )
    
    print(f"=== TEST PODLE UŽIVATELOVÝCH POŽADAVKŮ ===")
    print(f"Aktuální den: {current_day}")
    print(f"Den výplaty: {payday}")
    print(f"Rozmezí pro zbývající výdaje: {current_day}. - {payday}. (včetně)")
    print()
    
    print(f"Rozpis výdajů:")
    expected_remaining = 0
    for _, name, amount, day in expenses:
        status = ""
        if current_day <= day <= payday:
            status = "ZBÝVÁ ✅"
            expected_remaining += amount
        else:
            status = "NEZAPOČÍTÁVÁ SE ❌"
        print(f"  {name}: {amount} Kč (den {day}) - {status}")
    
    print(f"\nVýsledky:")
    print(f"  Očekávané zbývající výdaje: {expected_remaining} Kč")
    print(f"  Vypočítané zbývající výdaje: {result['remaining_expenses']} Kč")
    print(f"  Denní rozpočet: {result['daily_budget']:.0f} Kč")
    print(f"  Dnů do výplaty: {result['days_until_payday']}")
    
    success = expected_remaining == result['remaining_expenses'] == 9740
    print(f"\n{'✅ ÚSPĚCH' if success else '❌ CHYBA'}: Zbývající výdaje = 9740 Kč")
    
    if not success:
        print(f"\n🔧 Pro dosažení 9740 Kč zbývajících výdajů potřebujeme:")
        print(f"   Všechny výdaje v rozmezí {current_day}.-{payday}. = 9740 Kč celkem")

def test_with_different_expense_days():
    """Test s různými dny výdajů pro pochopení logiky"""
    
    current_balance = 12740
    payday = 15
    current_day = 6
    
    # Různé scénáře výdajů
    scenarios = [
        {
            "name": "Všechny výdaje v rozmezí 6.-15.",
            "expenses": [
                (1, "Výdaj A", 3000, 6),   # Den 6 - ZBÝVÁ
                (2, "Výdaj B", 3000, 10),  # Den 10 - ZBÝVÁ
                (3, "Výdaj C", 3740, 15),  # Den 15 - ZBÝVÁ
            ]
        },
        {
            "name": "Výdaje mimo rozmezí",
            "expenses": [
                (1, "Výdaj A", 2000, 5),   # Den 5 - NEZAPOČÍTÁVÁ
                (2, "Výdaj B", 5000, 8),   # Den 8 - ZBÝVÁ
                (3, "Výdaj C", 2740, 20),  # Den 20 - NEZAPOČÍTÁVÁ
            ]
        }
    ]
    
    print(f"\n=== TESTOVÁNÍ RŮZNÝCH SCÉNÁŘŮ ===")
    for scenario in scenarios:
        print(f"\n{scenario['name']}:")
        
        result = FinanceCalculator.calculate_daily_budget(
            income=0,
            balance=current_balance,
            expenses=scenario['expenses'],
            payday=payday,
            current_day=current_day
        )
        
        expected = sum(amount for _, _, amount, day in scenario['expenses'] 
                      if current_day <= day <= payday)
        
        for _, name, amount, day in scenario['expenses']:
            status = "ZBÝVÁ" if current_day <= day <= payday else "MIMO ROZMEZÍ"
            print(f"  {name}: {amount} Kč (den {day}) - {status}")
        
        print(f"  → Zbývající výdaje: {result['remaining_expenses']} Kč (očekáváno: {expected} Kč)")

if __name__ == "__main__":
    test_user_requirements()
    test_with_different_expense_days()
