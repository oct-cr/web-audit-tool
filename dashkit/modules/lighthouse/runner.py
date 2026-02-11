from ...services.snapshots import write_snapshot
from .http import fetch_lighthouse


def run_lighthouse_report(
    url: str,
    api_key: str,
    strategy: str = "Mobile",
    workspace_key: str = "",
    snapshot_key: str = "",
):
    print(f"Running Lighthouse for {url}...")
    body = fetch_lighthouse(url, api_key=api_key, strategy=strategy)

    if body is None:
        raise RuntimeError("Lighthouse run failed.")

    out_path = write_snapshot(workspace_key, snapshot_key, body)

    print(f"Report saved to: {out_path}")
    return out_path
