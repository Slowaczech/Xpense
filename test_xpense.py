"""
Testy pro Xpense aplikaci
"""

import unittest
import os
import tempfile
from datetime import datetime
from main import DatabaseManager, FinanceCalculator


class TestDatabaseManager(unittest.TestCase):
    """Testy pro databázový manager"""
    
    def setUp(self):
        """Nastavení testu s dočasnou databází"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = DatabaseManager(self.temp_db.name)
    
    def tearDown(self):
        """Úklid po testu"""
        # Uzavření všech databázových spojení před smazáním
        self.db = None
        try:
            os.unlink(self.temp_db.name)
        except (PermissionError, FileNotFoundError):
            pass  # Soubor může být stále používán na Windows
    
    def test_save_and_get_user_settings(self):
        """Test uložení a načtení uživatelských nastavení"""
        self.db.save_user_settings(30000, 15, 5000)
        income, payday, balance = self.db.get_user_settings()
        
        self.assertEqual(income, 30000)
        self.assertEqual(payday, 15)
        self.assertEqual(balance, 5000)
    
    def test_add_and_get_expenses(self):
        """Test přidání a načtení výdajů"""
        expense_id = self.db.add_expense("Nájem", 12000, 5)
        self.assertIsNotNone(expense_id)
        
        expenses = self.db.get_expenses()
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0][1], "Nájem")
        self.assertEqual(expenses[0][2], 12000)
        self.assertEqual(expenses[0][3], 5)
    
    def test_delete_expense(self):
        """Test smazání výdaje"""
        expense_id = self.db.add_expense("Test", 1000, 10)
        self.db.delete_expense(expense_id)
        
        expenses = self.db.get_expenses()
        self.assertEqual(len(expenses), 0)


class TestFinanceCalculator(unittest.TestCase):
    """Testy pro finanční kalkulátor"""
    
    def test_calculate_daily_budget_basic(self):
        """Test základního výpočtu denního rozpočtu"""
        expenses = [(1, "Nájem", 12000, 5), (2, "Energie", 3000, 10)]
        
        result = FinanceCalculator.calculate_daily_budget(
            income=30000,
            balance=20000,
            expenses=expenses,
            payday=25,
            current_day=1
        )
        
        # Testujeme, že se výpočet provede bez chyby
        self.assertIsInstance(result['daily_budget'], (int, float))
        self.assertIsInstance(result['days_until_payday'], int)
        self.assertIsInstance(result['remaining_expenses'], (int, float))
        self.assertIsInstance(result['available_money'], (int, float))
    
    def test_calculate_daily_budget_no_negative(self):
        """Test, že denní rozpočet není záporný"""
        expenses = [(1, "Drahý nájem", 25000, 5)]
        
        result = FinanceCalculator.calculate_daily_budget(
            income=30000,
            balance=10000,
            expenses=expenses,
            payday=25,
            current_day=1
        )
        
        # Denní rozpočet by neměl být záporný
        self.assertGreaterEqual(result['daily_budget'], 0)


if __name__ == '__main__':
    unittest.main()
