#!/usr/bin/env python3
"""Create a deterministic, dependency-free snapshot of a local Git repository."""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


IGNORED_DIRS = {
    ".git", ".hg", ".svn", ".idea", ".vscode", ".venv", "venv",
    "node_modules", "dist", "build", "coverage", "target", "vendor",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
}

LANGUAGES = {
    ".py": "Python", ".js": "JavaScript", ".mjs": "JavaScript",
    ".cjs": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript",
    ".jsx": "JavaScript", ".rs": "Rust", ".go": "Go", ".java": "Java",
    ".kt": "Kotlin", ".swift": "Swift", ".c": "C", ".h": "C/C++",
    ".cc": "C++", ".cpp": "C++", ".cs": "C#", ".rb": "Ruby",
    ".php": "PHP", ".sh": "Shell", ".ps1": "PowerShell", ".html": "HTML",
    ".css": "CSS", ".scss": "SCSS", ".vue": "Vue", ".svelte": "Svelte",
    ".md": "Markdown", ".json": "JSON", ".yaml": "YAML", ".yml": "YAML",
}

MANIFEST_NAMES = {
    "package.json", "pyproject.toml", "requirements.txt", "Pipfile",
    "poetry.lock", "uv.lock", "Cargo.toml", "go.mod", "pom.xml",
    "build.gradle", "build.gradle.kts", "Gemfile", "composer.json",
    "Makefile", "justfile", "Dockerfile", "docker-compose.yml",
    "docker-compose.yaml",
}


def git(repo: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return result.stdout.strip() or None
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def relative_files(repo: Path) -> list[Path]:
    files: list[Path] = []
    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(repo)
        if any(part in IGNORED_DIRS for part in relative.parts):
            continue
        files.append(relative)
    return sorted(files, key=lambda item: item.as_posix().casefold())


def is_test(path: Path) -> bool:
    name = path.name.casefold()
    parts = {part.casefold() for part in path.parts}
    return (
        "test" in parts or "tests" in parts or "spec" in parts or "specs" in parts
        or name.startswith("test_") or name.endswith("_test.py")
        or ".test." in name or ".spec." in name
    )


def detect_license(files: list[Path]) -> list[str]:
    return [p.as_posix() for p in files if p.name.casefold().startswith(("license", "copying"))]


def build_snapshot(repo: Path) -> dict:
    repo = repo.resolve()
    if not repo.is_dir():
        raise FileNotFoundError(f"repository path does not exist: {repo}")

    files = relative_files(repo)
    extensions = Counter(path.suffix.casefold() or "[no extension]" for path in files)
    languages = Counter()
    for suffix, count in extensions.items():
        language = LANGUAGES.get(suffix)
        if language:
            languages[language] += count

    manifests = [p.as_posix() for p in files if p.name in MANIFEST_NAMES]
    tests = [p.as_posix() for p in files if is_test(p)]
    docs = [
        p.as_posix() for p in files
        if p.suffix.casefold() in {".md", ".rst", ".adoc"}
        or "docs" in {part.casefold() for part in p.parts}
    ]
    workflows = [
        p.as_posix() for p in files
        if len(p.parts) >= 3 and p.parts[0:2] == (".github", "workflows")
    ]
    skills = [p.as_posix() for p in files if p.name == "SKILL.md"]

    return {
        "schema_version": 1,
        "captured_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repository": {
            "path": str(repo),
            "remote": git(repo, "remote", "get-url", "origin"),
            "commit": git(repo, "rev-parse", "HEAD"),
            "branch": git(repo, "branch", "--show-current"),
            "latest_commit": git(repo, "log", "-1", "--format=%H|%cI|%s"),
            "dirty": bool(git(repo, "status", "--porcelain")),
        },
        "inventory": {
            "file_count": len(files),
            "extensions": dict(extensions.most_common()),
            "languages": dict(languages.most_common()),
            "manifests": manifests,
            "tests": tests,
            "documentation": docs,
            "workflows": workflows,
            "licenses": detect_license(files),
            "skills": skills,
        },
        "signals": {
            "has_tests": bool(tests),
            "has_ci": bool(workflows),
            "has_license": bool(detect_license(files)),
            "has_dependency_manifest": bool(manifests),
            "is_skill_repository": bool(skills),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(build_snapshot(args.repo), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
