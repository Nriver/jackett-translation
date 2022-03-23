import os

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from settings import PATCH_FOLDER, LANG, TRANS_RELEASE_FOLDER

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


if __name__ == '__main__':

    a = input(f'Delete folder {TRANS_RELEASE_FOLDER}, continue?(y)')
    if a not in ['y', ]:
        exit()

    os.system(f'rm -rf {TRANS_RELEASE_FOLDER}')
    os.makedirs(f'{TRANS_RELEASE_FOLDER}')
    os.chdir(TRANS_RELEASE_FOLDER)
    make_patch()
    os.system(f'xdg-open {TRANS_RELEASE_FOLDER}')
