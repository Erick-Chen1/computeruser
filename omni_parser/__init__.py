"""Wrapper for invoking the standalone OmniParser project.

This module defines a single :func:`parse` function which shells out to an
external OmniParser CLI.  Users should clone the official repository
(https://github.com/microsoft/OmniParser) and set the environment variable
``OMNIPARSER_CMD`` to the command that runs the parser.  The command should
accept the screenshot path as its final argument and output JSON describing
UI elements to stdout.

The function returns a list of node dictionaries or an empty list if anything
fails.
"""
from __future__ import annotations

import json
import os
import shlex
import subprocess
from typing import Any, Dict, List


def parse(image_path: str) -> List[Dict[str, Any]]:
    """Parse ``image_path`` using OmniParser.

    The parser command is taken from ``OMNIPARSER_CMD`` environment variable.
    It must output either a JSON list of nodes or a dictionary containing an
    ``elements`` list.  Each node should be a mapping with at least ``bbox`` and
    ``text`` fields.  Any failure results in an empty list.
    """

    cmd = os.environ.get("OMNIPARSER_CMD")
    if not cmd:
        return []

    args = shlex.split(cmd) + [image_path]
    try:
        proc = subprocess.run(args, capture_output=True, text=True, check=True)
    except Exception:
        return []

    try:
        data = json.loads(proc.stdout)
    except Exception:
        return []

    if isinstance(data, dict):
        items = data.get("elements", [])
    elif isinstance(data, list):
        items = data
    else:
        items = []

    result: List[Dict[str, Any]] = []
    for node in items:
        if isinstance(node, dict):
            result.append(node)
    return result
