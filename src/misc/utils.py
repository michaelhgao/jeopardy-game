import os
import sys


def resource_path(*paths: str) -> str:
    """
    Path to bundled, read-only resources
    """
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, *paths)


def app_path(*paths: str) -> str:
    """
    Path to writable, user-facing files
    """
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, *paths)
