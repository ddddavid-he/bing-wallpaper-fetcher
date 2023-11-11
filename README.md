# bing-wallpaper-fetcher
<p align="center">
    <a href="README_ZH.md"> 中文文档见此 </a>
</p>

Automatically download bing wallpaper at a resolution of 4K+ 

***Some images may have a resolution of 1080p***

## Requirments
- Python 3
- Python packages:  requests, argparse, pandas
- `auto_fetch.sh` `start` and `stop` scripts only work on Linux and macOS

## Usage
- running `python3 fetch.py` does everything
- `HTMLGenerator.py` file creates webpages for the wallpapers, to avoid that, use `--no-html` or `--image-only`
- by using `--no-image` along with  `--no-html`, the script updates `source_list.csv` only   
- `--update` updates the `source_list.csv` files and performs backup without downloading images and generating html files
- ***using `--no-cache` option will DELETEs and rebuilds the `source_list` file. BE CAREFUL WHEN USING THIS OPTION!***
- `--use-wget` option will use wget tool in system instead of Python requests package
- `--no-fetch` option stops it from updating `source_list.csv`. The program will only read existing source_list (if it do).
- other parameters works as what their name indicates
