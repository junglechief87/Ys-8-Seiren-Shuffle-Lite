import shutil
import os
import sys
import fsspec
import shared.config as config

repo = fsspec.filesystem("github", org="junglechief87", repo="Seiren-Shuffle-An-Ys-8-Randomizer-", sha='main')
folders = ['script/',
           'inc/',
           'text/en/']

def copyOriginalGameFiles():
    try:
        shutil.copytree(src=config.executable_directory, dst=os.path.join(config.executable_directory, 'Original Game Files'), ignore=shutil.ignore_patterns('Seiren Shuffle.exe','Original Game Files','seirenShuffleSettings.json'), dirs_exist_ok=False)
    except:
        """do nothing if the files already exist"""

def downloadFiles():
    for folder in folders:
        os.makedirs(os.path.join(config.executable_directory, folder), exist_ok=True)
        repo.get(repo.ls(folder), os.path.join(config.executable_directory, folder))

def restoreOriginalGameFiles():
    shutil.copytree(os.path.join(config.executable_directory, 'Original Game Files'), config.executable_directory, dirs_exist_ok=True)
