# Deploy Eirene Game to GitHub Pages (Google Drive assets)

## Why this setup?

GitHub Pages is **static only** — it cannot run server code or read GitHub Secrets in the browser.

| Approach | Works? |
|----------|--------|
| Put Drive credentials in `index.html` | No — anyone can steal them |
| GitHub Secret read by the live website | No — secrets are only available in Actions |
| **GitHub Actions downloads from Drive at deploy time** | **Yes — recommended** |

Flow:

```
Google Drive (private/shared folder)
        ↓  service account (secret in GitHub Actions)
GitHub Actions build
        ↓
GitHub Pages (HTTPS site with assets baked in)
        ↓
Visitor sees password gate in browser
```

Credentials stay in **GitHub Secrets**. They are used only during the ~2 minute deploy job.

---

## Step 1 — Upload assets to Google Drive

1. Create a folder in Google Drive (e.g. `Eirene-Photos-3-001`).
2. Upload every file from `Photos-3-001/` into that folder (flat list, same filenames).
3. Copy the **folder ID** from the URL:
   ```
   https://drive.google.com/drive/folders/FOLDER_ID_HERE
   ```

---

## Step 2 — Google Cloud service account

1. Open [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project (e.g. `eirene-game`).
3. **APIs & Services → Library** → enable **Google Drive API**.
4. **APIs & Services → Credentials → Create credentials → Service account**.
5. Create the account (e.g. `github-pages-deploy`).
6. Open the service account → **Keys → Add key → Create new key → JSON**.
7. Save the JSON file safely (you will paste it into GitHub once).

Copy the service account email, e.g.:
```
github-pages-deploy@eirene-game.iam.gserviceaccount.com
```

---

## Step 3 — Share the Drive folder with the service account

1. In Google Drive, right-click your assets folder → **Share**.
2. Add the **service account email** as **Viewer**.
3. Uncheck “Notify people” → **Share**.

The service account can now read files; random users cannot without your site password + the deployed URLs.

---

## Step 4 — GitHub repository secrets & variables

Repo: `ilona-asa/cautious-barnacle` → **Settings → Secrets and variables → Actions**

### Secret (required)

| Name | Value |
|------|--------|
| `GDRIVE_SERVICE_ACCOUNT_JSON` | Paste the **entire** JSON key file contents |

### Variable (required)

| Name | Value |
|------|--------|
| `GDRIVE_FOLDER_ID` | The folder ID from Step 1 |

Use a **secret** for the JSON (sensitive). The folder ID can be a **variable** (not secret on its own).

---

## Step 5 — Enable GitHub Pages (Actions source)

1. Repo → **Settings → Pages**
2. **Build and deployment → Source:** `GitHub Actions` (not “Deploy from branch”)
3. Save

---

## Step 6 — Stop tracking local assets in Git

Run once on your Mac (keeps files on disk, removes from Git):

```bash
cd "/Users/asa-sabsono/Documents/side project/eirene_game"
git rm -r --cached Photos-3-001
git add .gitignore .github scripts docs
git commit -m "Deploy Pages via Actions; fetch Photos-3-001 from Google Drive"
git push origin main
```

After push, open **Actions** tab → **Deploy GitHub Pages** → confirm it succeeds.

Your site URL: `https://ilona-asa.github.io/cautious-barnacle/`

---

## Step 7 — Update assets later

1. Add/replace files in the Google Drive folder (keep filenames matching `index.html`).
2. Either push any commit to `main`, or **Actions → Deploy GitHub Pages → Run workflow**.

No need to upload large videos to GitHub again.

---

## Local development

Keep `Photos-3-001/` on your machine for testing. It is gitignored.

```bash
python3 -m http.server 8765
# open http://localhost:8765
```

To test the Drive script locally (optional):

```bash
export GDRIVE_CREDENTIALS="$(cat /path/to/service-account.json)"
export GDRIVE_FOLDER_ID="your-folder-id"
pip install google-api-python-client google-auth
python scripts/download_gdrive_assets.py
```

---

## Security notes

- **GitHub Secret** — never committed; only used in Actions.
- **Password gate** (`AI=AsaIrene`) — casual privacy; password is visible in page source.
- **Deployed media URLs** — anyone who passes the password can still copy direct file URLs from the slideshow. For a birthday gift this is usually acceptable.
- **Private repo** — keeps code off public GitHub; Pages on private repos requires GitHub Pro. Public repo + no assets in Git is a common free compromise.
