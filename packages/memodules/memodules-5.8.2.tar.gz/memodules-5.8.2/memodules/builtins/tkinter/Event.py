from dataclasses import dataclass
from typing import Literal

__all__ = [
    'Conbobox',
    'Listbox',
    'Text',
    'Tk',
    'Toplevel',
]


@dataclass(frozen=True)
class Window:
    Resize: Literal["<Configure>"] = "<Configure>"
    """Example:
        my_window.bind(Resize, lambda event: print(event))"""


@dataclass(frozen=True)
class TextWidget:
    PressEnter: Literal["<Return>"] = "<Return>"
    "Events when the Enter key is pressed"
    AnyKey: Literal["<Key>"] = "<Key>"
    "Events when any key is pressed"


@dataclass(frozen=True)
class ListWidget:
    ItemSelect: Literal['<<ListboxSelect>>'] = '<<ListboxSelect>>'
    "Events when the any item is selected"


@dataclass(frozen=True)
class ConboboxWidget:
    ChangeValueByList: Literal['<<ComboboxSelected>>'] = '<<ComboboxSelected>>'
    "An event when a value is changed from the dropdown list."
    ItemSelected: Literal['<<ComboboxSelected>>'] = '<<ComboboxSelected>>'
    "An event when a value is changed from the dropdown list."
    SelectionChange: Literal['<<ComboboxSelected>>'] = '<<ComboboxSelected>>'
    "An event when a value is changed from the dropdown list."


Conbobox = ConboboxWidget()
Listbox = ListWidget()
Text = TextWidget()
Tk = Window()
Toplevel = Window()
