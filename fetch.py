"""
By Ddddavid 
2022-05-21
"""

import os
import time
import argparse
import requests as re
import pandas as pd
import FileOperations as fo
from HTMLGenerator import Generator as HG



database = "./source_list.csv"
img_dir = "./wallpaper/images"
subpages_dir = "./wallpaper/subpages"
cache_dir = "./cache"
backup_dir = "./backup"
# re_url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=10"
re_url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=10&nc=1614319565639&pid=hp&FORM=BEHPTB&uhd=1"
url_base = "https://cn.bing.com"
img_prefix = "BW"
MSG_LEN = 50


def stime():
    return time.strftime('%H:%M:%S')


def notify(message):
    print(f'-> ({stime()}) {message}')


def add2Backup(src):
    if os.path.exists(f'{backup_dir}/{database}.bak'):
        bak = pd.read_csv(f'{backup_dir}/{database}.bak', encoding='utf8')
        bak = pd.concat([bak, src], axis=0)
        bak.drop_duplicates(['date'], keep='first', inplace=True)
    else:
        bak = src
    bak.to_csv(f'{backup_dir}/{database}.bak', index=False, encoding='utf8')
    


ap = argparse.ArgumentParser(description='Bing Wallpaper Fetcher')
ap.add_argument('--image-only', action='store_true', help='只下载图片')
ap.add_argument('--html-only', action='store_true', help='只生成网页')
ap.add_argument('--update', action='store_true', help='只更新数据库')
ap.add_argument('--keep-cache', action='store_true', help='不删除临时文件')
ap.add_argument('--no-image', action='store_true', help='不下载图片')
ap.add_argument('--no-html', action='store_true', help='不生成网页')
ap.add_argument('--column-number', type=int, default=3, help='网页中一行的图片数')
ap.add_argument('--no-history', action='store_true', help='Caution! Stop loading source list.')
ap.add_argument('--no-backup', action='store_true', help='不备份数据库')
ap.add_argument('--use-wget', action='store_true', help='使用系统wget下载数据')

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
    
if args.update:
    if (not args.image_only) and (not args.html_only):
        image_on = html_on = False
    else:
        ...
else:
    ...


if os.path.exists(img_dir):
    ...
else:
    os.makedirs(img_dir)
if os.path.exists(subpages_dir):
    ...
else:
    os.makedirs(subpages_dir)
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



print('>' * MSG_LEN)
print('\t', time.ctime())
print('>' * MSG_LEN)


## read data base
# {
#   'date':[date], 'url':[url],
#   'description':[description], 'title':[title]
# }
if os.path.exists(database) and (not args.no_history):
    src = pd.read_csv(database, encoding='utf8')
    src = src[['date', 'title', 'url', 'description']]
else:
    src = pd.DataFrame({'date':[], 'url':[], 'description':[], 'title':[]})
src['date'] = src['date'].apply(lambda x: int(x))



## update database
notify('request to bing.com sent')
response = re.get(re_url).json()
img_jss = response['images']

notify('response from bing.com received')



new_list = {'date':[], 'title':[], 'url':[], 'description':[]}

for img_js in img_jss:
    new_list['date'].append(img_js['enddate'])
    new_list['title'].append(img_js['title'])
    new_list['url'].append(f"{url_base}{img_js['urlbase']}_UHD.jpg")
    new_list['description'].append(img_js['copyright'])
new_list = pd.DataFrame(new_list)
new_list = new_list[['date', 'title', 'url', 'description']]
new_list['date'] = new_list['date'].apply(lambda x: int(x))


for row in range(new_list.shape[0]):
    if new_list['date'][row] in src['date'].unique():
        new_list.drop(row, inplace=True)
# new_list.reset_index(drop=True, inplace=True)
src = pd.concat([src, new_list], axis=0)
# src.reset_index(drop=True, inplace=True)
    
src.sort_values('date', ascending=False, inplace=True, ignore_index=True)
src.reset_index(drop=True, inplace=True)
src['date'] = src['date'].apply(lambda x: str(x))
nc = new_list.shape[0]
notify(f"{nc} new item{'s' if nc>1 else ''} added")
# newer one at the front

if not args.no_backup:
    add2Backup(src) # backup old src
    notify('backup done')
# prune items older than one year
y_now = int(src['date'][0])
oc = 0
for row in range(src['date'].size):
    if int(src['date'][row]) - y_now > 1:
        src.drop(row, inplace=True)
        oc += 1
    else:
        ...
src.reset_index(drop=True, inplace=True)
notify(f"{oc} outdated item{'s' if oc>1 else ''} pruned")
src.to_csv(database, index=False, encoding='utf8')
notify(f"new source list saved, {nc} item{'s' if nc>1 else ''} added")



## download images
if image_on:
    downloaded_imgs = os.listdir(img_dir)
    for date, url in zip(src['date'], src['url']):
        if f'{img_prefix}-{date[2:]}.jpg' not in downloaded_imgs:
            if args.use_wget:
                os.system(f'wget -O {cache_dir}/img_cache {url} > /dev/null')
            else:
                r = re.get(url)
                with open(f'{cache_dir}/img_cache', 'wb') as f:
                    f.write(r.content)
                r.close()
            fo.mv(f'{cache_dir}/img_cache', f'{img_dir}/{img_prefix}-{date[2:]}.jpg')
            notify(f'{img_prefix}-{date[2:]} downloaded')
        else:
            ...
else:
    notify(f'image downloading skipped')


## generate html files 
if html_on:
    hg = HG(
        src['date'], src['url'], src['title'], src['description'],
        col=args.column_number
    )

    num = hg.generateAll()
    with open(f'{cache_dir}/index.html', 'w', encoding='utf8') as f:
        f.write(hg.mainpage)
    for key in hg.subpages.keys():
        with open(f'{cache_dir}/page-{key}.html', 'w', encoding='utf8') as f:
            f.write(hg.subpages[key])
            
    if num > 0:
        fo.rm(f'{backup_dir}/html/*.html')
        fo.mv(f'{subpages_dir}/*.html', f'{backup_dir}/html/')
        fo.mv(f'wallpaper/index.html', f'{backup_dir}/html/')
        fo.cp(f'{cache_dir}/index.html', f'wallpaper/')
        fo.cp(f'{cache_dir}/page-*.html', f'{subpages_dir}/')
        
                    

    notify(f'wallpaper/index.html generated')
    notify(f'{num} {subpages_dir}/page-*.html has been generated')
else:
    notify(f'html generation skipped')


if not args.keep_cache:
    fo.rm(f'{cache_dir}/img_cache')
    fo.rm(f'{cache_dir}/*.html')
else:
    ...

print('<' * MSG_LEN, end='\n\n')

exit(0)
  

