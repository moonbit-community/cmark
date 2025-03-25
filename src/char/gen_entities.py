#!/usr/bin/env python3

import argparse
import json
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input file")
    parser.add_argument("output", help="Output file")
    args = parser.parse_args()

    fin, fout = args.input, args.output

    buf = r"""/// A collection of named entities in HTML,
/// generated from <https://html.spec.whatwg.org/entities.json>.
/// To regenerate, run `moon build`.
let html_named_entities : Json = {
"""

    entities: dict[str, dict[str, str]] = json.loads(Path(fin).read_text())

    for entity, value in entities.items():
        if not entity.endswith(";"):
            continue
        k = entity.removeprefix("&").removesuffix(";")
        # Convert the value to `repr()` (e.g. "中"), then remove the quotes
        v = repr(value["characters"])[1:-1]
        if v == '"':
            v = r"\""
        elif v.startswith(r"\x"):
            v = r"\u{" + v[2:] + "}"
        buf += f'"{k}": "{v}",\n'

    buf += "}\n"
    Path(fout).write_text(buf, encoding="utf-8")
    subprocess.run(["moonfmt", "-w", f"{fout}"])


if __name__ == "__main__":
    main()
