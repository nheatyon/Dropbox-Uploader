# Dropbox Uploader

Command-line helper that sends a local file to Dropbox and stamps the remote name with the current date and time. The first run walks through Dropbox app authorization and stores a refresh token in a local `.login` file so later uploads do not ask again.

## Features

- One-argument upload: `python3 uploader.py <file_to_upload>`
- Dropbox OAuth 2 with PKCE and offline refresh tokens
- App key, app secret, and refresh token are prompted, never hard-coded
- Remote path includes `YYYY-MM-DD-HH:MM:SS`

## Requirements

- Python 3.9+
- A Dropbox app with scoped access (files.content.write)
- The packages in `requirements.txt`

## How to use

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 uploader.py <file_to_upload>
```

Arguments:

| Argument | Meaning |
| --- | --- |
| `<file_to_upload>` | Path of the local file to send to Dropbox |

On the first run the script asks for:

1. **App Key** and **App Secret** from the Dropbox App Console
2. A visit to the printed authorization URL
3. The one-time authorization code

Those values are written to `.login` in the working directory. Keep that file private; it is ignored by git.

Later runs reuse `.login` and upload the file into the app folder as:

```
/<original-name>-<date>-<time>.<extension>
```

Example:

```text
notes-2026-10-28-21:15:03.txt
```

## License

GNU General Public License v3.0. See [LICENSE](LICENSE).
