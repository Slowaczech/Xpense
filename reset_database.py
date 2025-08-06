"""
Aktualizace databáze podle požadovaných dat
"""
from main import DatabaseManager

def reset_database_to_expected():
    print("🔧 AKTUALIZACE DATABÁZE PODLE POŽADAVKŮ")
    print("=" * 50)
    
    db = DatabaseManager()
    
    # Smazání všech existujících výdajů
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM regular_expenses")
    conn.commit()
    print("✅ Všechny výdaje smazány")
    
    # Přidání nových výdajů podle požadavků (celkem 9740 Kč)
    expenses_to_add = [
        ("Nájem", 5000, 1),
        ("Jídlo", 3000, 10),
        ("Doprava", 1740, 20)
    ]
    
    total_added = 0
    for name, amount, day in expenses_to_add:
        db.add_expense(name, amount, day)
        total_added += amount
        print(f"✅ Přidán výdaj: {name} - {amount} Kč (den {day})")
    
    print(f"\n📊 SOUHRN ZMĚN:")
    print(f"   Celkem přidáno: {total_added} Kč")
    print(f"   Očekávané zbývající výdaje: {total_added} Kč")
    
    # Ověření nastavení
    income, payday, balance = db.get_user_settings()
    print(f"\n📋 AKTUÁLNÍ NASTAVENÍ:")
    print(f"   Aktuální zůstatek: {balance} Kč")
    print(f"   Den výplaty: {payday}")
    
    # Výpočet očekávaného denního rozpočtu
    expected_budget = (balance - total_added) / 9  # 9 dní do výplaty
    print(f"   Očekávaný denní rozpočet: {expected_budget:.0f} Kč")
    
    db.close_connection()
    
    print(f"\n🎯 DATABÁZE AKTUALIZOVÁNA!")
    print("   Nyní restartujte aplikaci pro zobrazení správných hodnot.")

if __name__ == "__main__":
    reset_database_to_expected()
