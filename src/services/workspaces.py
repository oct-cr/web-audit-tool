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


def get_node_by_path(sites, path):
    parts = path.split(":", 1)
    site_key = parts[0]
    page_key = parts[1] if len(parts) > 1 else None

    site = find_site(sites, site_key)
    if site is None:
        return None

    if page_key is None:
        return {
            **site,
            "node_type": "site",
        }

    pages = site.get("pages", {})
    page = pages.get(page_key)

    if page:
        return {
            **page,
            "node_type": "page",
        }

    return None
