# Bing Wallpaper Fetcher

<p align="center">
    <a href="README_ZH.md">中文文档</a>
</p>

A tool to automatically download Bing wallpapers in 4K+ resolution.

> **Note:** Some images may only be available in 1080p due to Bing's limitations.

---

## Requirements
- Python 3
- Python packages: `requests`, `argparse`, `pandas`

## Usage
- Run `python3 main.py` to download images and generate the HTML gallery.
- To skip HTML generation, add `--no-html` or `--image-only`.
- To only update the `source_list.csv` database without downloading images or generating HTML, use both `--no-image` and `--no-html`.
- The `--update` option updates `source_list.csv` and creates a backup without downloading images or generating HTML.
- **Warning:** Using `--no-cache` will **delete** and rebuild the `source_list.csv` database, resulting in loss of history. Use with caution!
- The `--use-wget` option uses the system's `wget` tool instead of Python's `requests` package for downloading.
- The `--no-fetch` option prevents updating `source_list.csv` and uses the existing file.
- Other parameters are self-explanatory based on their names.
