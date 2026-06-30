#!/usr/bin/env python3
"""Generate auth-config.js from SITE_PASSWORD (CI / local dev only)."""

import json
import os
import sys

import bcrypt

OUTPUT = "auth-config.js"


def main() -> None:
    password = os.environ.get("SITE_PASSWORD")
    if not password:
        print("ERROR: Set SITE_PASSWORD environment variable.", file=sys.stderr)
        sys.exit(1)

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")
    payload = json.dumps({"hash": hashed})

    with open(OUTPUT, "w", encoding="utf-8") as handle:
        handle.write("// Auto-generated at deploy time. Do not commit.\n")
        handle.write(f"window.__SITE_AUTH__ = {payload};\n")

    print(f"Wrote {OUTPUT} (bcrypt hash only — plaintext not stored).")


if __name__ == "__main__":
    main()
