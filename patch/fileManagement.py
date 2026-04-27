import shutil
import os
import sys
import fsspec
import shared.config as config

repo = fsspec.filesystem("github", org="junglechief87", repo="Ys-8-Seiren-Shuffle-Lite", sha='master')
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
        
        # Determine encoding based on folder
        encoding = 'shift-jis' if folder in ['script/', 'inc/'] else 'utf-8'
        
        for file in repo.ls(folder):
            with repo.open(file, 'r', encoding=encoding, errors='surrogateescape') as src:
                with open(os.path.join(config.executable_directory, folder, file.split('/')[-1]), 'w', encoding=encoding, errors='surrogateescape') as dst:
                    dst.write(src.read())

def restoreOriginalGameFiles():
    shutil.copytree(os.path.join(config.executable_directory, 'Original Game Files'), config.executable_directory, dirs_exist_ok=True)
