"""
Minimální test Kivy aplikace pro ověření builderu
"""
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

class TestApp(MDApp):
    def build(self):
        return MDLabel(text="Hello Xpense Test!")

if __name__ == '__main__':
    TestApp().run()
