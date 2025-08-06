"""
Type stubs pro KivyMD komponenty
Řeší problémy s Pylance type checking
"""

from typing import Any, Optional, Callable, List
from kivymd.uix.dialog import MDDialog as _MDDialog

class MDDialog(_MDDialog):
    """Type stub pro MDDialog s dismiss metodou"""
    
    def dismiss(self, *args: Any) -> None:
        """Zavření dialogu"""
        ...
    
    def open(self) -> None:
        """Otevření dialogu"""
        ...
