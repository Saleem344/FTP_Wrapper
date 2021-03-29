#import library
from decouple import config
import os,sys
sys.path.append(config("systempath"))
from datetime import datetime, timedelta
from infrastructure.utilities.credential import ftpinfo
from infrastructure.utilities.app_logs import logs


class deletefiles:
    def __init__(self):
        self.logger = logs().file_logs('ftp')
    # delete backup files

    def delete_files(self):
        # local path
        credential = ftpinfo().ftp_Push()
        directorypath = credential['ftp_pushed']
        availablefiles = os.listdir(directorypath)
        referencefiledatatime = int((datetime.today() - timedelta(days= int(config("daystostore")))).date().strftime('%Y%m%d'))
        filestoremove = [x for x in [int(element.split("_")[-1].replace(".csv","")[:8])  for element in availablefiles] if x < referencefiledatatime]
        for stringtomatch in filestoremove:
            for filetoremove in availablefiles:
                filepath = '{}{}'.format(directorypath, filetoremove) if str(
                    stringtomatch) in filetoremove else ""
                if os.path.exists(filepath):
                    os.remove(filepath)
                    self.logger.info(
                        filetoremove+' - file is removed successfully')
                else:
                    self.logger.warning(
                        'Could not delete file!,file does not exists')

    def delete_logs(self):
        # local path
        directorypath = ftpinfo().ftp_logs()
        availablefiles = os.listdir(directorypath)
        print(directorypath)
        referencefiledatatime = int(
            (datetime.today() - timedelta(days=30)).date().strftime('%Y%m%d'))
        filestoremove = [x for x in [int(element.split(
            ".")[0]) for element in availablefiles] if x <= referencefiledatatime]
        print(filestoremove)
        for filetoremove in filestoremove:
            print("for")
            filepath = '{}{}{}'.format(directorypath, filetoremove, '.log')
            if os.path.exists(filepath):
                os.remove(filepath)
                self.logger.info(
                    filetoremove+' - file is removed successfully')
            else:
                self.logger.warning(
                    'Could not delete file!,file does not exists')