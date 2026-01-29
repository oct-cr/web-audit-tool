import os
import sys


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from src.dashkit.app import DashkitApp
from services.workspaces import load_sites


if __name__ == "__main__":
    workspace = load_sites("sites.yaml")
    DashkitApp(workspace).run()
