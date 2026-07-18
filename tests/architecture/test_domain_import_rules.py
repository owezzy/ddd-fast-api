"""Architecture tests for domain-layer import boundaries."""

from __future__ import annotations

import ast
from pathlib import Path

DOMAIN_ROOT = Path(__file__).resolve().parents[2] / "src" / "ddd_fast_api" / "domain"
FORBIDDEN_IMPORT_PREFIXES = (
    "fastapi",
    "pydantic",
    "sqlalchemy",
    "starlette",
    "uvicorn",
    "ddd_fast_api.infrastructure",
    "ddd_fast_api.entrypoints",
)


def _iter_domain_python_files() -> list[Path]:
    return sorted(path for path in DOMAIN_ROOT.rglob("*.py") if path.is_file())


def _extract_import_targets(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    targets: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            targets.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            targets.append(node.module)

    return targets


def test_domain_layer_avoids_framework_and_outer_layer_imports() -> None:
    violations: list[str] = []

    for path in _iter_domain_python_files():
        for target in _extract_import_targets(path):
            if target.startswith(FORBIDDEN_IMPORT_PREFIXES):
                violations.append(f"{path.relative_to(DOMAIN_ROOT.parent.parent)} imports {target}")

    assert violations == []
