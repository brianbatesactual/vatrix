# tests/test_pathing.py
# v1 testing program

import re
from pathlib import Path

from appdirs import user_data_dir

from vatrix.utils.pathing import get_output_path


def test_default_to_app_data_dir():
    path = get_output_path("logs.csv")
    expected_root = Path(user_data_dir("vatrix"))
    assert expected_root in path.parents
    assert path.name == "logs.csv"


def test_explicit_use_cwd():
    path = get_output_path("logs.csv", use_cwd=True)
    assert Path.cwd() in path.parents

    # Cleanup empty output dir
    output_dir = path.parent
    if output_dir.exists() and not any(output_dir.iterdir()):
        output_dir.rmdir()


def test_with_timestamp():
    path = get_output_path("output.json", timestamp=True)
    assert path.name.startswith("output_")
    assert path.suffix == ".json"
    assert re.match(r"output_\d{8}_\d{6}\.json", path.name)


def test_home_dir_usage():
    path = get_output_path("stream.csv", use_cwd=False)
    assert "vatrix" in str(path)  # should be in ~/.local/share/vatrix or equivalent
    assert path.name == "stream.csv"


def test_custom_subdir():
    path = get_output_path("logfile.log", subdir="custom_logs")
    assert "custom_logs" in str(path)


def test_extension_override():
    path = get_output_path("rendered", ext=".txt", timestamp=True)
    assert path.name.endswith(".txt")
    assert re.match(r"rendered_\d{8}_\d{6}\.txt", path.name)
