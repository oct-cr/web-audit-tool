def get_sidebar_items(sites):
    items = []

    if not sites:
        return items

    for s in sites:
        sitename = s.get("name")
        sitekey = s.get("key")

        if not sitename or not sitekey:
            raise ValueError("Site is missing 'name' or 'key'.")

        items.append({"label": sitename, "command": f"{sitekey}"})

        pages = s.get("pages", {})

        for key, page in pages.items():
            url = page.get("url")

            if url:
                items.append({"label": key.capitalize(), "command": f"{sitekey}:{key}"})

    return items
