#!/usr/bin/env python3
"""Entry program for make.fun bounty news-image-20261124.

"Sum up 24 November's world news in one image": the repository holds the
finished front-page image at assets/entry.png (drawn beforehand with the
script in design/build_image.py, because this sandbox has no Pillow and
no network). This program verifies the asset and copies it, byte for
byte, to the output directory, so both grading runs produce identical
bytes.

Standard library only; no network.
"""

import os
import struct
import sys
from pathlib import Path

MAX_BYTES = 1_048_576  # 1 MiB gate limit
MAX_DIM = 1024         # gate limit per side, in pixels
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
ASSET = Path(__file__).resolve().parent / "assets" / "entry.png"


def load_asset() -> bytes:
    data = ASSET.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise SystemExit(f"asset {ASSET} is not a PNG file")
    if len(data) > MAX_BYTES:
        raise SystemExit(f"asset is {len(data)} bytes, over the 1 MiB limit")
    # The IHDR chunk follows the 8-byte signature: length(4), "IHDR",
    # then width and height as big-endian uint32.
    if data[12:16] != b"IHDR":
        raise SystemExit("asset PNG has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        raise SystemExit(f"asset is {width}x{height}, over the 1024x1024 limit")
    return data


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    data = load_asset()
    target = out_dir / "entry.png"
    target.write_bytes(data)
    print(f"entry.png: wrote {len(data)} bytes to {target}")


if __name__ == "__main__":
    sys.exit(main())
