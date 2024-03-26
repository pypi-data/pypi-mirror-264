"""."""

import flet as ft
from my_action import MyAction
from perform_action import perform_action

my_action = MyAction()


def my_page(page: ft.Page) -> None:
    """."""
    page.title = 'Flet example'
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    action_button = ft.ElevatedButton(icon=ft.icons.FORWARD, text='What could I do today...')
    text_control = ft.Text('')
    text_explanation = ft.Text('', size=15)
    image_control = ft.Image(src='/icon.png', height=512, fit=ft.ImageFit.CONTAIN)
    container = ft.Container(height=50)
    page.add(action_button, text_control, text_explanation, container, image_control)
    page.update()
    action_button.on_click = lambda event: perform_action(
        my_action, event, text_control, text_explanation, image_control)


def main() -> None:
    """."""
    ft.app(my_page, assets_dir='assets')


ft.app(my_page, assets_dir='assets')


