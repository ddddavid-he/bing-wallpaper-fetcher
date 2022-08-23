# bing-wallpaper-fetcher
Automatically download bing wallpaper at a resolution of 4K+

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
- `--use-wget` option will use wget tool in system instead of Python requests
- `--no-bakup` option stops it from reading and writing `source_list.csv.bak`
- other parameters works as what their name idicates
