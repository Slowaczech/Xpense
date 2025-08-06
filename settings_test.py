"""
Finální test aplikace s nejjednodušším layoutem
"""

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.widget import Widget
from kivy.metrics import dp


class SettingsTestApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Toolbar
        toolbar = MDTopAppBar(
            title="Test nastavení",
            size_hint_y=None,
            height=dp(56)
        )
        main_layout.add_widget(toolbar)
        
        # Scroll view
        scroll = MDScrollView()
        
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(40),
            size_hint_y=None,
            padding=[dp(30), dp(40), dp(30), dp(40)]
        )
        content.bind(minimum_height=content.setter('height'))
        
        # Pole pro příjem
        income_label = MDLabel(
            text="Měsíční příjem (Kč)",
            size_hint_y=None,
            height=dp(30),
            theme_text_color="Primary"
        )
        income_field = MDTextField(
            hint_text="Zadejte příjem",
            size_hint_y=None,
            height=dp(50),
            multiline=False
        )
        
        # Pole pro den výplaty
        payday_label = MDLabel(
            text="Den výplaty (1-31)",
            size_hint_y=None,
            height=dp(30),
            theme_text_color="Primary"
        )
        payday_field = MDTextField(
            hint_text="Zadejte den výplaty",
            size_hint_y=None,
            height=dp(50),
            multiline=False
        )
        
        # Pole pro zůstatek
        balance_label = MDLabel(
            text="Aktuální zůstatek (Kč)",
            size_hint_y=None,
            height=dp(30),
            theme_text_color="Primary"
        )
        balance_field = MDTextField(
            hint_text="Zadejte zůstatek",
            size_hint_y=None,
            height=dp(50),
            multiline=False
        )
        
        # Tlačítko
        save_btn = MDRaisedButton(
            text="ULOŽIT",
            size_hint_y=None,
            height=dp(50)
        )
        
        # Přidání do layoutu
        content.add_widget(income_label)
        content.add_widget(income_field)
        content.add_widget(Widget(size_hint_y=None, height=dp(10)))
        content.add_widget(payday_label)
        content.add_widget(payday_field)
        content.add_widget(Widget(size_hint_y=None, height=dp(10)))
        content.add_widget(balance_label)
        content.add_widget(balance_field)
        content.add_widget(Widget(size_hint_y=None, height=dp(20)))
        content.add_widget(save_btn)
        
        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        
        return main_layout


if __name__ == '__main__':
    SettingsTestApp().run()
