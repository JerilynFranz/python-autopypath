"""Tests for autopypath._config_py_path._config."""

from functools import cache
import itertools
from pathlib import Path
from types import MappingProxyType
from typing import Union, NamedTuple, Iterator


import pytest

from testspec import TestSpec, PytestAction

from autopypath._config_py_path._config import Config
from autopypath.load_strategy import LoadStrategy
from autopypath.marker_type import MarkerType
from autopypath.path_resolution import PathResolution


class ConfigParameters(NamedTuple):
    """Combination of Config parameters for testing.

    :param Union[MappingProxyType[str, MarkerType], None] repo_markers: Repository markers.
    :param Union[tuple[str, ...], tuple[Path, ...], None] paths: Additional paths.
    :param Union[LoadStrategy, str, None] load_strategy: Load strategy.
    :param Union[tuple[Union[PathResolution, str], ...], None] path_resolution_order: Path resolution order.
    """

    repo_markers: Union[MappingProxyType[str, MarkerType], None]
    paths: Union[tuple[str, ...], tuple[Path, ...], None]
    load_strategy: Union[LoadStrategy, str, None]
    path_resolution_order: Union[tuple[Union[PathResolution, str], ...], None]


# fmt: off

@pytest.mark.parametrize(
    'testspec', [
        PytestAction('MARKER_001',
            name='Create Config with valid repo_markers',
            action=Config,
            kwargs={'repo_markers': {'.git': MarkerType.DIR, 'pyproject.toml': MarkerType.FILE}},
            validate_attr='repo_markers',
            expected={'.git': MarkerType.DIR, 'pyproject.toml': MarkerType.FILE}),
        PytestAction('MARKER_002',
            name='Create Config with empty repo_markers',
            action=Config, kwargs={'repo_markers': {}},
            validate_attr='repo_markers', expected={}),
        PytestAction('MARKER_003',
            name='Create Config with single repo_marker',
            action=Config, kwargs={'repo_markers': {'setup.py': MarkerType.FILE}},
            validate_attr='repo_markers', expected={'setup.py': MarkerType.FILE}),
        PytestAction('MARKER_004',
            name='Create Config with string repo_markers',
            action=Config, kwargs={'repo_markers': {'.git': 'dir', 'setup.py': 'file'}},
            validate_attr='repo_markers', expected={'.git': MarkerType.DIR, 'setup.py': MarkerType.FILE}),
        PytestAction('MARKER_005',
            name='Create Config with mixed type repo_markers',
            action=Config, kwargs={'repo_markers': {'.git': MarkerType.DIR, 'setup.py': 'file'}},
            validate_attr='repo_markers', expected={'.git': MarkerType.DIR, 'setup.py': MarkerType.FILE}),
        PytestAction('MARKER_006',
            name='Create Config with invalid repo_marker',
            action=Config, kwargs={'repo_markers': {'.git': 'DIR'}},
            exception=ValueError),
        PytestAction('MARKER_007',
            name='Create Config with invalid repo_marker type',
            action=Config, kwargs={'repo_markers': {'.git': 123}},
            exception=TypeError),
        PytestAction('MARKER_008',
            name='Create Config with None repo_markers',
            action=Config, kwargs={'repo_markers': None},
            validate_attr='repo_markers', expected=None),
        PytestAction('MARKER_009',
            name='Create Config with no repo_markers',
            action=Config, kwargs={},
            validate_attr='repo_markers', expected=None),
        PytestAction('MARKER_010',
            name='Create Config with whitespace repo_marker key',
            action=Config, kwargs={'repo_markers': {'   ': MarkerType.DIR}},
            exception=ValueError),
        PytestAction('MARKER_011',
            name='Create Config with non-string repo_marker key',
            action=Config, kwargs={'repo_markers': {123: MarkerType.DIR}},
            exception=TypeError),
        PytestAction('MARKER_012',
            name='Create Config with non-mapping repo_markers',
            action=Config, kwargs={'repo_markers': [('setup.py', MarkerType.FILE)]},
            exception=TypeError),
        PytestAction('MARKER_013',
            name='Create Config with repo_marker key exceeding max length',
            action=Config, kwargs={'repo_markers': {'a' * 65: MarkerType.DIR}},
            exception=ValueError),
        PytestAction('MARKER_014',
            name='Create Config with repo_marker key containing path separator',
            action=Config, kwargs={'repo_markers': {'inva/lid': MarkerType.DIR}},
            exception=ValueError),
        PytestAction('MARKER_015',
            name='Create Config with repo_marker key being Windows reserved name',
            action=Config, kwargs={'repo_markers': {'CON': MarkerType.FILE}},
            exception=ValueError),
        PytestAction('MARKER_016',
            name='Create Config with repo_marker key containing forbidden characters',
            action=Config, kwargs={'repo_markers': {'inva<lid': MarkerType.FILE}},
            exception=ValueError),
        PytestAction('MARKER_017',
            name='Create Config with repo_marker key being empty string',
            action=Config, kwargs={'repo_markers': {'': MarkerType.FILE}},
            exception=ValueError),
        PytestAction('MARKER_018',
            name='Create Config with repo_marker key having leading whitespace',
            action=Config, kwargs={'repo_markers': {'  setup.py': MarkerType.FILE}},
            exception=ValueError),
        PytestAction('MARKER_019',
            name='Create Config with repo_marker key having trailing whitespace',
            action=Config, kwargs={'repo_markers': {'setup.py  ': MarkerType.FILE}},
            exception=ValueError),
        PytestAction('MARKER_020',
            name='Create Config with repo_marker key containing null character',
            action=Config, kwargs={'repo_markers': {'setup\0.py': MarkerType.FILE}},
            exception=ValueError),
    ]
)
def test_repo_markers(testspec: TestSpec) -> None:
    """Test Config with repo_markers."""
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('PATHS_001',
        name='Create Config with valid list of paths',
        action=Config, kwargs={'paths': ['src', 'lib', 'utils']},
        validate_attr='paths', expected=(Path('src'), Path('lib'), Path('utils'))),
    PytestAction('PATHS_002',
        name='Create Config with empty paths',
        action=Config, kwargs={'paths': []},
        validate_attr='paths', expected=None),
    PytestAction('PATHS_003',
        name='Create Config with single path',
        action=Config, kwargs={'paths': ['src']},
        validate_attr='paths', expected=(Path('src'),)),
    PytestAction('PATHS_004',
        name='Create Config with None paths',
        action=Config, kwargs={'paths': None},
        validate_attr='paths', expected=None),
    PytestAction('PATHS_005',
        name='Create Config with no paths',
        action=Config, kwargs={},
        validate_attr='paths', expected=None),
    PytestAction('PATHS_006',
        name='Create Config with invalid path type',
        action=Config, kwargs={'paths': ['src', 123, 'utils']},
        exception=TypeError),
    PytestAction('PATHS_007',
        name='Create Config with Path objects',
        action=Config, kwargs={'paths': [Path('src'), Path('lib')]},
        validate_attr='paths', expected=(Path('src'), Path('lib'))),
    PytestAction('PATHS_008',
        name='Create Config with path having leading whitespace',
        action=Config, kwargs={'paths': ['  src', 'lib']},
        exception=ValueError),
    PytestAction('PATHS_009',
        name='Create Config with path having trailing whitespace',
        action=Config, kwargs={'paths': ['src  ', 'lib']},
        exception=ValueError),
    PytestAction('PATHS_010',
        name='Create Config with path being only whitespace',
        action=Config, kwargs={'paths': ['   ', 'lib']},
        exception=ValueError),
    PytestAction('PATHS_011',
        name='Create Config with path being only forward slashes',
        action=Config, kwargs={'paths': ['///', 'lib']},
        exception=ValueError),
    PytestAction('PATHS_012',
        name='Create Config with path being only backslashes',
        action=Config, kwargs={'paths': ['\\\\\\', 'lib']},
        exception=ValueError),
    PytestAction('PATHS_013',
        name='Create Config with path having segment with leading whitespace',
        action=Config, kwargs={'paths': ['src/  utils', 'lib']},
        exception=ValueError),
    PytestAction('PATHS_014',
        name='Create Config with path having segment with trailing whitespace',
        action=Config, kwargs={'paths': ['src/utils  ', 'lib']},
        exception=ValueError),
    PytestAction('PATHS_015',
        name='Create Config with path having whitespace segment',
        action=Config, kwargs={'paths': ['src/ /utils', 'lib']},
        exception=ValueError),
    PytestAction('PATHS_016',
        name='Create Config with Path having segment being only whitespace',
        action=Config, kwargs={'paths': [Path('src/   /utils'), Path('lib')]},
        exception=ValueError),
    PytestAction('PATHS_017',
        name='Create Config with Path having segment with leading whitespace',
        action=Config, kwargs={'paths': [Path('src/  utils'), Path('lib')]},
        exception=ValueError),
    PytestAction('PATHS_018',
        name='Create Config with Path having segment with trailing whitespace',
        action=Config, kwargs={'paths': [Path('src/utils  /more'), Path('lib')]},
        exception=ValueError),
    PytestAction('PATHS_019',
        name='Create config with path being empty string',
        action=Config, kwargs={'paths': ['']},
        exception=ValueError),
    PytestAction('PATHS_020',
        name='Create config with path being neither str nor Path',
        action=Config, kwargs={'paths': [123]},
        exception=TypeError),
    PytestAction('PATHS_021',
        name='Create config with paths being neither sequence nor None',
        action=Config, kwargs={'paths': 123},
        exception=TypeError),
])
def test_paths(testspec: TestSpec) -> None:
    """Test Config with paths"""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('LOAD_001',
        name='Create Config with valid load_strategy',
        action=Config,
        kwargs={'load_strategy': LoadStrategy.MERGE},
        validate_attr='load_strategy',
        expected=LoadStrategy.MERGE),
    PytestAction('LOAD_002',
        name='Create Config with load_strategy as string',
        action=Config,
        kwargs={'load_strategy': 'merge'},
        validate_attr='load_strategy',
        expected=LoadStrategy.MERGE),
    PytestAction('LOAD_003',
        name='Create Config with invalid load_strategy string',
        action=Config,
        kwargs={'load_strategy': 'invalid_strategy'},
        exception=ValueError),
    PytestAction('LOAD_004',
        name='Create Config with invalid load_strategy type',
        action=Config,
        kwargs={'load_strategy': 123},
        exception=TypeError),
    PytestAction('LOAD_005',
        name='Create Config with no load_strategy',
        action=Config,
        kwargs={},
        validate_attr='load_strategy',
        expected=None),
    PytestAction('LOAD_006',
        name='Create Config with None load_strategy',
        action=Config,
        kwargs={'load_strategy': None},
        validate_attr='load_strategy')
])
def test_load_strategy(testspec: TestSpec) -> None:
    """Test Config with load_strategy"""
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('RESOLVE_001',
        name='Create Config with valid path_resolution_order',
        action=Config,
        kwargs={'path_resolution_order': [ 'manual', 'pyproject', 'dotenv']},
        validate_attr='path_resolution_order',
        expected=(PathResolution.MANUAL, PathResolution.PYPROJECT, PathResolution.DOTENV)),
    PytestAction('RESOLVE_002',
        name='Create Config with path_resolution_order as enums',
        action=Config,
        kwargs={'path_resolution_order': [PathResolution.DOTENV, PathResolution.MANUAL]},
        validate_attr='path_resolution_order',
        expected=(PathResolution.DOTENV, PathResolution.MANUAL)),
    PytestAction('RESOLVE_003',
        name='Create Config with invalid path_resolution_order string',
        action=Config,
        kwargs={'path_resolution_order': ['invalid_source']},
        exception=ValueError),
    PytestAction('RESOLVE_004',
        name='Create Config with invalid path_resolution_order type',
        action=Config,
        kwargs={'path_resolution_order': [123]},
        exception=TypeError),
    PytestAction('RESOLVE_005',
        name='Create Config with empty path_resolution_order',
        action=Config,
        kwargs={'path_resolution_order': []},
        validate_attr='path_resolution_order',
        expected=None),
    PytestAction('RESOLVE_006',
        name='Create Config with None path_resolution_order',
        action=Config,
        kwargs={'path_resolution_order': None},
        validate_attr='path_resolution_order',
        expected=None),
    PytestAction('RESOLVE_007',
        name='Create Config with no path_resolution_order',
        action=Config,
        kwargs={},
        validate_attr='path_resolution_order',
        expected=None),
    PytestAction('RESOLVE_008',
        name='Create Config with duplicate path_resolution_order entries',
        action=Config,
        kwargs={'path_resolution_order': ['manual', 'pyproject', 'manual']},
        exception=ValueError),
    PytestAction('RESOLVE_009',
        name='Create Config with single path_resolution_order entry',
        action=Config,
        kwargs={'path_resolution_order': ['dotenv']},
        validate_attr='path_resolution_order',
        expected=(PathResolution.DOTENV,)),
    PytestAction('RESOLVE_010',
        name='Create Config with mixed type path_resolution_order entries',
        action=Config,
        kwargs={'path_resolution_order': ['manual', PathResolution.DOTENV, 'pyproject']},
        validate_attr='path_resolution_order',
        expected=(PathResolution.MANUAL, PathResolution.DOTENV, PathResolution.PYPROJECT)),
    PytestAction('RESOLVE_011',
        name='Create Config with path_resolution_order having leading/trailing whitespace',
        action=Config,
        kwargs={'path_resolution_order': [' manual ', 'pyproject']},
        exception=ValueError),
    PytestAction('RESOLVE_012',
        name='Create Config with path_resolution_order being neither sequence nor None',
        action=Config,
        kwargs={'path_resolution_order': 123},
        exception=TypeError),
    PytestAction('RESOLVE_013',
        name='Create Config with path_resolution_order containing non-str/non-enum',
        action=Config,
        kwargs={'path_resolution_order': ['manual', 123]},
        exception=TypeError),
    PytestAction('RESOLVE_014',
        name="Create config with path_resolution_order as a string",
        action=Config,
        kwargs={'path_resolution_order': 'manual'},
        exception=TypeError),
])
def test_path_resolution_order(testspec: TestSpec) -> None:
    """Test Config with path_resolution_order"""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('REPLACE_001',
        name='Use replace method to change repo_markers of Config',
        action=Config().replace,
        kwargs={'repo_markers': {'.hg': MarkerType.DIR}},
        validate_attr='repo_markers',
        expected={'.hg': MarkerType.DIR}),
    PytestAction('REPLACE_002',
        name='Use replace method to change paths of Config',
        action=Config().replace, kwargs={'paths': ['new_src', 'new_lib']},
        validate_attr='paths',
        expected=(Path('new_src'), Path('new_lib'))),
    PytestAction('REPLACE_003',
        name='Use replace method to change load_strategy of Config',
        action=Config().replace, kwargs={'load_strategy': LoadStrategy.REPLACE},
        validate_attr='load_strategy',
        expected=LoadStrategy.REPLACE),
    PytestAction('REPLACE_004',
        name='Use replace method to change path_resolution_order of Config',
        action=Config().replace, kwargs={'path_resolution_order': ['dotenv', 'manual']},
        validate_attr='path_resolution_order',
        expected=(PathResolution.DOTENV, PathResolution.MANUAL)),
    PytestAction('REPLACE_005',
        name='Use replace method with multiple changes to Config',
        action=Config().replace,
        kwargs={
            'repo_markers': {'.svn': MarkerType.DIR},
            'paths': ['another_src'],
            'load_strategy': 'merge_highest_priority',
            'path_resolution_order': [PathResolution.PYPROJECT]
        },
        validate_attr='repo_markers',
        expected={'.svn': MarkerType.DIR}),
])
def test_replace(testspec: TestSpec) -> None:
    """Test Config replace method."""
    testspec.run()


@cache
def generate_all_config_combinations() -> tuple[tuple[Config, ConfigParameters], ...]:
    """Generate all combinations of Config parameters for testing.

    Cached after first call to improve performance.

    Creates Config instances for every test combination of the following parameters:
    - repo_markers
    - paths
    - load_strategy
    - path_resolution_order

    :return tuple[tuple[Config, ConfigParameters], ...]: A tuple containing all generated Config instances and
        their corresponding parameter combinations.
    """
    repo_markers: tuple[Union[MappingProxyType[str, MarkerType], None], ...] = (
        MappingProxyType({'.git': MarkerType.DIR}),
        MappingProxyType({'pyproject.toml': MarkerType.FILE}),
        MappingProxyType({'.git': MarkerType.DIR, 'pyproject.toml': MarkerType.FILE}),
        None,
    )

    paths: tuple[Union[tuple[str, ...], tuple[Path, ...], None], ...] = (
        ('src', 'lib'),
        ('utils',),
        None
    )

    load_strategies: tuple[Union[LoadStrategy, str, None], ...] = (
        LoadStrategy.MERGE,
        LoadStrategy.REPLACE,
        LoadStrategy.MERGE_HIGHEST_PRIORITY,
        None,
    )

    path_resolution_orders: tuple[Union[tuple[Union[PathResolution, str], ...], None], ...] = (
        (PathResolution.MANUAL, PathResolution.PYPROJECT),
        (PathResolution.DOTENV,),
        None,
    )

    # generate all combinations of the above parameters and creates tuples of
    # (Config instance, ConfigParameters) for each combination
    configs = []
    for rm, p, ls, pro in itertools.product(repo_markers, paths, load_strategies, path_resolution_orders):
        config = Config(
                repo_markers=rm,
                paths=p,
                load_strategy=ls,
                path_resolution_order=pro)
        combination = ConfigParameters(rm, p, ls, pro)
        configs.append((config, combination))

    return tuple(configs)


# Efficiently generate only (i, j) pairs where i <= j to avoid redundant equality checks
# By making this a generator, we avoid storing all pairs in memory at once.
def config_combinations_pairs() -> Iterator[tuple[tuple[Config, ConfigParameters], tuple[Config, ConfigParameters]]]:
    configs: tuple[tuple[Config, ConfigParameters], ...] = generate_all_config_combinations()
    n: int = len(configs)
    for i in range(n):
        for j in range(i, n):
            yield (configs[i], configs[j])


def test_eq() -> None:
    """Test Config equality comparison.

    Fails on first mismatch found.
    """
    n_combinations = len(generate_all_config_combinations())
    lower_limit_of_comparisons = n_combinations * (n_combinations + 1) // 2  # n * (n + 1) / 2
    counter = 0
    for config_a, config_b in config_combinations_pairs():
        assert (config_a[0] == config_b[0]) == (config_a[1] == config_b[1]), (
            f'EQ_001 Config equality failed for combinations: '
            f'Config A parameters: {config_a[1]} and '
            f'Config B parameters: {config_b[1]}'
        )
        counter += 1
    assert counter >= lower_limit_of_comparisons, (
        f"EQ_002 Test did not compare enough Config combinations: only {counter} comparisons made."
        f" Expected at least {lower_limit_of_comparisons}.")

    instance = Config()
    result = instance == "not a config"
    assert not result, "EQ_003 Config __eq__ did not return False for a non-Config comparison."

def test_hash() -> None:
    """Test Config hashing.

    Fails on first mismatch found.
    """
    n_combinations = len(generate_all_config_combinations())
    lower_limit_of_comparisons = n_combinations * (n_combinations + 1) // 2  # n * (n + 1) / 2
    counter = 0
    for config_a, config_b in config_combinations_pairs():
        assert (hash(config_a[0]) == hash(config_b[0])) == (config_a[1] == config_b[1]), (
            f'HASH_001 Config hash comparison failed for combinations: '
            f'Config A parameters: {config_a[1]} and '
            f'Config B parameters: {config_b[1]}'
        )
        counter += 1
    assert counter >= lower_limit_of_comparisons, (
        f"HASH_002 Test did not compare enough Config combinations: only {counter} comparisons made."
        f" Expected at least {lower_limit_of_comparisons}.")


def test_repr_str() -> None:
    """Test Config __repr__ and __str__ methods."""
    config = Config(
        repo_markers={'.git': MarkerType.DIR},
        paths=['src', 'lib'],
        load_strategy=LoadStrategy.MERGE,
        path_resolution_order=[PathResolution.MANUAL, PathResolution.PYPROJECT]
    )

    expected_repr = (
        "Config("
        "repo_markers={'.git': MarkerType.DIR}, "
        "paths=['src', 'lib'], "
        "load_strategy=LoadStrategy.MERGE, "
        "path_resolution_order=[PathResolution.MANUAL, PathResolution.PYPROJECT]"
        ")"
    )
    repr_output = repr(config)
    assert repr_output == expected_repr, (
        "REPR_001 Config __repr__ output mismatch. "
        f"Expected: {expected_repr}, Got: {repr_output}"
    )

def test_str() -> None:
    config = Config(
        repo_markers={'.git': MarkerType.DIR},
        paths=['src', 'lib'],
        load_strategy=LoadStrategy.MERGE,
        path_resolution_order=[PathResolution.MANUAL, PathResolution.PYPROJECT]
    )
    expected_str = (
        "Config("
        "repo_markers={'.git': MarkerType.DIR}, "
        "paths=['src', 'lib'], "
        "load_strategy=LoadStrategy.MERGE, "
        "path_resolution_order=[PathResolution.MANUAL, PathResolution.PYPROJECT]"
        ")"
    )
    assert str(config) == expected_str, "STR_001 Config __str__ output mismatch."




# fmt: on
