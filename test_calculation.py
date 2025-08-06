"""
Test výpočtu podle požadavků uživatele
"""
from main import FinanceCalculator
from datetime import datetime

def test_calculation_with_custom_date():
    """Test s vlastním datem pro ověření očekávaného výsledku"""
    
    # Vstupní data podle příkladu
    current_balance = 12740
    payday = 15
    total_expenses = 9740
    
    # Simulace výdajů (celkem 9740)
    expenses = [
        (1, "Nájem", 5000, 1),
        (2, "Jídlo", 3000, 5),
        (3, "Doprava", 1740, 10)
    ]
    
    # Testovací kalkulátor s možností nastavit datum
    class TestCalculator(FinanceCalculator):
        @staticmethod
        def calculate_daily_budget_with_date(income, balance, expenses, payday, test_date):
            """Testovací verze s možností nastavit datum"""
            current_day = test_date.day
            current_month = test_date.month
            current_year = test_date.year
            
            # Určení příštího dne výplaty
            if current_day < payday:
                next_payday = datetime(current_year, current_month, payday)
            else:
                if current_month == 12:
                    next_payday = datetime(current_year + 1, 1, payday)
                else:
                    next_payday = datetime(current_year, current_month + 1, payday)
            
            # Výpočet dnů do výplaty (včetně dnešního dne)
            days_until_payday = (next_payday - test_date).days + 1
            
            # Celkové výdaje za měsíc
            total_monthly_expenses = sum(amount for _, _, amount, day in expenses)
            
            # Výpočet denního rozpočtu
            available_money = balance - total_monthly_expenses
            daily_budget = available_money / days_until_payday if days_until_payday > 0 else 0
            
            return {
                'daily_budget': max(0, daily_budget),
                'days_until_payday': days_until_payday,
                'remaining_expenses': total_monthly_expenses,
                'available_money': available_money
            }
    
    # Test s různými daty, abychom našli správné
    test_dates = [
        datetime(2025, 8, 5),  # 5. srpna - 10 dní do 15.
        datetime(2025, 8, 4),  # 4. srpna - 11 dní do 15.
        datetime(2025, 8, 6),  # 6. srpna - 9 dní do 15.
    ]
    
    print(f"=== TEST RŮZNÝCH DAT ===")
    for test_date in test_dates:
        result = TestCalculator.calculate_daily_budget_with_date(
            income=0,
            balance=current_balance,
            expenses=expenses,
            payday=payday,
            test_date=test_date
        )
        
        print(f"Datum: {test_date.strftime('%d.%m.%Y')}")
        print(f"  Dnů do výplaty: {result['days_until_payday']}")
        print(f"  Denní rozpočet: {result['daily_budget']:.0f}")
        
        if result['days_until_payday'] == 10 and abs(result['daily_budget'] - 300) < 1:
            print(f"  ✅ ODPOVÍDÁ OČEKÁVÁNÍ!")
        print()

def test_calculation_example():
    """Test podle příkladu uživatele"""
    
    # Vstupní data
    current_balance = 12740
    payday = 15
    total_expenses = 9740
    current_day = datetime.now().day
    
    # Simulace výdajů (celkem 9740)
    expenses = [
        (1, "Nájem", 5000, 1),
        (2, "Jídlo", 3000, 5),
        (3, "Doprava", 1740, 10)
    ]
    
    # Výpočet
    result = FinanceCalculator.calculate_daily_budget(
        income=0,  # není potřeba pro tento výpočet
        balance=current_balance,
        expenses=expenses,
        payday=payday,
        current_day=current_day
    )
    
    print(f"=== AKTUÁLNÍ TEST ===")
    print(f"Vstup:")
    print(f"  Aktuální zůstatek: {current_balance}")
    print(f"  Den výplaty: {payday}")
    print(f"  Výdaje celkem: {sum(amount for _, _, amount, day in expenses)}")
    print(f"  Aktuální den: {current_day}")
    print()
    print(f"Výstup:")
    print(f"  Dnů do výplaty: {result['days_until_payday']}")
    print(f"  Denní rozpočet: {result['daily_budget']:.0f}")
    print(f"  Dostupné peníze: {result['available_money']}")

if __name__ == "__main__":
    test_calculation_with_custom_date()
    print("="*50)
    test_calculation_example()
