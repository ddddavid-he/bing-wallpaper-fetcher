# bing-wallpaper-fetcher
Automatically download bing wallpaper at a resolution of 4K+

## Requirment
- Python 3
- Python packages: joblib, requests, argparse
- Linux or macOS 
  - It may work on Windows if it is supported to use `wget` `mv` `rm` `cp` in shell
  - `start``stop` scripts only work on Linux and macOS

## usage
- parameters works as what their name idicates
- ***using `--no-cache` option will clean up and rebuild the former `source_list.jbl` file***
