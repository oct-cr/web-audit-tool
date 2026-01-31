import re
import urllib.parse


def get_filename_from_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    base = (parsed.netloc or "") + (parsed.path or "")

    base = re.sub(r"^https?://", "", base)
    name = re.sub(r"[^A-Za-z0-9_-]+", "-", base).strip("-")

    return name
