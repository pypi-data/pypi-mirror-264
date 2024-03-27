from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest


class CommonTestSetup:
    @pytest.fixture(autouse=True)
    def setup(
        self, pytester: pytest.Pytester, tmp_path: Path, pytestconfig: pytest.Config
    ):
        self.test_dir = pytester
        self.tmp_path = tmp_path
        self.pytestconfig = pytestconfig
        self.json_file = self.tmp_path.joinpath("collect.json")
        self.json_lines_file = self.tmp_path.joinpath("collect.jsonl")

    def read_json_file(self) -> dict[str, Any]:
        return json.loads(self.json_file.read_text())

    def read_json_lines_file(self) -> list[dict[str, Any]]:
        return [
            json.loads(line.strip())
            for line in self.json_lines_file.read_text().splitlines()
            if line.strip()
        ]

    def make_testfile(self, filename: str, content: str) -> None:
        if filename.endswith(".py"):
            filename = filename[:-3]
        else:
            raise ValueError("Filename must end with '.py'")
        kwargs = {filename: content}
        self.test_dir.makepyfile(**kwargs)
