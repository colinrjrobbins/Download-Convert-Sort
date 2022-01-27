# from modules.FileWatcher import *
import configparser
# from multiprocessing import Pool
import subprocess as sp
# import os

config = configparser.ConfigParser()
config.read('config.cfg')

### REMOVAL
## FileWatcher class creation will be done in seperate processes not in base file.
## Creation of classes in Base file results in only one being called at a time.
## Creation of individual classes was the solution past the limitation of the CPU
## using multiprocessing/multithreading methods.

# convert_watcher = FileWatcher(config['FOLDERS']['convert'])
# torrent_watcher = FileWatcher(config['FOLDERS']['completed_torrents'])
# rename_watcher = FileWatcher(config['FOLDERS']['converted'])
# sort_watcher = FileWatcher(config['FOLDERS']['sort'])

class_folders = [config['FOLDERS']['convert'],
                  config['FOLDERS']['completed_torrents'],
                  config['FOLDERS']['converted'],
                  config['FOLDERS']['sort']]

if __name__ == '__main__':
    try:
        for watcher in class_folders:
            try:
            # attempting OS spawn 
            # os.spawnl(os.P_NOWAIT, "python3 modules/FileWatcher.py " + watcher)
            # RESULT: Single call and stuck on first observer
            
            # attempting subprocess call
            # sp.call(["python3","modules/FileWatcher.py", watcher])
            # RESULT: Single call and stuck on First Observer

            # Attempting: Subprocess Process Creation
                sp.Popen(["python3","modules/FileWatcher.py", watcher])
            # RESULT: Functioning Process call. 
            except Exception as e:
                print("Exception: " + str(e))
    except KeyboardInterrupt:
        sp.call(["pkill", "-f", ".*/FileWatcher.*"]) 