"""
Pomocné funkce pro Xpense aplikaci
"""

from datetime import datetime, timedelta
import re


class InputValidator:
    """Validátor vstupních dat"""
    
    @staticmethod
    def validate_income(income_str):
        """Validace příjmu"""
        if not income_str or not income_str.strip():
            return False, "Příjem nesmí být prázdný"
        
        try:
            income = float(income_str.replace(',', '.'))
            if income <= 0:
                return False, "Příjem musí být větší než 0"
            if income > 9999999:
                return False, "Příjem je příliš velký"
            return True, income
        except ValueError:
            return False, "Neplatná hodnota příjmu"
    
    @staticmethod
    def validate_payday(payday_str):
        """Validace dne výplaty"""
        if not payday_str or not payday_str.strip():
            return False, "Den výplaty nesmí být prázdný"
        
        try:
            payday = int(payday_str)
            if payday < 1 or payday > 31:
                return False, "Den výplaty musí být mezi 1-31"
            
            # Dodatečná kontrola pro aktuální měsíc
            today = datetime.now()
            if not DateHelper.is_valid_day_for_month(payday, today.month, today.year):
                return False, f"Den {payday} není platný pro {DateHelper.get_czech_month_name(today.month)}"
            
            return True, payday
        except ValueError:
            return False, "Neplatný den výplaty"
    
    @staticmethod
    def validate_balance(balance_str):
        """Validace zůstatku"""
        if not balance_str or not balance_str.strip():
            return False, "Zůstatek nesmí být prázdný"
        
        try:
            balance = float(balance_str.replace(',', '.'))
            if balance < 0:
                return False, "Zůstatek nemůže být záporný"
            if balance > 99999999:
                return False, "Zůstatek je příliš velký"
            return True, balance
        except ValueError:
            return False, "Neplatná hodnota zůstatku"
    
    @staticmethod
    def validate_expense_name(name):
        """Validace názvu výdaje"""
        if not name or not name.strip():
            return False, "Název výdaje nesmí být prázdný"
        
        name = name.strip()
        if len(name) < 2:
            return False, "Název musí mít alespoň 2 znaky"
        if len(name) > 50:
            return False, "Název je příliš dlouhý (max 50 znaků)"
        
        # Kontrola zakázaných znaků
        forbidden_chars = ['<', '>', '/', '\\', '|', ':', '*', '?', '"']
        if any(char in name for char in forbidden_chars):
            return False, "Název obsahuje zakázané znaky"
        
        return True, name
    
    @staticmethod
    def validate_expense_amount(amount_str):
        """Validace částky výdaje"""
        if not amount_str or not amount_str.strip():
            return False, "Částka nesmí být prázdná"
        
        try:
            amount = float(amount_str.replace(',', '.'))
            if amount <= 0:
                return False, "Částka musí být větší než 0"
            if amount > 999999:
                return False, "Částka je příliš velká"
            return True, amount
        except ValueError:
            return False, "Neplatná částka"
    
    @staticmethod
    def validate_expense_day(day_str):
        """Validace dne výdaje"""
        if not day_str or not day_str.strip():
            return False, "Den nesmí být prázdný"
        
        try:
            day = int(day_str)
            if day < 1 or day > 31:
                return False, "Den musí být mezi 1-31"
            return True, day
        except ValueError:
            return False, "Neplatný den"


class DateHelper:
    """Pomocník pro práci s daty"""
    
    @staticmethod
    def get_days_in_month(year, month):
        """Získání počtu dnů v měsíci"""
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        
        last_day = next_month - timedelta(days=1)
        return last_day.day
    
    @staticmethod
    def is_valid_day_for_month(day, month, year):
        """Kontrola, zda je den platný pro daný měsíc"""
        max_days = DateHelper.get_days_in_month(year, month)
        return 1 <= day <= max_days
    
    @staticmethod
    def format_currency(amount):
        """Formátování částky jako měna - zobrazuje přesné hodnoty"""
        return f"{amount:.0f} Kč"
    
    @staticmethod
    def format_date(date):
        """Formátování data"""
        return date.strftime("%d.%m.%Y")
    
    @staticmethod
    def get_czech_month_name(month):
        """Získání českého názvu měsíce"""
        months = [
            "Leden", "Únor", "Březen", "Duben", "Květen", "Červen",
            "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"
        ]
        return months[month - 1] if 1 <= month <= 12 else "Neznámý"


class ErrorHandler:
    """Správce chyb aplikace"""
    
    @staticmethod
    def handle_database_error(error, operation="databázová operace"):
        """Zpracování databázových chyb"""
        error_msg = str(error)
        if "locked" in error_msg.lower():
            return f"Databáze je zablokována. Zkuste to znovu."
        elif "permission" in error_msg.lower():
            return f"Nedostatečná oprávnění pro {operation}."
        elif "disk" in error_msg.lower():
            return f"Nedostatek místa na disku."
        else:
            return f"Chyba při {operation}: {error_msg[:50]}..."
    
    @staticmethod
    def handle_calculation_error(error):
        """Zpracování chyb výpočtu"""
        return f"Chyba výpočtu: Zkontrolujte zadané hodnoty."
    
    @staticmethod
    def format_error_message(title, message):
        """Formátování chybové zprávy"""
        return f"{title}\n\n{message}"
