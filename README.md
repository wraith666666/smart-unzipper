# Bulk ZIP Extractor

> A practical Windows desktop utility to extract multiple ZIP files at once — fast, clean, and no setup required.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows)
![License](https://img.shields.io/badge/License-MIT-green)
![UI](https://img.shields.io/badge/UI-Tkinter-informational)

---

## Why This Exists

Windows has no built-in way to extract dozens of ZIP files at once. Existing tools are either too bloated, require installation, or can't handle edge cases like Google Drive split archives or nested single-root folders.

This utility solves that — point it at a folder, pick your ZIPs, click Extract.

---

## Features

- **Bulk extraction** — select and extract multiple ZIP files in one click
- **Individual mode** — each ZIP extracts into its own named folder
- **Common folder mode** — all ZIPs merge into a single destination folder
- **Smart folder unwrapping** — automatically flattens single-root ZIPs (no extra nesting)
- **Duplicate-safe merging** — conflicting filenames are renamed automatically, never overwritten
- **Google Drive / split archive friendly** — works with chunked ZIP sets
- **Delete after extract** — optionally remove ZIP files once done
- **Threaded extraction** — UI stays responsive during long operations
- **Progress bar** — real-time feedback per file
- **Dark theme UI** — easy on the eyes
- **Standalone EXE** — no Python required on target machine (via PyInstaller)
- **Zero external dependencies** — pure Python standard library

---

## Screenshots

> _Screenshots coming soon — place app screenshots here._

<!-- Replace the lines below with actual images after capturing -->
<!-- ![Main Window](screenshots/main.png) -->
<!-- ![Extraction in Progress](screenshots/extracting.png) -->
<!-- ![Done Dialog](screenshots/done.png) -->

---

## Installation

### Option 1 — Run as Python script

**Requirements:** Python 3.8 or higher (Windows)

```bash
git clone https://github.com/yourusername/bulk-zip-extractor.git
cd bulk-zip-extractor
python unzipper.py
```

No pip installs needed — the app uses only the Python standard library.

### Option 2 — Download the EXE

> _Pre-built releases coming soon._

Download the latest `.exe` from the [Releases](../../releases) page and run it directly. No Python installation required.

---

## Usage

1. Launch the app (`python unzipper.py` or run the EXE)
2. The folder defaults to your current working directory — click **Browse** to change it
3. All ZIP files in the folder are listed with checkboxes (all selected by default)
4. Choose your extraction mode:
   - **Individual Folders** — each ZIP extracts into `ZipName/`
   - **Common Folder** — all ZIPs extract into a single named folder (default: `Combined`)
5. Optionally enable:
   - **Rename duplicate files** — avoids overwriting conflicts
   - **Delete ZIP after extraction** — cleans up source files
6. Click **Extract Selected**
7. A summary dialog reports successes and any failures

---

## Build EXE

To package the app as a standalone Windows executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "BulkZipExtractor" unzipper.py
```

The output EXE will be in the `dist/` folder.

**Optional — add a custom icon:**

```bash
pyinstaller --onefile --windowed --icon=icon.ico --name "BulkZipExtractor" unzipper.py
```

> The `icon.ico` file is already included in the repository.

---

## Tech Stack

| Component  | Technology                     |
|------------|-------------------------------|
| Language   | Python 3.8+                   |
| UI         | Tkinter + ttk (dark theme)    |
| Extraction | Windows built-in `tar` command |
| Threading  | Python `threading` module     |
| Packaging  | PyInstaller                   |

All standard library — no third-party packages required to run.

---

## Project Structure

```
bulk-zip-extractor/
├── unzipper.py          # Main application (single file)
├── icon.ico             # App icon (optional, for EXE builds)
├── requirements.txt     # Empty — no dependencies
├── .gitignore
├── LICENSE
└── README.md
```

---

## Future Improvements

- [ ] Drag-and-drop ZIP file support
- [ ] Recursive folder scan (find ZIPs in subfolders)
- [ ] Password-protected ZIP support
- [ ] `.7z` and `.rar` format support
- [ ] Extraction history / log panel
- [ ] Tray icon / minimize to system tray
- [ ] macOS / Linux compatibility via Python `zipfile` fallback
- [ ] Configurable theme (light / dark toggle)

---

## Release Versioning

This project follows [Semantic Versioning](https://semver.org/):

- `v1.0.0` — Initial stable release
- `v1.x.0` — New features, backwards compatible
- `v1.x.x` — Bug fixes and minor improvements

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## Contributing

This is a small personal utility — contributions and suggestions are welcome via Issues and Pull Requests.
