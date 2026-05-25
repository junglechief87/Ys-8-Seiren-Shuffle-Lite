import shutil
import os
import sys
import fsspec
import shared.config as config

repo = fsspec.filesystem("github", org="junglechief87", repo="Ys-8-Seiren-Shuffle-Lite", sha='master')
folders = ['script/',
           'inc/',
           'text/en/',
           'text/stage/']

def countOriginalGameFiles():
    """Count files to be backed up from the game directory"""
    try:
        count = 0
        for root, dirs, files in os.walk(config.executable_directory):
            # Skip certain directories
            dirs[:] = [d for d in dirs if d not in ['Seiren Shuffle.exe', 'Original Game Files', 'seirenShuffleSettings.json']]
            
            # Don't count the executable or settings file
            for file in files:
                if file not in ['Seiren Shuffle.exe', 'seirenShuffleSettings.json'] and 'Original Game Files' not in root:
                    count += 1
        return count if count > 0 else 500  # Fallback estimate
    except:
        return 500  # Fallback estimate

def countDownloadFiles():
    """Count files to be downloaded from the patch repository"""
    try:
        count = 0
        for folder in folders:
            count += len(repo.ls(folder))
        return count if count > 0 else 337  # Fallback: 334 script + 1 inc + 2 text/en
    except:
        return 337  # Fallback count

def restoreOriginalGameFiles(progress_callback=None):
    def _cp(src, dst):
        shutil.copy2(src, dst)
        if progress_callback:
            progress_callback(f"Restored: {os.path.basename(src)}")
    shutil.copytree(
        os.path.join(config.executable_directory, 'Original Game Files'),
        config.executable_directory,
        dirs_exist_ok=True,
        copy_function=_cp
    )

def copyOriginalGameFiles(progress_callback=None):
    def _cp(src, dst):
        shutil.copy2(src, dst)
        if progress_callback:
            progress_callback(f"Backed up: {os.path.basename(src)}")
    try:
        shutil.copytree(
            src=config.executable_directory,
            dst=os.path.join(config.executable_directory, 'Original Game Files'),
            ignore=shutil.ignore_patterns('Seiren Shuffle.exe', 'Original Game Files', 'seirenShuffleSettings.json'),
            dirs_exist_ok=False,
            copy_function=_cp
        )
    except:
        pass

def downloadFiles(progress_callback=None):
    for folder in folders:
        os.makedirs(os.path.join(config.executable_directory, folder), exist_ok=True)
        
        # Determine encoding based on folder
        encoding = 'shift-jis' if folder in ['script/', 'inc/'] else 'utf-8'
        
        for file in repo.ls(folder):
            dest_path = os.path.join(config.executable_directory, folder, file.split('/')[-1])
            with repo.open(file, 'r', encoding=encoding, errors='surrogateescape') as src:
                with open(dest_path, 'w', encoding=encoding, errors='surrogateescape') as dst:
                    dst.write(src.read())
            if progress_callback:
                progress_callback(f"Downloaded: {file.split('/')[-1]}")


def countChestLocations():
    """Count chest locations from the locations CSV for accurate progress tracking."""
    try:
        from shared.functions import getLocations
        locations = getLocations()
        return sum(1 for loc in locations if loc.item and 'TBOX' in loc.mapCheckID)
    except:
        return 75  # fallback estimate
