from rich.text import Text

icons = {
    "0": "•",
    "1": "✔",
    "2": "⚠",
    "3": "✖",
}


def get_color_from_status(status: int | None) -> str:
    if status is None:
        return "grey50"
    try:
        s = int(status)
    except Exception:
        return "grey50"

    if s == 1:
        return "dark_green"
    if s == 2:
        return "dark_goldenrod"
    if s == 3:
        return "deep_pink3"

    return "grey50"


def get_text_with_status_color(text: str, status: int | None) -> Text:
    return Text(text, style=get_color_from_status(status))


def get_status_icon(status: int | None) -> Text:
    return get_text_with_status_color(
        icons.get(str(status), "•"),
        status,
    )
