from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.config import ConfigError, load_config, render_config

PROJECT = Path(__file__).resolve().parents[1]


class ConfigTests(unittest.TestCase):
    def test_sample_config_loads(self) -> None:
        config = load_config(PROJECT / "config.ini")
        self.assertEqual(config.package_name, "com.example:demo-app")
        self.assertEqual(config.package_version, "1.0.0")
        self.assertEqual(config.resolved_repository_mode, "local")
        self.assertIn("package_name=com.example:demo-app", render_config(config))

    def test_missing_config(self) -> None:
        with self.assertRaisesRegex(ConfigError, "не найден"):
            load_config(PROJECT / "missing.ini")

    def test_invalid_coordinates(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repo.json"
            repo.write_text("{}", encoding="utf-8")
            path = root / "bad.ini"
            path.write_text(
                "[package]\nname = invalid\nversion = 1.0\n"
                f"[repository]\nlocation = {repo}\nmode = local\n"
                "[visualization]\ngraph_image = graph.png\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ConfigError, "groupId:artifactId"):
                load_config(path)

    def test_empty_parameter(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repo.json"
            repo.write_text("{}", encoding="utf-8")
            path = root / "bad.ini"
            path.write_text(
                "[package]\nname = com.example:app\nversion = \n"
                f"[repository]\nlocation = {repo}\nmode = local\n"
                "[visualization]\ngraph_image = graph.png\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ConfigError, "не должен быть пустым"):
                load_config(path)

    def test_missing_repository_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "bad.ini"
            path.write_text(
                "[package]\nname = com.example:app\nversion = 1.0\n"
                "[repository]\nlocation = absent.json\nmode = local\n"
                "[visualization]\ngraph_image = graph.png\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ConfigError, "не найден"):
                load_config(path)

    def test_repository_mode_mismatch(self) -> None:
        with self.assertRaisesRegex(ConfigError, r"HTTP\(S\)-URL"):
            # config.ini points to a local file, but is forced to remote
            with tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                repo = root / "repo.json"
                repo.write_text("{}", encoding="utf-8")
                path = root / "bad.ini"
                path.write_text(
                    "[package]\nname = com.example:app\nversion = 1.0\n"
                    f"[repository]\nlocation = {repo}\nmode = remote\n"
                    "[visualization]\ngraph_image = graph.png\n",
                    encoding="utf-8",
                )
                load_config(path)


if __name__ == "__main__":
    unittest.main()
