import os
import re
from zipfile import ZipFile

import requests
from loguru import logger
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from settings import BASE_FOLDER, USE_PROXY, PROXIES

# disable warning if we use proxy
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

CLIENT_FOLDER = BASE_FOLDER + 'Jackett'
REPO_NAME = 'Jackett/Jackett'
# regex match which file to download if multiple files exists
PREFERRED_RELEASE_NAME_PATTERN = 'Jackett.Binaries.Windows.zip'
SOURCE_CODE_NAME_PATTERN = 'Jackett-linux-x64-.*?.tar.xz'

CMD_STOP_SERVICE = """pkill -9 Jackett"""

# 是否从GitHub下载文件
# whether download files from GitHub
DO_DOWNLOAD = True

# 是否删除临时文件
# whether delete template files
# DO_DELETE = False
DO_DELETE = True


def requests_get(url):
    ret = None
    try:
        ret = requests.get(url, proxies=PROXIES, verify=not USE_PROXY)
    except Exception as e:
        logger.info(f"{'If github is not available, you can set USE_PROXY to True and set PROXIES to your proxy.'}")
        logger.info(f"{'Exception', e}")
    return ret


def get_latest_version():
    """get latest version info"""
    logger.info(f"{'get latest version info'}")
    url = f'https://api.github.com/repos/{REPO_NAME}/releases/latest'
    logger.info(f'{url}')
    res = requests_get(url)
    version_info = {}

    # zipball_url is the source code
    version_info['zipball_url'] = res.json()['zipball_url']

    version_info['name'] = res.json()['name']
    for x in res.json()['assets']:
        logger.info(f"{x['name']}")
        if not re.match(PREFERRED_RELEASE_NAME_PATTERN, x['name']):
            continue
        version_info['browser_download_url'] = x['browser_download_url']
        break
    if 'browser_download_url' not in version_info:
        logger.info(
            f"{'Did not find a matching release! Please check file name and modify PREFERRED_RELEASE_NAME_PATTERN.'}")
        exit()
    logger.info(f'latest version is {version_info["name"]}')
    return version_info


def download_source(url, file_name=None):
    logger.info(f"{'download source', url}")
    if not file_name:
        file_name = url.split('/')[-1]
    logger.info(f"{'downloading ...'}")
    if DO_DOWNLOAD:
        with requests.get(url, proxies=PROXIES, verify=False, stream=True) as r:
            r.raise_for_status()
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    logger.info(f'download complete, file saved as {file_name}')
    return file_name


def decompress_source_package(file_name):
    if file_name.endswith('.zip'):
        with ZipFile(file_name, 'r') as zip_file:
            # printing all the contents of the zip file
            extracted_folder = zip_file.namelist()[0].split('/')[0]
        if extracted_folder:
            os.system(f'unzip -o {file_name}')
            os.system('pwd')
            if DO_DELETE:
                os.system(f'rm -rf Jackett-src.zip')
            logger.info(f'{extracted_folder}')
            os.system(f'mv {extracted_folder} Jackett-src')


if __name__ == '__main__':
    if os.path.exists(BASE_FOLDER):
        if not (input(f'BASE_FOLDER exists! DELETE {BASE_FOLDER}, continue?(y)')).lower() in ['y', 'yes']:
            exit()
        os.system(f'rm -rf {BASE_FOLDER}')
    os.makedirs(BASE_FOLDER)
    logger.info(f"{'BASE_FOLDER', BASE_FOLDER}")
    os.chdir(BASE_FOLDER)

    version_info = get_latest_version()

    logger.info(f'{version_info}')

    # 下载源码
    # get source code
    file_name = download_source(version_info['zipball_url'], 'Jackett-src.zip')
    logger.info(f'file_name {file_name}')
    decompress_source_package(file_name)

    logger.info(f"{'finished!'}")
