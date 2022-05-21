# bing-wallpaper-fetcher
Automatically download bing wallpaper at a resolution of 4K+

## Requirment
- Python 3
- Python packages:  requests, argparse, pandas
- `start` and `stop` scripts only work on Linux and macOS

## usage
- run `python3 fetch.py` do everything
- `HTMLGenerator.py` file create webpages for the wallpapers, to avoid that use `--no-html` or `--image-only`
- by using `--no-image` along with  `--no-html`, the script updates `source_list.jbl` only   
- `--update` updates the `source_list.csv` files and perform backup without downloading images and generating html files
- ***using `--no-cache` option will clean up and rebuild the former `source_list` file***
- `--use-wget` option will use wget tool in system instead of Python requests
- `--no-bakup` option stops it from reading and writing `source_list.csv.bak`
- other parameters works as what their name idicates
