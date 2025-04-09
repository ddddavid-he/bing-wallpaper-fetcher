# Bing壁纸下载工具

<p align="center">
    <a href="README.md">English Documentation</a>
</p>

一个自动下载4K分辨率Bing壁纸的工具。

> **注意：** 由于Bing的限制，部分壁纸可能只有1080p分辨率。

---

## 环境要求
- Python 3
- Python库：`requests`、`argparse`、`pandas`

## 使用方法
- 运行 `python3 main.py`，即可下载壁纸并生成画廊网页。
- 若不需要生成网页，可添加参数 `--no-html` 或 `--image-only`。
- 若只想更新 `source_list.csv` 数据库而不下载图片或生成网页，需同时添加 `--no-image` 和 `--no-html`。
- 使用 `--update` 参数将更新 `source_list.csv` 并备份，不会下载图片或生成网页。
- **警告：** 使用 `--no-cache` 会**删除**并重建 `source_list.csv` 数据库，历史数据将丢失，请谨慎操作！
- `--use-wget` 参数会调用系统的 `wget` 工具下载图片，否则默认使用Python的 `requests` 库。
- `--no-fetch` 参数会阻止更新 `source_list.csv`，仅使用已有的数据库文件。
- 其他参数可根据名称理解用途。
