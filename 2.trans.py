import os
import platform
import re
import shutil

from loguru import logger

from settings import BASE_FOLDER, PATCH_FOLDER, TRANSLATOR, TRANSLATOR_URL, LANG
from translations import translation_dict

script_path = os.path.dirname(os.path.abspath(__file__))

BASE_PATH = f'{BASE_FOLDER}Jackett-src/'
os.chdir(BASE_PATH)

TRANSLATOR_LABEL = translation_dict['translator']

# 用 [[]] 来标记要翻译的内容
# use [[]] to mark the content you want to translate

pat = re.compile('\[\[(.*?)\]\]', flags=re.DOTALL + re.MULTILINE)

missing_files = []


def translate(m):
    # logger.info(f'{m}')
    trans = translation_dict.get(m.group(1), m.group(1))
    if not trans:
        trans = m.group(1)
    return trans


def replace_in_file(file_path, translation, base_path=BASE_PATH):
    file_full_path = os.path.join(base_path, file_path)
    if not os.path.exists(file_full_path):
        missing_files.append(file_full_path)
        return

    with open(file_full_path, 'r') as f:
        content = f.read()

    for ori_mark in translation:
        ori_content = ori_mark.replace('[[', '').replace(']]', '')

        trans = pat.sub(translate, ori_mark)

        # logger.info(f"{'ori_content', ori_content}")
        # logger.info(f"{'trans', trans}")

        content = content.replace(ori_content, trans)

    with open(file_full_path, 'w') as f:
        f.write(content)


# TODO: 关于页面添加翻译者信息
# add translator info in about page :)
logger.info(f"{'add translator info in about page.'}")
translator_info = f'{TRANSLATOR} {TRANSLATOR_URL} {LANG}'

modded_file_list = []

# 下面一堆是正则匹配规则, 读代码的时候下面这一段可以跳过, 直接看最后面几行
# TL;DR, the following codes are regex matches, you can jump to the last few lines.

file_path = 'src/Jackett.Common/Content/custom.js'
translation = [
    '>[[Show all]]<',
    '>[[Click here to open an issue on GitHub for this indexer.]]<',
    '>[[NO UPLOAD]]<',
    '>[[ Show dead torrents]]<',
    '[[Search query consists of several keywords.\\nKeyword starting with \\"-\\" is considered a negative match.]]',
    'doNotify("[[Error loading Jackett settings, request to Jackett server failed, is server running ?]]",',
    'doNotify("[[Error loading indexers, request to Jackett server failed, is server running ?]]",',
    'doNotify("[[Adding selected Indexers, please wait...]]",',
    'doNotify("[[Error: You must select more than one indexer]]",',
    'doNotify("[[Selected indexers successfully added.]]",',
    'doNotify("[[Configuration failed]]",',
    'doNotify("[[An error occurred while configuring this indexer, is Jackett server running ?]]",',
    'doNotify("[[Copied to clipboard!]]",',
    'doNotify("[[Error deleting indexer, request to Jackett server error]]",',
    'doNotify("[[An error occurred while testing indexers, please take a look at indexers with failed test for more informations.]]",',
    'doNotify("[[Request to Jackett server failed]]",',
    'doNotify("[[An error occurred while updating this indexer, request to Jackett server failed, is server running ?]]",',
    'doNotify("[[Downloaded sent to the blackhole successfully.]]",',
    'doNotify("[[Redirecting you to complete configuration update..]]",',
    'doNotify("[[Updater triggered see log for details..]]",',
    'doNotify("[[Admin password has been set.]]",',
    # 表格显示条数
    ', "[[All]]"]',
    "nonSelectedText: '[[All]]'",
]
replace_in_file(file_path, translation)
modded_file_list.append(file_path)

file_path = 'src/Jackett.Common/Content/index.html'
translation = [
    '>[[API Key: ]]<',
    '>[[Standalone version of Jackett is now available - Mono not required]]<',
    '[[To upgrade to the standalone version of Jackett, <a href="https://github.com/Jackett/Jackett#install-on-linux-amdx64" target="_blank" class="alert-link">click here</a> for install instructions.\n            Upgrading is straight forward, simply install the standalone version and your indexers/configuration will carry over.\n            Benefits include: increased performance, improved stability and no dependency on Mono.]]',
    '>[[Configured Indexers]]<',
    '>[[Adding a Jackett indexer in Sonarr or Radarr]]<',
    '>[[Go to ]]<',
    '>[[Settings > Indexers > Add > Torznab > Custom]]<',
    '>[[Click on the indexers corresponding <button type="button" class="btn btn-xs btn-info">Copy Torznab Feed</button> button and paste it into the Sonarr/Radarr <b>URL</b> field.]]<',
    '[[Click on an URL to copy it to the Site Link field.]]',
    '>[[For the <b>API key</b> use <b class="api-key-text"></b>.]]<',
    '>[[Configure the correct category IDs via the <b>(Anime) Categories</b> options. See the Jackett indexer configuration for a list of supported categories.]]<',
    '>[[Adding a Jackett indexer in CouchPotato]]<',
    '>[[Settings > Searchers]]<',
    '>[[Enable ]]<',
    '>[[Click on the indexers corresponding <button type="button" class="btn btn-xs btn-info">Copy Potato Feed</button> button and paste it into the CouchPotato <b>host</b> field.]]<',
    '>[[Click on the indexers corresponding <button type="button" class="btn btn-xs btn-info">Copy RSS Feed</button> button and paste it into the URL field of the RSS client.]]<',
    '>[[For the <b>Passkey</b> use <b class="api-key-text"></b>. Leave the <b>username</b> field blank.]]<',
    '>[[Adding a Jackett indexer to RSS clients (RSS feed)]]<',
    '>[[Click on the indexers corresponding <button type="button" class="btn btn-xs btn-info">Copy RSS Feed</button> button and paste it into the URL field of the RSS client.]]<',
    '[[You can adjust the <b>q</b> (search string) and <b>cat</b> (categories) arguments accordingly.\n                    E.g. <b>...&cat=2030,2040&q=big+buck+bunny</b> will search for "big buck bunny" in the Movies/SD (2030) and Movies/HD (2040) categories (See the indexer configuration for available categories).]]',
    '>[[Jackett Configuration]]<',
    '>[[   Apply server settings ]]<',
    '>[[ View logs ]]<',
    '>[[   Check for updates ]]<',
    '>[[Admin password: ]]<',
    '>[[  Set Password ]]<',
    '>[[Base path override: ]]<',
    '>[[Server port: ]]<',
    '>[[Blackhole directory: ]]<',
    '>[[Proxy type: ]]<',
    '>[[Disabled]]<',
    '>[[Proxy URL: ]]<',
    '>[[Proxy port: ]]<',
    '>[[Proxy username: ]]<',
    '>[[Proxy password: ]]<',
    '>[[External access: ]]<',
    '>[[Disable auto update: ]]<',
    '>[[Update to pre-release: ]]<',
    '>[[Enhanced logging: ]]<',
    '>[[Cache enabled (recommended): ]]<',
    '>[[Cache TTL (seconds): ]]<',
    '>[[Cache max results per indexer: ]]<',
    '>[[FlareSolverr API URL: ]]<',
    '>[[FlareSolverr Max Timeout (ms): ]]<',
    '>[[OMDB API key: ]]<',
    '>[[OMDB API Url: ]]<',
    '>[[ Version ]]<',
    '>[[Indexer]]<',
    '>[[Actions]]<',
    '>[[Categories]]<',
    '>[[Type]]<',
    '>[[Type string]]<',
    '>[[Language]]<',
    '>[[Cached Releases]]<',
    '>[[This screen shows releases which have been recently returned from Jackett. Only the last 300 releases for each tracker are returned.]]<',
    '>[[Published]]<',
    '>[[First Seen]]<',
    '>[[Tracker]]<',
    '>[[Name]]<',
    '>[[Size]]<',
    '>[[Files]]<',
    '>[[Category]]<',
    '>[[Grabs]]<',
    '>[[Seeds]]<',
    '>[[Leechers]]<',
    '>[[DL Factor]]<',
    '>[[UL Factor]]<',
    '>[[Download]]<',
    '>[[Close]]<',
    '>[[Manual search]]<',
    '>[[You can search all configured indexers from this screen.]]<',
    '>[[Query]]<',
    '>[[Filter]]<',
    '>[[all]]<',
    '>[[Error]]<',
    '>[[Select an indexer to setup]]<',
    '>[[Add Selected]]<',
    '>[[Server Logs]]<',
    '>[[Date]]<',
    '>[[Level]]<',
    '>[[Message]]<',
    '>[[Okay]]<',
    '>[[Capabilities]]<',
    '>[[Description]]<',
    '>[[Filter ]]<',
    '>[[All]]<',
    'title="[[Jackett on GitHub]]"',
    'title="[[Search]]"',
    'title="[[Configure]]"',
    'title="[[Delete]]"',
    'title="[[Add]]"',
    'title="[[Download locally]]"',
    'title="[[Download locally (magnet)]]"',
    'title="[[Save to server blackhole directory]]"',
    'placeholder="[[Blank to disable]]"',
    # 以下为不规则内容
    '> [[Add indexer]]',
    '> [[Manual Search]]',
    '>  [[View cached releases]]',
    '> [[Test All]]',
    '>[[Copy RSS Feed]]<',
    '>[[Copy Torznab Feed]]<',
    '>[[Copy Potato Feed]]<',
    '        [[Test]]',
    '"[[Blank for default]]"',
]
replace_in_file(file_path, translation)
modded_file_list.append(file_path)

file_path = 'src/Jackett.Common/Content/libs/bootstrap-notify.js'
translation = [
    '>[[{1}]]<',
    '>[[{2}]]<',
]
replace_in_file(file_path, translation)
modded_file_list.append(file_path)

file_path = 'src/Jackett.Common/Content/login.html'
translation = [
    '>[[Jackett]]<',
    '>[[Login]]<',
    '>[[Admin password]]<',
]
replace_in_file(file_path, translation)
modded_file_list.append(file_path)

file_path = 'src/Jackett.Common/Content/libs/jquery.dataTables.min.js'
translation = [
    'sSortAscending:": [[activate to sort column ascending]]",',
    'sSortDescending:": [[activate to sort column descending]]"',
    'sFirst:"[[First]]",',
    'sLast:"[[Last]]"',
    'sNext:"[[Next]]",',
    'sPrevious:"[[Previous]]"',
    'sEmptyTable:"[[No data available in table]]",',
    'sInfo:"[[Showing _START_ to _END_ of _TOTAL_ entries]]"',
    'sInfoEmpty:"[[Showing 0 to 0 of 0 entries]]",',
    'sInfoFiltered:"[[(filtered from _MAX_ total entries)]]"',
    'sLengthMenu:"[[Show _MENU_ entries]]",',
    'sLoadingRecords:"[[Loading...]]",',
    'sProcessing:"[[Processing...]]"',
    'sSearch:"[[Search:]]",',
    'sZeroRecords:"[[No matching records found]]"',
]
replace_in_file(file_path, translation)
modded_file_list.append(file_path)

# 创建补丁文件, 可以直接用在其它release里
# make patch files, which can be used by other platform release
if os.path.exists(PATCH_FOLDER):
    shutil.rmtree(PATCH_FOLDER)
os.mkdir(PATCH_FOLDER)

for file_path in modded_file_list:
    src = BASE_PATH + file_path
    dst = PATCH_FOLDER + file_path
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy(src, dst)
# 把文件夹移出来
shutil.move(PATCH_FOLDER + 'src/Jackett.Common/Content', PATCH_FOLDER)
shutil.rmtree(PATCH_FOLDER + 'src')

if missing_files:
    logger.info(f"{'missing_files!'}")
    for x in missing_files:
        logger.info(f'{x}')

logger.info(f"{'finished!'}")

if platform.system() == 'Linux':
    os.system(f'xdg-open {PATCH_FOLDER}')
