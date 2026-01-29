import argparse
import os
import sys

from rich.console import Console

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from sections.sitesummary.dataprovider import get_site_summary
from sections.sitesummary.view import get_site_summary_view


from services.workspaces import load_sites, find_site


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("site_key", help="Site key to look up")
    args = p.parse_args(argv)

    sites = load_sites("sites.yaml")
    site = find_site(sites, args.site_key)

    if site is None:
        raise ValueError(f"Site not found: {args.site_key}")

    site_summary = get_site_summary(site)

    console = Console()
    console.print(get_site_summary_view(site_summary))


if __name__ == "__main__":
    sys.exit(main())
