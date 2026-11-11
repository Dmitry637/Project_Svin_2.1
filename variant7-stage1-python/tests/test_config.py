from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.config import (
    ConfigError,
    load_config,
    render_config,
)
PROJECT = Path(__file__).resolve().parents[1]
class ConfigTests(unittest.TestCase):
    def test_sample_config_loads(self) -> None:
        config = load_config(PROJECT / "config.ini")
        self.assertEqual(
            config.package_name,
            "com.example:demo-app",
        )
        self.assertEqual(config.package_version, "1.0.0")
        self.assertEqual(
            config.resolved_repository_mode,
            "local",
        )
        self.assertIn(
            "package_name=com.example:demo-app",
            render_config(config),
        )
    def test_missing_config(self) -> None:
        with self.assertRaisesRegex(
            ConfigError, "не найден"
        ):
            load_config(PROJECT / "missing.ini")
    def test_invalid_coordinates(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repo.json"
            repo.write_text("{}", encoding="utf-8")
            path = root / "bad.ini"
            path.write_text(
                "[package]\n"
                "name = invalid\n"
                "version = 1.0\n"
                f"[repository]\n"
                f"location = {repo}\n"
                "mode = local\n"
                "[visualization]\n"
                "graph_image = graph.png\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                ConfigError, "groupId:artifactId"
            ):
                load_config(path)
    def test_empty_parameter(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repo.json"
            repo.write_text("{}", encoding="utf-8")
            path = root / "bad.ini"
            path.write_text(
                "[package]\n"
                "name = com.example:app\n"
                "version = \n"
                f"[repository]\n"
                f"location = {repo}\n"
                "mode = local\n"
                "[visualization]\n"
                "graph_image = graph.png\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                ConfigError, "не должен быть пустым"
            ):
                load_config(path)
    def test_missing_repository_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "bad.ini"
            path.write_text(
                "[package]\n"
                "name = com.example:app\n"
                "version = 1.0\n"
                "[repository]\n"
                "location = absent.json\n"
                "mode = local\n"
                "[visualization]\n"
                "graph_image = graph.png\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                ConfigError, "не найден"
            ):
                load_config(path)
    def test_repository_mode_mismatch(self) -> None:
        with self.assertRaisesRegex(
            ConfigError, r"HTTP\(S\)-URL"
        ):
            with tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                repo = root / "repo.json"
                repo.write_text("{}", encoding="utf-8")
                path = root / "bad.ini"
                path.write_text(
                    "[package]\n"
                    "name = com.example:app\n"
                    "version = 1.0\n"
                    f"[repository]\n"
                    f"location = {repo}\n"
                    "mode = remote\n"
                    "[visualization]\n"
                    "graph_image = graph.png\n",
                    encoding="utf-8",
                )
                load_config(path)
if __name__ == "__main__":
    unittest.main()