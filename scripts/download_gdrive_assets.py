#!/usr/bin/env python3
"""Download all files from a Google Drive folder via service account (CI only)."""

import io
import json
import os
import sys

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "Photos-3-001")
SKIP_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}


def main() -> None:
    creds_json = os.environ.get("GDRIVE_CREDENTIALS")
    folder_id = os.environ.get("GDRIVE_FOLDER_ID")
    if not creds_json or not folder_id:
        print("ERROR: Set GDRIVE_CREDENTIALS and GDRIVE_FOLDER_ID.", file=sys.stderr)
        sys.exit(1)

    info = json.loads(creds_json)
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    service = build("drive", "v3", credentials=creds, cache_discovery=False)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = []
    page_token = None
    while True:
        response = (
            service.files()
            .list(
                q=f"'{folder_id}' in parents and trashed=false",
                fields="nextPageToken, files(id, name, mimeType)",
                pageToken=page_token,
                pageSize=100,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
            )
            .execute()
        )
        files.extend(response.get("files", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            break

    files = [f for f in files if f["name"] not in SKIP_NAMES]
    if not files:
        print(f"ERROR: No files in Drive folder {folder_id}.", file=sys.stderr)
        sys.exit(1)

    print(f"Downloading {len(files)} file(s) to {OUTPUT_DIR}/")
    for item in files:
        path = os.path.join(OUTPUT_DIR, item["name"])
        print(f"  -> {item['name']}")
        request = service.files().get_media(fileId=item["id"], supportsAllDrives=True)
        with open(path, "wb") as handle:
            downloader = MediaIoBaseDownload(handle, request, chunksize=1024 * 1024)
            done = False
            while not done:
                _, done = downloader.next_chunk()

    print("Google Drive download complete.")


if __name__ == "__main__":
    main()
