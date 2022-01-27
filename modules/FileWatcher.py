from watchdog.observers import Observer
from CustomHandlers import create_handler
import logging
from datetime import datetime
import time
import sys
import subprocess as sp

class FileWatcher():
    def __init__(self, directory_path):
        self.path = directory_path
        self.dateinfo = str.strip(str(datetime.now())," ")[0]

    def watch(self):
        logging.basicConfig(filename="/sharedfolders/convert/scripts/logging/watchdog_log-" + self.dateinfo + ".log",
                                       level=logging.DEBUG)
        
        directory = self.path[1].split("/")
        folder_to_observer = directory[-2]
        
        try:
            self.observer = Observer()
            event_handler = create_handler(folder_to_observer)
            self.observer.schedule(event_handler,
                                   self.path[1],
                                   recursive=True)
            
            print(event_handler)

            try:
                self.observer.start()
                self.observer.join()
                logging.info(folder_to_observer + " Observer has started.")
                while True:
                    time.sleep(10)
            except Exception as e:
                self.observer.stop()
                logging.error("Error Occured During Execution: " + str(e))
                sp.call(["pkill", "-f", ".*/FileWatcher.*"]) 
            
        except Exception as e:
            logging.error("Error Occured In Creation: " + str(e))
            self.observer.stop()

## REQUIRED ##
# Creation of subprocess FileWatcher calls pulling the individual folders to
# watch from console calls    
if __name__ == "__main__":
    observering = FileWatcher(sys.argv)
    observering.watch()