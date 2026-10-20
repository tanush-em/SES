from __future__ import annotations

import re
from dataclasses import dataclass, field

NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")
VALID_LANGUAGES = ("python", "typescript", "both")
VALID_RISKS = ("side-project", "commercial")
VALID_SENSITIVE = ("auth", "payments", "pii", "none")


@dataclass
class InitAnswers:
    name: str
    purpose: str
    languages: str  # python | typescript | both
    has_api: bool
    has_ui: bool
    has_db: bool
    risk: str
    sensitive: list[str] = field(default_factory=lambda: ["none"])

    def validate(self) -> None:
        if not NAME_RE.match(self.name):
            raise ValueError(
                f"Invalid product name {self.name!r}; expected slug matching {NAME_RE.pattern}"
            )
        if not self.purpose.strip():
            raise ValueError("Purpose must be a non-empty one-liner")
        if self.languages not in VALID_LANGUAGES:
            raise ValueError(f"languages must be one of {VALID_LANGUAGES}")
        if self.risk not in VALID_RISKS:
            raise ValueError(f"risk must be one of {VALID_RISKS}")
        for item in self.sensitive:
            if item not in VALID_SENSITIVE:
                raise ValueError(f"sensitive value {item!r} not in {VALID_SENSITIVE}")

    @property
    def python_package(self) -> str:
        return self.name.replace("-", "_")

    @property
    def lang_python(self) -> bool:
        return self.languages in ("python", "both")

    @property
    def lang_typescript(self) -> bool:
        return self.languages in ("typescript", "both") or self.has_ui

    @property
    def has_python(self) -> bool:
        return self.lang_python

    @property
    def has_ts_api(self) -> bool:
        return self.has_api and (self.languages in ("typescript", "both"))

    @property
    def has_lib(self) -> bool:
        # Standalone TS surface when no web UI and no TS API package.
        return self.languages in ("typescript", "both") and not self.has_ui and not self.has_ts_api

    def template_context(self) -> dict:
        langs: list[str] = []
        if self.lang_python:
            langs.append("python")
        if self.lang_typescript:
            langs.append("typescript")
        sensitive = list(self.sensitive) if self.sensitive else ["none"]
        return {
            "name": self.name,
            "purpose": self.purpose.strip(),
            "languages": langs,
            "has_api": self.has_api,
            "has_ui": self.has_ui,
            "has_db": self.has_db,
            "risk": self.risk,
            "sensitive": sensitive,
            "python_package": self.python_package,
            "has_python": self.has_python,
            "has_typescript": self.lang_typescript,
            "has_ts_api": self.has_ts_api,
            "has_lib": self.has_lib,
        }

    def modules(self) -> list[str]:
        mods: list[str] = []
        if self.has_python:
            mods.append("python")
        if self.has_lib:
            mods.append("typescript")
        if self.has_api and self.has_python:
            mods.append("api-python")
        if self.has_ts_api:
            mods.append("api-typescript")
        if self.has_ui:
            mods.append("ui")
        if self.has_db:
            mods.append("db-sqlite")
        return mods
