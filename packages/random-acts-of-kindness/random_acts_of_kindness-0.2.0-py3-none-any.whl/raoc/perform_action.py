"""."""

from pathlib import Path

import flet as ft

from raoc.my_action import MyAction
from raoc.text_component import update_text_control
from raoc.file_name import get_file_name

ASSETS_PATH = Path('.')


def perform_action(action: MyAction,
                   event: ft.ControlEvent,
                   text_control: ft.Text,
                   text_explanation: ft.Text,
                   image_control: ft.Image) -> None:
    """."""
    page = event.page
    act_of_kindness, explanation = action.get_random_act_and_explanation()
    update_text_control(text_control, act_of_kindness, explanation)
    text_explanation.value = explanation
    image_control.src = f'{get_file_name(act_of_kindness)}.jpg'
    page.update()

