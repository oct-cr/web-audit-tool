import yaml


def load_sites(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def find_site(sites, key):
    key_l = key.lower()
    for s in sites:
        if s.get("key") == key:
            return s
        if s.get("name", "").lower() == key_l:
            return s
    return None


def get_site_urls(site):
    urls = []
    if site:
        pages = site.get("pages", {})
        for page in pages.values():
            url = page.get("url")
            if url:
                urls.append(url)
    return urls
