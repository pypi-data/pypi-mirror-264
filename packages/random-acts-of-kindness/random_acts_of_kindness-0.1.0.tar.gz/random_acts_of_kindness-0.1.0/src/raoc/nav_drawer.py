"""."""

import flet as ft


def on_change_in_drawer(e: ft.ControlEvent) -> None:
    """."""
    drawer: ft.NavigationDrawer = e.control
    print(drawer.selected_index)
    index = 0
    for control in drawer.controls:
        if isinstance(control, ft.NavigationDrawerDestination):
            if drawer.selected_index == index:
                print(control.label, index)
            index += 1


def get_nav_drawer() -> ft.NavigationDrawer:
    """."""
    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(label="Item 1"),
            ft.Divider(thickness=1),
            ft.NavigationDrawerDestination(label="Item 2"),
            ft.NavigationDrawerDestination(label="Item 3"),
        ],
    )
    drawer.on_change = on_change_in_drawer
    return drawer
