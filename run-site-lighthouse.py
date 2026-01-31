from datetime import datetime
from dotenv import load_dotenv
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from lighthouse import run_lighthouse_report
from services.workspaces import load_sites, find_site


def main():
    load_dotenv()
    site_key = sys.argv[1]
    sites_file = "sites.yaml"

    sites = load_sites(sites_file)
    site = find_site(sites, site_key)

    if not site:
        print(f"Site not found for key/name: {site_key}", file=sys.stderr)
        sys.exit(2)

    pages_conf = site.get("pages", {})
    api_key = os.environ.get("PAGESPEED_API_KEY")
    assert api_key, "PAGESPEED_API_KEY must be set"

    round_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for page in pages_conf.values():
        url = page.get("url")
        if not url:
            continue

        run_lighthouse_report(url, api_key=api_key, round_timestamp=round_timestamp)


if __name__ == "__main__":
    main()
