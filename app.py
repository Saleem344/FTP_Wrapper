#import libraries
import dotenv
import os,sys
from business.ftp.ftp import FTP_Operations
from business.ftpes.ftpes import FTPes_Operations
from business.sftp.sftp import SFTP_Operations
import time
from infrastructure.utilities.app_logs import logs
from infrastructure.utilities.delete import deletefiles
from pathlib import Path
import schedule
from decouple import config


#append system path
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
os.environ["systempath"] = sys.path[0] + "{}".format("/")
dotenv.set_key(dotenv_file, "systempath", os.environ["systempath"])

#check directory 
Path(os.environ["localfilestopush"]).mkdir(parents=True, exist_ok= True)
Path(os.environ["localfilespushed"]).mkdir(parents=True, exist_ok= True)
Path(os.environ["logfilespath"]).mkdir(parents=True, exist_ok= True)



class mainclass:
    def __init__(self):
            self.logger = logs().file_logs('ftp')
            self.logger.info('FTP program started')
    # pull
    def ftp_pull(self):
        try:
            if os.environ["protocol"] == "ftp":
                FTP_Operations().data_pull()
            elif os.environ["protocol"] == "ftpes":
                FTPes_Operations().data_pull()
            elif os.environ["protocol"] == "sftp":
                SFTP_Operations().data_pull()
            time.sleep(10)
            self.logger.info('FTP app program execution finished')
        except:
            self.logger.error(sys.exc_info()[1])

    def ftp_push(self):
        try:
            if os.environ["protocol"] == "ftp":
                FTP_Operations().data_push()
            elif os.environ["protocol"] == "ftpes":
                FTPes_Operations().data_push()
            elif os.environ["protocol"] == "sftp":
                SFTP_Operations().data_push()
            time.sleep(10)
            self.logger.info('FTP app program execution finished')
        except:
            print(sys.exc_info())
            self.logger.error(sys.exc_info()[1])

    def ftp_delete(self):
        try:
            deletefiles().delete_files()
            time.sleep(10)
            deletefiles().delete_logs()
            time.sleep(10)
        except:
            self.logger.error(sys.exc_info()[1])

# #schedule            
# schedule.every().day.at("10:00").do(mainclass().ftp_delete)
# schedule.every().day.at("10:30").do(deletefiles().delete_logs)

# logger = logs().file_logs('ftp')
# while True:
#     try:
#         if config("ftpoperation") == "push":
#             mainclass().ftp_push()
#         elif config("ftpoperation") == "pull":
#             mainclass().ftp_pull()
#         schedule.run_pending()
#         time.sleep(60)
#     except:
#         logger.error(sys.exc_info())