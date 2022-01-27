from calendar import c
from watchdog.events import FileSystemEventHandler
from ConvertMedia import executeConversion
import shutil
import os
import time
import configparser
import re
import subprocess as sp

# create abstract handler class to create subsequent handlers required 
# based on directory handed in to the class.
def create_handler(directory):
    try:
        if directory == "toConvert":
            return ConvertHandler()
        elif directory == "Converted":
            return RenameHandler()
        elif directory == "completed":
            return TorrentHandler()
        elif directory == "Newly Added":
            return SortHandler()
        else:
            raise
    except Exception:
        print ("No handler found for specific directory.")
        pass

def get_config():
    config = configparser.ConfigParser()
    config.read('/sharedfolders/convert/scripts/config.cfg')
    return config   

# moves files from Completed torrent folder to either toConvert folder
# or moves directly to Converted folder for renaming and then sorting.
class TorrentHandler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        config = get_config()
        if event.is_directory:
            return None
        elif event.event_type == "created":
            print("file added to completed torrents, waiting for copy...")
            time.sleep(10)
            fileNamePath = str(event.src_path)
            # EX. /sharedfolders/convert/Torrents/completed/The.Book.of.Boba.Fett.S01E03.mkv
            print("filename copying: "+ fileNamePath)
            fileName = fileNamePath.split("/")[-1]
            fileNameExt = fileNamePath[-4:]

            if fileNameExt == ".mp4":
                shutil.move(fileNamePath, config['FOLDERS']['converted']+fileName)
                print("moved mp4 to converted folder for rename.")
            elif fileNameExt == ".mkv" or fileNameExt == ".avi":
                shutil.move(fileNamePath, config['FOLDERS']['convert']+fileName)
                print("moved other toConvert folder for conversion.")
            else:
                pass
                print("passing on other documents.")
        else:
            pass

# deals with the files located in the toConvert folder and converts them
# as neccessary
class ConvertHandler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        valueCheck = ["!","@","#","$","%","^","&","*","(",")","=","+","<",">","?","[","]","{","}",";",":","'"," "]
        if event.is_directory:
            return None
        elif event.event_type == "created":
            config = get_config()
            # take any action here when a file is first created.
            print("Running Conversion.")
            file_path = str(event.src_path)
            if config['FOLDERS']['convert'] in file_path:
                file_name = file_path.split("/")[-1]
                filename3 = file_name[:-4]
                for check in valueCheck:
                    filename3 = filename3.replace(check,"")
                print(file_name.split("."))
                if file_name.split(".")[-1] == "mp4":
                    print(file_name.split(".")[-1])
                    os.rename(file_path,config['FOLDERS']['converted']+file_name)
                else:
                    for check in valueCheck:
                        file_name = file_name.replace(check,"")
                    os.rename(file_path,config['FOLDERS']['convert']+file_name)
                    print(file_name.split(".")[-1])
                    print("File Name 1: " + file_path)
                    print("File Name 2: " + file_name)
                    print("File Name 3: " + filename3)
                    print("Final File Name: " + filename3)
                    executeConversion(file_name, filename3, config['FOLDERS']['convert'], config['FOLDERS']['converting'], config['FOLDERS']['converted'])

# uses filebot to rename the files based on if they are a movie or TV show.
# (Done in converted folder)
class RenameHandler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == "created":
            config = get_config()
            file_path = str(event.src_path)
            if config['FOLDERS']['converted'] in file_path:
                print("filepath: "+file_path)
                file_name = file_path.split("/")[-1]
                time.sleep(5)

                # Determine if Movie or TV Show
                tv_pattern = r'S\w\wE\w\w'
                result = re.search(tv_pattern, file_name.upper())

                if result != None:
                    sp.call(['filebot','-rename',
                             config['FOLDERS']['converted']+file_name,
                             '--format',
                             '"{n} {S00E00} - {t}"',
                             '--db', 
                             'TheTVDB', 
                             '-non-strict'])
                    # run TV show setup
                else:
                    sp.call(['filebot',
                             '-rename',
                             config['FOLDERS']['converted']+file_name,
                             '--format',
                             '"{n} ({y})"', 
                             '--db', 
                             'TheMovieDB', 
                             '-non-strict'])
                    # run Movie setup

                time.sleep(2)

                file_name = os.listdir(config['FOLDERS']['converted'])[0]
                print("wo path: "+ file_name)
                shutil.copy(config['FOLDERS']['converted']+file_name, config['FOLDERS']['sort']+file_name)
                os.remove(config['FOLDERS']['converted']+file_name)

# sorts files moved into the Newly Added directory accordingly.
class SortHandler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == "created":
            time.sleep(5)
            config = get_config()
            file_path = str(event.src_path)
            if config['FOLDERS']['sort'] in file_path:
                file_name = file_path.split("/")[-1]

                tv_pattern = r'S\w\wE\w\w'
                result = re.search(tv_pattern, file_name.upper())

                if result != None:
                    show_name = file_name.split(result.group(0))[0]
                    show_name = show_name[0:len(show_name)-1]
                    tv_shows = os.listdir(config['FOLDERS']['tvshows'])
                    if show_name in tv_shows:
                        show_season = result.group(0).split('E')[0].replace('S','')
                        if show_season[0] == '0':
                            show_season = show_season.replace('0','')
                        else:
                            pass
                        seasons_listed = os.listdir(config['FOLDERS']['tvshows']+show_name+'/')
                        if ('Season ' + show_season) in seasons_listed:
                            shutil.move(file_path,config['FOLDERS']['tvshows']+show_name+'/Season '+show_season+'/')
                        else:
                            os.mkdir(config['FOLDERS']['tvshows']+show_name+'/Season '+show_season+'/')
                            shutil.move(file_path,config['FOLDERS']['tvshows']+show_name+'/Season '+show_season+'/')
                    else:
                        os.mkdir(config['FOLDERS']['tvshows']+show_name)
                        show_season = result.group(0).split('E')[0].replace('S','')
                        if show_season[0] == '0':
                            show_season = show_season.replace('0','')
                        else:
                            pass
                        os.mkdir(config['FOLDERS']['tvshows']+show_name+'/Season '+show_season+'/')
                        shutil.move(file_path,config['FOLDERS']['tvshows']+show_name+'/Season '+show_season+'/')
                else:
                    shutil.move(file_path, config['FOLDERS']['movies'])


