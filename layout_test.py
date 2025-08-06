"""
Rychlý test layoutu nastavení
"""

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp


class LayoutTestApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        scroll = MDScrollView()
        
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(30),
            size_hint_y=None,
            padding=[dp(20), dp(40), dp(20), dp(40)]
        )
        content.bind(minimum_height=content.setter('height'))
        
        # Test textová pole
        field1 = MDTextField(
            hint_text="Měsíční příjem",
            helper_text="Zadejte výši měsíčního příjmu v Kč",
            helper_text_mode="persistent",
            size_hint_y=None,
            height=dp(100)
        )
        
        field2 = MDTextField(
            hint_text="Den výplaty",
            helper_text="Den v měsíci kdy dostáváte výplatu (1-31)",
            helper_text_mode="persistent",
            size_hint_y=None,
            height=dp(100)
        )
        
        field3 = MDTextField(
            hint_text="Aktuální zůstatek",
            helper_text="Kolik peněz máte aktuálně k dispozici v Kč",
            helper_text_mode="persistent",
            size_hint_y=None,
            height=dp(100)
        )
        
        btn = MDRaisedButton(
            text="ULOŽIT NASTAVENÍ",
            size_hint=(1, None),
            height=dp(56)
        )
        
        content.add_widget(field1)
        content.add_widget(field2)
        content.add_widget(field3)
        content.add_widget(btn)
        
        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        
        return main_layout


if __name__ == '__main__':
    LayoutTestApp().run()
