from __future__ import annotations

import argparse
import sys

from src.config import ConfigError, load_config, render_config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Вариант №7, этап 1: чтение INI-конфигурации, "
            "проверка параметров и вывод ключ=значение."
        )
    )
    parser.add_argument(
        "--config",
        default="config.ini",
        metavar="FILE",
        help="путь к INI-файлу (по умолчанию: config.ini)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        config = load_config(args.config)
    except ConfigError as exc:
        print(f"Ошибка конфигурации: {exc}", file=sys.stderr)
        return 2

    print(render_config(config))
    print("\nКонфигурация проверена успешно.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
