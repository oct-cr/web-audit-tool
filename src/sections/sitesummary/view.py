from modules.lighthouse.terminal import get_summary_table


def get_site_summary_view(site_summary):
    return get_summary_table(site_summary["lighthouse_summary_rows"])
