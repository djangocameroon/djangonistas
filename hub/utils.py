"""Shared helpers for the hub app."""

from __future__ import annotations

import json
from pathlib import Path

from django.conf import settings


def load_json_data(name: str):
    """Return parsed JSON payload from the data directory.

    Raises:
        FileNotFoundError: If the requested file does not exist.
        ValueError: If the JSON payload cannot be decoded.
    """

    data_file = Path(settings.DATA_ROOT) / f"{name}.json"
    with data_file.open(encoding="utf-8") as handle:
        return json.load(handle)
