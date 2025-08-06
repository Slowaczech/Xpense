"""
Přesný test podle požadavků uživatele
"""

def test_exact_scenario():
    """Test přesného scénáře"""
    
    # Zadané hodnoty
    current_balance = 12740
    payday = 15  
    total_expenses = 9740
    
    # Logika výpočtu podle požadovaného výstupu:
    # Dny do výplaty: 10
    # Denní rozpočet: 300
    # To znamená: (12740 - 9740) / 10 = 3000 / 10 = 300
    
    available_money = current_balance - total_expenses
    expected_days = 10
    expected_daily_budget = available_money / expected_days
    
    print("=== ANALÝZA POŽADOVANÉHO VÝPOČTU ===")
    print(f"Vstup:")
    print(f"  Aktuální zůstatek: {current_balance}")
    print(f"  Den výplaty: {payday}")
    print(f"  Výdaje: {total_expenses}")
    print()
    print(f"Výpočet:")
    print(f"  Dostupné peníze: {current_balance} - {total_expenses} = {available_money}")
    print(f"  Dny do výplaty: {expected_days}")
    print(f"  Denní rozpočet: {available_money} / {expected_days} = {expected_daily_budget}")
    print()
    print(f"Očekávaný výstup:")
    print(f"  Dnů do výplaty: {expected_days}")
    print(f"  Denní rozpočet: {int(expected_daily_budget)}")
    
    # Pro dosažení 10 dní do výplaty při 15. jako dni výplaty
    # znamená to, že aktuální den je 5. (15-5-1+1=10)
    # nebo je to 6. bez započítání aktuálního dne (15-6+1=10)
    print()
    print("=== ANALÝZA DNÍ ===")
    print("Pro dosažení 10 dní do výplaty při dni výplaty = 15:")
    print("Možnost 1: Aktuální den = 5, počítáme včetně aktuálního: 15-5+1 = 11 ❌")
    print("Možnost 2: Aktuální den = 6, nepočítáme aktuální: 15-6+1 = 10 ✅")
    print("Možnost 3: Aktuální den = 6, počítáme jen pracovní dny: custom logika")

if __name__ == "__main__":
    test_exact_scenario()
