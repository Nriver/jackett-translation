# 更新各个渠道的release文件
import hashlib
import json
import os

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from settings import PROXIES

# disable warning if we use proxy
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 注意这里的版本号开头没有v!
with open('VERSION') as f:
    version = f.read().strip()

# if not input(f'{version} 请确认版本号正确！！！ (y)').lower() in ['y', 'yes']:
#     exit()

# 计算hash
release_url_windows = f'https://github.com/Nriver/jackett-translation/releases/download/v{version}/Jackett-cn.Binaries.Windows.zip'

# windows 客户端
scoop_folder = f'/home/nate/gitRepo/Scoop-Nriver'


def get_sha256(file_path):
    with open(file_path, 'rb') as f:
        return (hashlib.sha256(f.read()).hexdigest())


def download_file(url, file_name):
    tmp_folder = 'tmp/'
    if not os.path.exists(tmp_folder):
        os.mkdir(tmp_folder)
    download_path = os.path.join(tmp_folder, file_name)
    with requests.get(url, proxies=PROXIES, verify=False, stream=True) as r:
        r.raise_for_status()
        with open(download_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    return download_path


print('下载release文件...')
release_fp_windows = download_file(release_url_windows, 'Jackett-cn.Binaries.Windows.zip')

# scoop
# windows 客户端
scoop_fp = f'{scoop_folder}/bucket/jackett-cn.json'
with open(scoop_fp, 'r', encoding='utf-8') as f:
    c = json.loads(f.read())
    c['version'] = version
    c['architecture']['64bit'][
        'url'] = release_url_windows
    c['architecture']['64bit']['hash'] = get_sha256(release_fp_windows)

    new_c = json.dumps(c, ensure_ascii=False, indent=4)

print(scoop_fp)
with open(scoop_fp, 'w', encoding='utf-8') as f:
    f.write(new_c)

print('=====')
print('请注意提交以下文件')
print(scoop_folder)
