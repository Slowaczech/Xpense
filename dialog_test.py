"""
Test dialogu pro přidání výdaje
"""

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp


class DialogTestApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(50),
            spacing=dp(30)
        )
        
        test_btn = MDRaisedButton(
            text="TEST DIALOG",
            size_hint=(1, None),
            height=dp(50),
            on_release=self.show_test_dialog
        )
        
        main_layout.add_widget(test_btn)
        return main_layout
    
    def show_test_dialog(self, *args):
        """Test dialog s novým layoutem"""
        if self.dialog:
            self.dialog.dismiss()
        
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            size_hint_y=None,
            height=dp(280)
        )
        
        # Název výdaje
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
        
        # Částka
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
        
        # Den
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
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="PŘIDAT",
                    md_bg_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()


if __name__ == '__main__':
    DialogTestApp().run()
