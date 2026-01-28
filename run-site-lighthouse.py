import os
import sys
from dotenv import load_dotenv

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

    exit_code = 0
    for page in pages_conf.values():
        url = page.get("url")
        if not url:
            continue
        rc = run_lighthouse_report(url, api_key=api_key)
        if rc != 0:
            exit_code = rc

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
