"""."""

from flet import Page


def show_nav_drawer(page: Page) -> None:
    """."""
    page.drawer.open = True
    page.update()
