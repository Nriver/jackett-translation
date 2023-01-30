import os

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from settings import PATCH_FOLDER, LANG, TRANS_RELEASE_FOLDER, BASE_FOLDER

# disable warning if we use proxy
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

COMPRESS_TOOL = '7z'

COMPRESS_LEVEL = 9


def make_patch():
    # 打zip包
    # make zip
    new_name = f'jackett-{LANG}-patch.zip'
    print('new_name', new_name)
    os.system(f'rm -f {new_name}')
    os.chdir(TRANS_RELEASE_FOLDER)

    if COMPRESS_TOOL == '7z':
        cmd = f'7z a {new_name} -r {PATCH_FOLDER}/*'
    else:
        cmd = f'zip -{COMPRESS_LEVEL} -r {new_name} {PATCH_FOLDER}/*'

    print(cmd)
    os.system(cmd)


def make_release_package():
    # 应用补丁
    # apply patch
    cmd = f'cp -rf {PATCH_FOLDER}* "{BASE_FOLDER}/Jackett/"'
    print('cmd', cmd)
    os.system(cmd)

    # 打zip包
    # make zip
    new_name = f'Jackett-cn.Binaries.Windows.zip'

    if COMPRESS_TOOL == '7z':
        cmd = f'7z a {new_name} -r {BASE_FOLDER}/Jackett/*'
    else:
        cmd = f'zip -{COMPRESS_LEVEL} -r {new_name} {BASE_FOLDER}/Jackett/*'

    print(cmd)
    os.system(cmd)


if __name__ == '__main__':

    if 'GITHUB_ACTIONS' in os.environ:
        print('当前在Github Actions中运行')
    else:
        print('当前在本地电脑上运行')
        a = input(f'Delete folder {TRANS_RELEASE_FOLDER}, continue?(y)')
        if a not in ['y', ]:
            exit()

    os.system(f'rm -rf {TRANS_RELEASE_FOLDER}')
    os.makedirs(f'{TRANS_RELEASE_FOLDER}')
    os.chdir(TRANS_RELEASE_FOLDER)
    make_patch()
    make_release_package()
    if 'GITHUB_ACTIONS' not in os.environ:
        os.system(f'xdg-open {TRANS_RELEASE_FOLDER}')
