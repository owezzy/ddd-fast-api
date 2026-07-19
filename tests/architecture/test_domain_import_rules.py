"""Architecture tests for layer import boundaries."""

from __future__ import annotations

import ast
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "ddd_fast_api"
DOMAIN_ROOT = SRC_ROOT / "domain"
APPLICATION_ROOT = SRC_ROOT / "application"
FOUNDATION_ROOT = SRC_ROOT / "foundation"

DOMAIN_FORBIDDEN_IMPORT_PREFIXES = (
    "fastapi",
    "pydantic",
    "sqlalchemy",
    "starlette",
    "uvicorn",
    "ddd_fast_api.infrastructure",
    "ddd_fast_api.entrypoints",
)
APPLICATION_FORBIDDEN_IMPORT_PREFIXES = (
    "fastapi",
    "pydantic",
    "sqlalchemy",
    "starlette",
    "uvicorn",
    "ddd_fast_api.infrastructure",
    "ddd_fast_api.entrypoints",
)
FOUNDATION_FORBIDDEN_IMPORT_PREFIXES = (
    "ddd_fast_api.application",
    "ddd_fast_api.domain",
    "ddd_fast_api.entrypoints",
    "ddd_fast_api.infrastructure",
)


def _iter_python_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.py") if path.is_file())


def _extract_import_targets(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    targets: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            targets.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            targets.append(node.module)

    return targets


def _find_violations(root: Path, forbidden_prefixes: tuple[str, ...]) -> list[str]:
    violations: list[str] = []

    for path in _iter_python_files(root):
        for target in _extract_import_targets(path):
            if target.startswith(forbidden_prefixes):
                violations.append(f"{path.relative_to(SRC_ROOT.parent)} imports {target}")

    return violations


def test_domain_layer_avoids_framework_and_outer_layer_imports() -> None:
    violations = _find_violations(DOMAIN_ROOT, DOMAIN_FORBIDDEN_IMPORT_PREFIXES)

    assert violations == []


def test_application_layer_avoids_framework_and_outer_layer_imports() -> None:
    violations = _find_violations(APPLICATION_ROOT, APPLICATION_FORBIDDEN_IMPORT_PREFIXES)

    assert violations == []


def test_foundation_layer_stays_independent_of_project_business_layers() -> None:
    violations = _find_violations(FOUNDATION_ROOT, FOUNDATION_FORBIDDEN_IMPORT_PREFIXES)

    assert violations == []
