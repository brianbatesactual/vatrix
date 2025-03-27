# vatrix/utils/helpers.py

# deprecated

import os

def project_root():
    """Return absolute path to the project root."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def path_from_root(relative_path):
    """Resolve a path from the project root."""
    return os.path.abspath(os.path.join(project_root(), relative_path))

def ensure_dir_exists(path):
    """Ensure directory for given path exists."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path