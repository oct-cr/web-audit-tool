from rich.console import group


@group()
def get_rendered_view(widgets: list):
    for widget in widgets:
        data, view_fn = widget
        yield view_fn(data)
