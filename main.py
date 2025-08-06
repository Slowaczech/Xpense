"""
Xpense - Aplikace pro správu financí
Optimalizovaná Android aplikace v Pythonu s Kivy
"""

__version__ = "1.0"

# Konstanty aplikace
MAX_EXPENSES = 20
LOW_BUDGET_THRESHOLD = 100
MEDIUM_BUDGET_THRESHOLD = 300
SNACKBAR_DURATION = 3

from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivy.lang import Builder
from kivy.metrics import dp
from datetime import datetime, timedelta
import sqlite3
import os
from utils import InputValidator, DateHelper, ErrorHandler
from typing import Optional


class DatabaseManager:
    """Optimalizovaný databázový manager pro SQLite"""
    
    def __init__(self, db_name="xpense.db"):
        self.db_path = db_name
        self._connection = None
        self.init_database()
    
    def get_connection(self):
        """Získání připojení k databázi"""
        if self._connection is None:
            self._connection = sqlite3.connect(self.db_path)
        return self._connection
    
    def close_connection(self):
        """Uzavření připojení k databázi"""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def init_database(self):
        """Inicializace databáze s optimalizovanými indexy"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabulka pro nastavení uživatele
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_settings (
                id INTEGER PRIMARY KEY,
                monthly_income REAL NOT NULL,
                payday INTEGER NOT NULL,
                current_balance REAL NOT NULL,
                last_updated TEXT NOT NULL
            )
        """)
        
        # Tabulka pro pravidelné výdaje
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS regular_expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                amount REAL NOT NULL,
                day_of_month INTEGER NOT NULL,
                is_active INTEGER DEFAULT 1,
                created_at TEXT NOT NULL
            )
        """)
        
        # Optimalizační indexy
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_expenses_day ON regular_expenses(day_of_month)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_expenses_active ON regular_expenses(is_active)")
        
        conn.commit()
    
    def save_user_settings(self, income, payday, balance):
        """Uložení uživatelských nastavení"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_settings")  # Vždy jen jeden řádek
        cursor.execute("""
            INSERT INTO user_settings (monthly_income, payday, current_balance, last_updated)
            VALUES (?, ?, ?, ?)
        """, (income, payday, balance, datetime.now().isoformat()))
        conn.commit()
    
    def get_user_settings(self):
        """Získání uživatelských nastavení"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT monthly_income, payday, current_balance FROM user_settings LIMIT 1")
            result = cursor.fetchone()
            return result if result else (0, 1, 0)
    
    def add_expense(self, name, amount, day):
        """Přidání pravidelného výdaje"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO regular_expenses (name, amount, day_of_month, created_at)
                VALUES (?, ?, ?, ?)
            """, (name, amount, day, datetime.now().isoformat()))
            conn.commit()
            return cursor.lastrowid
    
    def get_expenses(self):
        """Získání všech aktivních výdajů"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, amount, day_of_month 
                FROM regular_expenses 
                WHERE is_active = 1 
                ORDER BY day_of_month
            """)
            return cursor.fetchall()
    
    def delete_expense(self, expense_id):
        """Smazání výdaje"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE regular_expenses SET is_active = 0 WHERE id = ?", (expense_id,))
            conn.commit()


class FinanceCalculator:
    """Optimalizovaný kalkulátor financí"""
    
    @staticmethod
    def calculate_daily_budget(income, balance, expenses, payday, current_day):
        """Výpočet denního rozpočtu do výplaty"""
        # Získání dnů do výplaty
        today = datetime.now()
        current_month = today.month
        current_year = today.year
        current_day = today.day
        
        # Určení příštího dne výplaty
        if current_day <= payday:
            # Výplata je ještě v tomto měsíci
            next_payday = datetime(current_year, current_month, payday)
        else:
            # Výplata je až příští měsíc
            if current_month == 12:
                next_payday = datetime(current_year + 1, 1, payday)
            else:
                next_payday = datetime(current_year, current_month + 1, payday)
        
        # Výpočet dnů do výplaty (včetně dne výplaty)
        days_until_payday = (next_payday - today).days + 1
        
        # Výpočet zbývajících výdajů do výplaty
        remaining_expenses = 0
        total_monthly_expenses = 0
        
        # Určení příštího dne výplaty
        if current_day <= payday:
            # Výplata je ještě v tomto měsíci
            next_payday_month = current_month
            next_payday_year = current_year
        else:
            # Výplata je až příští měsíc
            if current_month == 12:
                next_payday_month = 1
                next_payday_year = current_year + 1
            else:
                next_payday_month = current_month + 1
                next_payday_year = current_year
        
        for _, _, amount, expense_day in expenses:
            total_monthly_expenses += amount
            
            # Kontrola, zda výdaj spadá do období od aktuálního dne do příštího dne výplaty
            expense_in_period = False
            
            if current_day <= payday:
                # Výplata je v tomto měsíci - počítáme výdaje od aktuálního dne do dne výplaty
                if expense_day >= current_day and expense_day <= payday:
                    expense_in_period = True
            else:
                # Výplata je až příští měsíc
                if expense_day >= current_day or expense_day <= payday:
                    expense_in_period = True
            
            if expense_in_period:
                remaining_expenses += amount
        
        # Výpočet denního rozpočtu
        # Pro denní rozpočet počítáme: balance minus zbývající výdaje, děleno dny do výplaty
        available_money = balance - remaining_expenses
        daily_budget = available_money / days_until_payday if days_until_payday > 0 else 0
        
        return {
            'daily_budget': max(0, daily_budget),
            'days_until_payday': days_until_payday,
            'remaining_expenses': remaining_expenses,  # Pouze zbývající výdaje do výplaty
            'available_money': available_money
        }


class MainScreen(Screen):
    """Hlavní obrazovka s přehledem financí"""
    pass


class SettingsScreen(Screen):
    """Obrazovka nastavení"""
    pass


class SimpleSettingsScreen(Screen):
    """Jednoduchá obrazovka nastavení s TextInput"""
    pass


class ExpensesScreen(Screen):
    """Obrazovka pro správu výdajů"""
    pass


class XpenseApp(MDApp):
    """Hlavní aplikace Xpense"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DatabaseManager()
        self.calculator = FinanceCalculator()
        self.dialog: Optional[MDDialog] = None
        
    def build(self):
        """Sestavení aplikace"""
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.accent_palette = "LightGreen"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.accent_hue = "400"
        
        # Načtení jednoduchého KV souboru
        Builder.load_file('xpense_simple.kv')
        
        # Screen Manager
        self.sm = ScreenManager()
        
        # Vytvoření obrazovek
        self.main_screen = MainScreen()
        self.settings_screen = SimpleSettingsScreen()
        self.expenses_screen = ExpensesScreen()
        
        self.sm.add_widget(self.main_screen)
        self.sm.add_widget(self.settings_screen)
        self.sm.add_widget(self.expenses_screen)
        
        return self.sm
    
    def switch_screen(self, screen_name):
        """Přepnutí na jinou obrazovku"""
        self.sm.current = screen_name
        
        if screen_name == 'main':
            self.update_main_screen()
        elif screen_name == 'settings':
            self.load_settings()
        elif screen_name == 'expenses':
            self.load_expenses()
    
    def update_main_screen(self, *args):
        """Aktualizace hlavní obrazovky"""
        try:
            income, payday, balance = self.db.get_user_settings()
            expenses = self.db.get_expenses()
            current_day = datetime.now().day
            
            # Získání referencí na labely z KV souboru
            main_screen = self.sm.get_screen('main')
            daily_budget_label = main_screen.ids.daily_budget_label
            days_label = main_screen.ids.days_label
            expenses_label = main_screen.ids.expenses_label
            
            if income > 0:
                calc_result = self.calculator.calculate_daily_budget(
                    income, balance, expenses, payday, current_day
                )
                
                # Formátované zobrazení
                daily_budget_formatted = DateHelper.format_currency(calc_result['daily_budget'])
                expenses_formatted = DateHelper.format_currency(calc_result['remaining_expenses'])
                
                daily_budget_label.text = f"Denní rozpočet: {daily_budget_formatted}"
                days_label.text = f"Dnů do výplaty: {calc_result['days_until_payday']}"
                expenses_label.text = f"Zbývající výdaje: {expenses_formatted}"
                
                # Barevné indikace podle situace
                if calc_result['daily_budget'] < LOW_BUDGET_THRESHOLD:
                    daily_budget_label.theme_text_color = "Error"
                elif calc_result['daily_budget'] < MEDIUM_BUDGET_THRESHOLD:
                    daily_budget_label.theme_text_color = "Primary"  # Orange by mělo být, ale není v KivyMD
                else:
                    daily_budget_label.theme_text_color = "Primary"
            else:
                daily_budget_label.text = "⚙️ Nastavte prosím své finance"
                days_label.text = "Přejděte do nastavení"
                expenses_label.text = "Aplikace potřebuje vaše údaje"
                
        except Exception as e:
            error_msg = ErrorHandler.handle_calculation_error(e)
            self.show_snackbar(error_msg)
    
    def load_settings(self):
        """Načtení nastavení do formuláře"""
        income, payday, balance = self.db.get_user_settings()
        settings_screen = self.sm.get_screen('settings')
        settings_screen.ids.income_field.text = str(income) if income > 0 else ""
        settings_screen.ids.payday_field.text = str(payday)
        settings_screen.ids.balance_field.text = str(balance) if balance > 0 else ""
    
    def save_settings(self, *args):
        """Uložení nastavení"""
        try:
            settings_screen = self.sm.get_screen('settings')
            income_text = settings_screen.ids.income_field.text
            payday_text = settings_screen.ids.payday_field.text
            balance_text = settings_screen.ids.balance_field.text
            
            # Validace příjmu
            is_valid, result = InputValidator.validate_income(income_text)
            if not is_valid:
                self.show_snackbar(f"❌ {result}")
                return
            income = result
            
            # Validace dne výplaty
            is_valid, result = InputValidator.validate_payday(payday_text)
            if not is_valid:
                self.show_snackbar(f"❌ {result}")
                return
            payday = result
            
            # Validace zůstatku
            is_valid, result = InputValidator.validate_balance(balance_text)
            if not is_valid:
                self.show_snackbar(f"❌ {result}")
                return
            balance = result
            
            # Kontrola validity dne pro aktuální měsíc
            today = datetime.now()
            if not DateHelper.is_valid_day_for_month(payday, today.month, today.year):
                self.show_snackbar(f"❌ Den {payday} není platný pro {DateHelper.get_czech_month_name(today.month)}")
                return
            
            self.db.save_user_settings(income, payday, balance)
            self.show_snackbar("✅ Nastavení úspěšně uloženo!")
            
        except Exception as e:
            error_msg = ErrorHandler.handle_database_error(e, "ukládání nastavení")
            self.show_snackbar(f"❌ {error_msg}")
    
    def load_expenses(self):
        """Načtení seznamu výdajů"""
        expenses_screen = self.sm.get_screen('expenses')
        expenses_list = expenses_screen.ids.expenses_list
        expenses_list.clear_widgets()
        expenses = self.db.get_expenses()
        
        if not expenses:
            # Zobrazení prázdného stavu
            from kivymd.uix.card import MDCard
            from kivymd.uix.label import MDLabel
            
            empty_card = MDCard(
                size_hint=(1, None),
                height=dp(140),
                elevation=1,
                padding=dp(20),
                md_bg_color=(0.95, 0.95, 0.95, 1),
                radius=[10, 10, 10, 10]
            )
            
            empty_label = MDLabel(
                text="📝 Žádné výdaje\n\nPřidejte své první pravidelné výdaje\npomocí tlačítka + v horní liště",
                halign="center",
                theme_text_color="Secondary",
                font_style="Body1"
            )
            
            empty_card.add_widget(empty_label)
            expenses_list.add_widget(empty_card)
        else:
            for expense_id, name, amount, day in expenses:
                item = TwoLineListItem(
                    text=f"💰 {name}",
                    secondary_text=f"💳 {amount:.0f} Kč • 📅 {day}. den v měsíci",
                    on_release=lambda x, exp_id=expense_id: self.show_delete_expense_dialog(exp_id),
                    theme_text_color="Primary"
                )
                expenses_list.add_widget(item)
    
    def show_add_expense_dialog(self):
        """Dialog pro přidání výdaje"""
        if self.dialog:
            self.dialog.dismiss()  # type: ignore
            self.dialog = None  # Uvolnění paměti
        
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            size_hint_y=None,
            height=dp(280),
            adaptive_height=True
        )
        
        # Název výdaje s labelem
        name_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint_y=None,
            height=dp(70)
        )
        name_label = MDLabel(
            text="💰 Název výdaje",
            theme_text_color="Primary",
            font_style="Subtitle2",
            size_hint_y=None,
            height=dp(25)
        )
        name_field = MDTextField(
            hint_text="Zadejte název",
            size_hint_y=None,
            height=dp(45),
            multiline=False
        )
        name_layout.add_widget(name_label)
        name_layout.add_widget(name_field)
        
        # Částka s labelem
        amount_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint_y=None,
            height=dp(70)
        )
        amount_label = MDLabel(
            text="💳 Částka (Kč)",
            theme_text_color="Primary", 
            font_style="Subtitle2",
            size_hint_y=None,
            height=dp(25)
        )
        amount_field = MDTextField(
            hint_text="Zadejte částku", 
            input_filter="float",
            size_hint_y=None,
            height=dp(45),
            multiline=False
        )
        amount_layout.add_widget(amount_label)
        amount_layout.add_widget(amount_field)
        
        # Den v měsíci s labelem
        day_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint_y=None,
            height=dp(70)
        )
        day_label = MDLabel(
            text="📅 Den v měsíci (1-31)",
            theme_text_color="Primary",
            font_style="Subtitle2", 
            size_hint_y=None,
            height=dp(25)
        )
        day_field = MDTextField(
            hint_text="Zadejte den", 
            input_filter="int",
            size_hint_y=None,
            height=dp(45),
            multiline=False
        )
        day_layout.add_widget(day_label)
        day_layout.add_widget(day_field)
        
        content.add_widget(name_layout)
        content.add_widget(amount_layout)
        content.add_widget(day_layout)
        
        self.dialog = MDDialog(
            title="Nový pravidelný výdaj",
            type="custom",
            content_cls=content,
            size_hint=(0.9, None),
            height=dp(480),
            buttons=[
                MDRaisedButton(
                    text="ZRUŠIT",
                    theme_text_color="Primary",
                    on_release=lambda x: self.dialog.dismiss() if self.dialog else None  # type: ignore
                ),
                MDRaisedButton(
                    text="PŘIDAT",
                    md_bg_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.add_expense(
                        name_field.text, amount_field.text, day_field.text
                    )
                )
            ]
        )
        self.dialog.open()
    
    def add_expense(self, name, amount, day):
        """Přidání nového výdaje"""
        try:
            # Validace názvu
            is_valid, result = InputValidator.validate_expense_name(name)
            if not is_valid:
                self.show_snackbar(f"❌ {result}")
                return
            validated_name = result
            
            # Validace částky
            is_valid, result = InputValidator.validate_expense_amount(amount)
            if not is_valid:
                self.show_snackbar(f"❌ {result}")
                return
            validated_amount = result
            
            # Validace dne
            is_valid, result = InputValidator.validate_expense_day(day)
            if not is_valid:
                self.show_snackbar(f"❌ {result}")
                return
            validated_day = result
            
            # Kontrola limitu výdajů
            current_expenses = self.db.get_expenses()
            if len(current_expenses) >= MAX_EXPENSES:
                self.show_snackbar(f"❌ Maximální počet výdajů je {MAX_EXPENSES}")
                return
            
            # Kontrola duplicity názvu
            for _, existing_name, _, _ in current_expenses:
                if existing_name.lower().strip() == validated_name.lower().strip():
                    self.show_snackbar("❌ Výdaj s tímto názvem již existuje")
                    return
            
            self.db.add_expense(validated_name, validated_amount, validated_day)
            self.load_expenses()
            if self.dialog:
                self.dialog.dismiss()  # type: ignore
                self.dialog = None  # Uvolnění paměti
            self.show_snackbar(f"✅ Výdaj '{validated_name}' byl přidán!")
            
        except Exception as e:
            error_msg = ErrorHandler.handle_database_error(e, "přidávání výdaje")
            self.show_snackbar(f"❌ {error_msg}")
    
    def show_delete_expense_dialog(self, expense_id):
        """Dialog pro potvrzení smazání výdaje"""
        if self.dialog:
            self.dialog.dismiss()  # type: ignore
            self.dialog = None  # Uvolnění paměti
            
        # Najdeme název výdaje
        expenses = self.db.get_expenses()
        expense_name = "výdaj"
        expense_amount = 0
        for exp_id, name, amount, day in expenses:
            if exp_id == expense_id:
                expense_name = name
                expense_amount = amount
                break
        
        self.dialog = MDDialog(
            title="🗑️ Smazat výdaj",
            text=f"Opravdu chcete smazat výdaj:\n\n💰 {expense_name}\n💳 {expense_amount:.0f} Kč\n\nTato akce je nevratná.",
            size_hint=(0.8, None),
            buttons=[
                MDRaisedButton(
                    text="ZRUŠIT",
                    theme_text_color="Primary",
                    on_release=lambda x: self.dialog.dismiss() if self.dialog else None  # type: ignore
                ),
                MDRaisedButton(
                    text="SMAZAT",
                    md_bg_color=[0.8, 0.2, 0.2, 1],  # Červená barva
                    on_release=lambda x: self.confirm_delete_expense(expense_id)
                )
            ]
        )
        self.dialog.open()
    
    def confirm_delete_expense(self, expense_id):
        """Potvrzení smazání výdaje"""
        self.delete_expense(expense_id)
        if self.dialog:
            self.dialog.dismiss()  # type: ignore
            self.dialog = None  # Uvolnění paměti

    def delete_expense(self, expense_id):
        """Smazání výdaje"""
        self.db.delete_expense(expense_id)
        self.load_expenses()
        self.show_snackbar("🗑️ Výdaj byl úspěšně smazán")
    
    def show_snackbar(self, message):
        """Zobrazení snackbaru s konfigurovatelnou dobou trvání"""
        # Fix pro kompatibilitu s KivyMD 1.2.0
        snackbar = Snackbar()
        snackbar.text = message
        snackbar.duration = SNACKBAR_DURATION
        snackbar.open()
    
    def on_start(self):
        """Spuštění aplikace"""
        self.update_main_screen()


if __name__ == '__main__':
    app = XpenseApp()
    app.run()
