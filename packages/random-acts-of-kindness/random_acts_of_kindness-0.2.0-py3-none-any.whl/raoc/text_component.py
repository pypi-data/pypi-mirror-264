"""."""

import flet as ft
import random

TEXT_COLORS = ['red', 'blue', 'green', 'black', 'indigo', 'cyan', 'pink', 'orange']


def update_text_control(text_control: ft.Text, text: str, explanation: str) -> None:
    """."""
    text_control.value = text
    text_control.tooltip = explanation
    text_control.size = 20
    text_control.color = random.choice(TEXT_COLORS)
    text_control.weight = ft.FontWeight.BOLD

