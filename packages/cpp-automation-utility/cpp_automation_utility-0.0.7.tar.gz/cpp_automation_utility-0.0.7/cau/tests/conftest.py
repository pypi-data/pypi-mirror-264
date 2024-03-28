"""Test fixtures."""
import logging

import pytest

import cau

logger = logging.getLogger("CAU")

@pytest.fixture(name="mock_conan")
def _mock_conan(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Mocks Conan wrapper.

    Args:
        monkeypatch (pytest.MonkeyPatch): monkeypatch fixture
    """

    class MockProcess:
        returncode: int = 0

    class MockConan:

        def __init__(self, *args, **kwargs) -> None: # noqa: ANN003, ANN002
            pass

        def restore(self) -> MockProcess:
            print("Restored Conan")
            return MockProcess()

        def build(self) -> MockProcess:
            print("Build successful")
            return MockProcess()

        def clean_build(self) -> bool:
            print("Cleaned out build directory")
            return True

        def clean_conan(self) -> bool:
            print("Cleaned out conan directory")
            return True

    monkeypatch.setattr(cau, "Conan", lambda *args, **kwargs: MockConan(args, kwargs))

@pytest.fixture(name="mock_git")
def _mock_git(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Mocked git wrapper.

    Args:
        monkeypatch (pytest.MonkeyPatch): monkeypatch fixture
    """

    class MockGit:

        def changed_files(self) -> list:
            print("Got changes from git")
            return []

    monkeypatch.setattr(cau, "Git", MockGit)

@pytest.fixture(name="mock_tidy")
def _mock_tidy(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Mocked tidy wrapper.

    Args:
        monkeypatch (pytest.MonkeyPatch): monkeypatch fixture
    """

    class MockTidy:

        def __init__(self, *args, **kwargs) -> None: # noqa: ANN002, ANN003
            pass

        def lint(self) -> bool:
            print("Lint was successful")
            return True

    monkeypatch.setattr(cau, "Tidy", lambda *args, **kwargs: MockTidy(args, kwargs))

@pytest.fixture(name="mock_coverage")
def _mock_coverage(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Mocks coverage wrapper.

    Args:
        monkeypatch (pytest.MonkeyPatch): monkey patch fixture
    """

    class MockProcess:
        returncode: int = 0

    class MockCoverage:

        def __init__(self, *args, **kwargs) -> None: # noqa: ANN002, ANN003
            pass

        def run(self) -> MockProcess:
            print("Running coverage")
            return MockProcess()

    monkeypatch.setattr(cau, "Coverage", MockCoverage)
