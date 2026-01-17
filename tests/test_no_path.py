"""Tests for the _NoPath type in autopypath.types._no_path module."""
# mypy: disable-error-code=operator
# pyright: reportCallIssue=false

import pytest

from autopypath.types._no_path import _NoPath, _UsagePreventedType


@pytest.fixture
def no_path() -> _NoPath:
    return _NoPath()


def test_exists_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.exists(_UsagePreventedType())
    assert True, 'NOPATH_001: exists should raise NotImplementedError'


def test_is_file_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.is_file(_UsagePreventedType())
    assert True, 'NOPATH_002: is_file should raise NotImplementedError'


def test_is_dir_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.is_dir(_UsagePreventedType())
    assert True, 'NOPATH_003: is_dir should raise NotImplementedError'


def test_open_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.open(_UsagePreventedType())
    assert True, 'NOPATH_004: open should raise NotImplementedError'


def test_read_text_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.read_text(_UsagePreventedType())
    assert True, 'NOPATH_005: read_text should raise NotImplementedError'


def test_read_bytes_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.read_bytes(_UsagePreventedType())
    assert True, 'NOPATH_006: read_bytes should raise NotImplementedError'


def test_write_text_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.write_text(_UsagePreventedType())
    assert True, 'NOPATH_007: write_text should raise NotImplementedError'


def test_write_bytes_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.write_bytes(_UsagePreventedType())
    assert True, 'NOPATH_008: write_bytes should raise NotImplementedError'


def test_mkdir_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.mkdir(_UsagePreventedType())
    assert True, 'NOPATH_009: mkdir should raise NotImplementedError'


def test_rmdir_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.rmdir(_UsagePreventedType())
    assert True, 'NOPATH_010: rmdir should raise NotImplementedError'


def test_unlink_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.unlink(_UsagePreventedType())
    assert True, 'NOPATH_011: unlink should raise NotImplementedError'


def test_rename_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.rename(_UsagePreventedType())
    assert True, 'NOPATH_012: rename should raise NotImplementedError'


def test_replace_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.replace(_UsagePreventedType())
    assert True, 'NOPATH_013: replace should raise NotImplementedError'


def test_touch_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.touch(_UsagePreventedType())
    assert True, 'NOPATH_014: touch should raise NotImplementedError'


def test_stat_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.stat(_UsagePreventedType())
    assert True, 'NOPATH_015: stat should raise NotImplementedError'


def test_chmod_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.chmod(_UsagePreventedType())
    assert True, 'NOPATH_016: chmod should raise NotImplementedError'


def test_lstat_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.lstat(_UsagePreventedType())
    assert True, 'NOPATH_017: lstat should raise NotImplementedError'


def test_owner_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.owner(_UsagePreventedType())
    assert True, 'NOPATH_018: owner should raise NotImplementedError'


def test_group_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.group(_UsagePreventedType())
    assert True, 'NOPATH_019: group should raise NotImplementedError'


def test_readlink_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.readlink(_UsagePreventedType())
    assert True, 'NOPATH_020: readlink should raise NotImplementedError'


def test_symlink_to_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.symlink_to(_UsagePreventedType())
    assert True, 'NOPATH_021: symlink_to should raise NotImplementedError'


def test_hardlink_to_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.hardlink_to(_UsagePreventedType())
    assert True, 'NOPATH_022: hardlink_to should raise NotImplementedError'


def test_absolute_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.absolute(_UsagePreventedType())
    assert True, 'NOPATH_023: absolute should raise NotImplementedError'


def test_resolve_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.resolve(_UsagePreventedType())
    assert True, 'NOPATH_024: resolve should raise NotImplementedError'


def test_samefile_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.samefile(_UsagePreventedType())
    assert True, 'NOPATH_025: samefile should raise NotImplementedError'


def test_expanduser_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.expanduser(_UsagePreventedType())
    assert True, 'NOPATH_026: expanduser should raise NotImplementedError'


def test_with_name_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.with_name(_UsagePreventedType())
    assert True, 'NOPATH_027: with_name should raise NotImplementedError'


def test_with_suffix_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.with_suffix(_UsagePreventedType())
    assert True, 'NOPATH_028: with_suffix should raise NotImplementedError'


def test_relative_to_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.relative_to(_UsagePreventedType())
    assert True, 'NOPATH_029: relative_to should raise NotImplementedError'


def test_is_absolute_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.is_absolute(_UsagePreventedType())
    assert True, 'NOPATH_030: is_absolute should raise NotImplementedError'


def test_is_reserved_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.is_reserved(_UsagePreventedType())
    assert True, 'NOPATH_031: is_reserved should raise NotImplementedError'


def test_joinpath_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.joinpath(_UsagePreventedType())
    assert True, 'NOPATH_032: joinpath should raise NotImplementedError'


def test_match_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.match(_UsagePreventedType())
    assert True, 'NOPATH_033: match should raise NotImplementedError'


def test_parent_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        _ = no_path.parent
    assert True, 'NOPATH_034: parent should raise NotImplementedError'


def test_parents_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        _ = no_path.parents
    assert True, 'NOPATH_035: parents should raise NotImplementedError'


def test_parts_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        _ = no_path.parts
    assert True, 'NOPATH_036: parts should raise NotImplementedError'


def test_drive_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        _ = no_path.drive
    assert True, 'NOPATH_037: drive should raise NotImplementedError'


def test_root_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        _ = no_path.root
    assert True, 'NOPATH_038: root should raise NotImplementedError'


def test_anchor_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        _ = no_path.anchor
    assert True, 'NOPATH_039: anchor should raise NotImplementedError'


def test_name_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        _ = no_path.name
    assert True, 'NOPATH_040: name should raise NotImplementedError'


def test_suffix_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        _ = no_path.suffix
    assert True, 'NOPATH_041: suffix should raise NotImplementedError'


def test_suffixes_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        _ = no_path.suffixes
    assert True, 'NOPATH_042: suffixes should raise NotImplementedError'


def test_stem_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        _ = no_path.stem
    assert True, 'NOPATH_043: stem should raise NotImplementedError'


def test_as_posix_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.as_posix(_UsagePreventedType())
    assert True, 'NOPATH_044: as_posix should raise NotImplementedError'


def test_as_uri_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.as_uri(_UsagePreventedType())
    assert True, 'NOPATH_045: as_uri should raise NotImplementedError'


def test_is_mount_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.is_mount(_UsagePreventedType())
    assert True, 'NOPATH_046: is_mount should raise NotImplementedError'


def test_is_symlink_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.is_symlink(_UsagePreventedType())
    assert True, 'NOPATH_047: is_symlink should raise NotImplementedError'


def test_is_block_device_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.is_block_device(_UsagePreventedType())
    assert True, 'NOPATH_048: is_block_device should raise NotImplementedError'


def test_is_char_device_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.is_char_device(_UsagePreventedType())
    assert True, 'NOPATH_049: is_char_device should raise NotImplementedError'


def test_is_fifo_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.is_fifo(_UsagePreventedType())
    assert True, 'NOPATH_050: is_fifo should raise NotImplementedError'


def test_is_socket_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.is_socket(_UsagePreventedType())
    assert True, 'NOPATH_051: is_socket should raise NotImplementedError'


def test_iterdir_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.iterdir(_UsagePreventedType())
    assert True, 'NOPATH_052: iterdir should raise NotImplementedError'


def test_glob_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.glob(_UsagePreventedType())
    assert True, 'NOPATH_053: glob should raise NotImplementedError'


def test_rglob_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.rglob(_UsagePreventedType())
    assert True, 'NOPATH_054: rglob should raise NotImplementedError'


def test_cwd_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.cwd()
    assert True, 'NOPATH_055: cwd should raise NotImplementedError'


def test_home_raises(no_path: _NoPath) -> None:
    with pytest.raises(NotImplementedError, match='NoPath does not support IO operations.'):
        no_path.home()
    assert True, 'NOPATH_056: home should raise NotImplementedError'


def test_repr_returns_expected(no_path: _NoPath) -> None:
    assert repr(no_path) == '<NoPath>', 'NOPATH_057: __repr__ should return <NoPath>'


def test_str_returns_expected(no_path: _NoPath) -> None:
    assert str(no_path) == '<NoPath>', 'NOPATH_058: __str__ should return <NoPath>'


def test_eq_returns_true_for_no_path_instances(no_path: _NoPath) -> None:
    other = _NoPath()
    assert no_path == other, 'NOPATH_059: __eq__ should return True for two NoPath instances'


def test_eq_returns_false_for_non_no_path(no_path: _NoPath) -> None:
    assert not (no_path == object()), 'NOPATH_060: __eq__ should return False for non-NoPath objects'
