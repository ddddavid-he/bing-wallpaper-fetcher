# bing-wallpaper-fetcher
Automatically download bing wallpaper at a resolution of 4K+

## Requirment
- Python 3
- Python packages: joblib, requests, argparse
- Linux or macOS 
  - It may work on Windows if it is supported to use `wget` `mv` `rm` `cp` in shell
  - `start` and `stop` scripts only work on Linux and macOS

## usage
- run `python3 fetch.py` do everything
- `HTMLGenerator.py` file create webpages for the wallpapers, to avoid that use `--no-html` or `--image-only`
- by using `--no-image` along with  `--no-html`, the script updates `source_list.jbl` only   
- parameters works as what their name idicates
- ***using `--no-cache` option will clean up and rebuild the former `source_list.jbl` file***
