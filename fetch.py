"""
By Ddddavid 
2022-05-20
"""

import os
import argparse
import requests as re
#import wget
import joblib as jbl
from HTMLGenerator import Generator as HG



data_base = "./source_list.jbl"
img_dir = "./wallpaper/images"
html_dir = "./wallpaper/html"
cache_dir = "./cache"
backup_dir = "./backup"
# re_url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=10"
re_url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=10&nc=1614319565639&pid=hp&FORM=BEHPTB&uhd=1"
url_base = "https://cn.bing.com"
img_prefix = "BW"


def add2Backup(src):
    with open(f'{backup_dir}/{data_base}.bak', 'a+') as file:
        keys = list(src.keys())
        for i in range(len(src[keys[0]])):
            line = ''
            for k in keys:
                line += f'{src[k][i]}\t'
            line = line[:-1]
            file.write(line)


ap = argparse.ArgumentParser(description='Bing Wallpaper Fetcher')
ap.add_argument('--image-only', action='store_true', help='只下载图片')
ap.add_argument('--html-only', action='store_true', help='只生成网页')
ap.add_argument('--keep-cache', action='store_true', help='不删除临时文件')
ap.add_argument('--no-image', action='store_true', help='不下载图片')
ap.add_argument('--no-html', action='store_true', help='不生成网页')
ap.add_argument('--column-number', type=int, default=3, help='网页中一行的图片数')
ap.add_argument('--no-history', action='store_true', help='Caution! Stop loading source list.')
# ap.add_argument('--add-item', type=str, nargs='+', help='手动添加项目（json格式）')
# ap.add_argument('--sort-item', action='store_true', help='对item排序')
# TODO: 添加排序功能

args = ap.parse_args()
if args.image_only and (not args.html_only):
    image_on = True
    html_on = False
elif args.html_only and (not args.image_only):
    html_on = True
    image_on = False
elif (not args.image_only) and (not args.html_only):
    if (not args.no_image) and (not args.no_html):
        image_on = html_on = True
    elif args.no_image and args.no_html:
        image_on = html_on = False
    elif args.no_image:
        html_on = True
        image_on = False
    else:
        html_on = False
        image_on = False
else:
    print("Conflicting parameters. Check again.")
    exit(1)


if os.path.exists(img_dir):
    ...
else:
    os.makedirs(img_dir)
if os.path.exists(html_dir):
    ...
else:
    os.makedirs(html_dir)
if os.path.exists(cache_dir):
    ...
else:
    os.makedirs(cache_dir)
if os.path.exists(backup_dir):
    if os.path.exists(f'{backup_dir}/html'):
        ...
    else:
        os.makedirs(f'{backup_dir}/html')
else:
    os.makedirs(backup_dir)


## read data base
# {
#   'date':[date], 'url':[url],
#   'description':[description], 'title':[title]
# }
# newer one rank higher
if os.path.exists(data_base) and (not args.no_history):
    src = jbl.load(data_base) 
else:
    src = {'date':[], 'url':[], 'description':[], 'title':[]}
for k in src.keys():
    src[k].reverse()
# newer one at behind


## find updates
response = re.get(re_url).json()

img_jss = response['images']



n_dates = [] # [YYYY-MM-DD]
n_urls = [] 
n_descriptions = []
n_titles = []

for img_js in img_jss:
    n_dates.append(img_js['enddate'])
    n_urls.append(f"{url_base}{img_js['urlbase']}_UHD.jpg")
    n_descriptions.append(img_js['copyright'])
    n_titles.append(img_js['title'])

n_dates.reverse()
n_urls.reverse()
n_descriptions.reverse()
n_titles.reverse()


# TODO: Iteration needed to be generalize
for date, url, description, title in zip(
    n_dates, n_urls, n_descriptions, n_titles
):
    if date not in src['date']:
        src['date'].append(date)
        src['url'].append(url)
        src['description'].append(description)
        src['title'].append(title)
    else:
        ...

tmp = src.copy()
for k in src.keys():
    tmp[k].reverse()
    src[k] = []
# newer one at the front


add2Backup(tmp) # backup old src
# prune items older than one year
y_now = int(tmp['date'][0][2:4])
for date, url, description, title in \
    zip(tmp['date'], tmp['url'], tmp['description'], tmp['title']):
    if int(date[2:4]) - y_now <= 1:
        src['date'].append(date)
        src['url'].append(url)
        src['description'].append(description)
        src['title'].append(title)
    else:
        ...

jbl.dump(src, data_base)



## download images
if image_on:
    downloaded_imgs = os.listdir(img_dir)

    for date, url in zip(src['date'], src['url']):
        if f'{img_prefix}-{date[2:]}.jpg' not in downloaded_imgs:
            # wget.download(url, out=f'{cache_dir}/img_cache')
            os.system(f'wget -O {cache_dir}/img_cache {url}')
            """
            TODO: needed to add error detection
            """
            os.system(f'mv {cache_dir}/img_cache  {img_dir}/{img_prefix}-{date[2:]}.jpg')
            print(f'-> {img_prefix}-{date[2:]} downloaded.')
        else:
            ...
else:
    print('-> image downloading skipped')


## generate html files 
if html_on:
    hg = HG(
        src['date'], src['url'], src['title'], src['description'],
        col=args.column_number
    )

    num = hg.generateAll()
    with open(f'{cache_dir}/index.html', 'w') as file:
        file.write(hg.mainpage)
    for key in hg.subpages.keys():
        with open(f'{cache_dir}/page-{key}.html', 'w') as file:
            file.write(hg.subpages[key])
            
    if num > 0:
        # os.system(f'rm -f {backup_dir}/html/*.html')
        os.system(f'mv {html_dir}/*.html {backup_dir}/html/') # BUG: backup don't update
        os.system(f'cp {cache_dir}/index.html {html_dir}/')
        os.system(f'cp {cache_dir}/page-*.html {html_dir}/')
                    

    print(f'->{html_dir}/index.html generated \n->{num} {html_dir}/page-*.html has been generated.')
else:
    print('-> html generation skipped')


if not args.keep_cache:
    os.system(f'rm -f {cache_dir}/img_cache*')
    os.system(f'rm -f {cache_dir}/*.html')
else:
    ...
    

exit(0)
  

