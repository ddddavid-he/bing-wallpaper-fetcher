# bing-wallpaper-fetcher
<p align='center'>
    <a href="README.md"> English Document Here </a>
</p>

以4K分辨率下载Bing壁纸的工具

***有些壁纸仅有1080p的分辨率，是Bing网站的限制所致***

## 环境要求
- Python 3
- Python 包： requests、argparse、pandas
- `auto_fetch.sh` `start` and `stop` 三个脚本只适用于  Linux 和 macOS

## 使用方法
- 直接运行命令 `python3 fetch.py` 即可一步完成下载图片、生成html
- `HTMLGenerator.py` 文件提供生成壁纸画廊网页的工具， 如果不需要生成网页文件运行上述命令时添加参数 `--no-html` 或 `--image-only`
- 当使用参数 `--no-image` 和  `--no-html`时，程序只更新`source_list.csv` 文件（保存历史所有图片链接的数据库）   
- `--update` 参数作用同上，只更新 `source_list.csv` 文件
- **如果使用 `--no-cache` 参数 会删除`source_list` 文件并重新生成数据库，会丢失所有超过十天的数据。小心使用**！
- `--use-wget` 使用系统提供的wget程序下载图片，如果没有这个参数程序使用Python的request包进行下载。
- `--no-bakup`阻止程序进行备份步骤，备份文件为 `source_list.csv.bak`
- 其他参数用法可从参数名推测
