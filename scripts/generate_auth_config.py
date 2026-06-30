#!/usr/bin/env python3
"""Generate auth-config.js from SITE_PASSWORD (CI / local dev only)."""

import hashlib
import json
import os
import secrets
import sys

OUTPUT = "auth-config.js"


def main() -> None:
    password = os.environ.get("SITE_PASSWORD", "").strip()
    if not password:
        print("ERROR: Set SITE_PASSWORD environment variable.", file=sys.stderr)
        sys.exit(1)

    salt = secrets.token_hex(16)
    digest = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    payload = json.dumps({"salt": salt, "digest": digest})

    with open(OUTPUT, "w", encoding="utf-8") as handle:
        handle.write("// Auto-generated at deploy time. Do not commit.\n")
        handle.write(f"window.__SITE_AUTH__ = {payload};\n")

    print(f"Wrote {OUTPUT} (salt + SHA-256 digest only).")


if __name__ == "__main__":
    main()
