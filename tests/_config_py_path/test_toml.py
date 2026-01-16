from pathlib import Path


from autopypath._config_py_path._config._toml import TomlConfig
from autopypath.marker_type import MarkerType
from autopypath.path_resolution import PathResolution
from autopypath.load_strategy import LoadStrategy


def test_toml_config_init(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    marker_file = repo_root / 'filename.txt'
    marker_file.touch()
    marker_dir = repo_root / 'dirname'
    marker_dir.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""
[tool.autopypath]
paths = ['src', 'lib']
load_strategy = 'prepend'
path_resolution_order = ['manual', 'autopypath', 'pyproject', 'dotenv']
""")
    config = TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
