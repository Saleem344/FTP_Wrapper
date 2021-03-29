#import libraries
from decouple import config
import os,sys
sys.path.append(config("systempath"))
from infrastructure.utilities.app_logs import logs
from infrastructure.utilities.credential import ftpinfo
from infrastructure.sftp.entities.process import sftpoperations
import pysftp


class  SFTP_Operations:
    def __init__(self):
        self.logger = logs().file_logs('ftp')
    
    def data_push(self):
        try:
            credentials = ftpinfo().sftp_Push()
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            local_files = sorted(list(os.listdir(credentials['sftp_push'])), reverse=False)
            filestopush = sorted([x for x in [element.split("_")[-1][:len(config("filenameendingformat"))]  for element in local_files]])
            # check file count
            if(len(local_files) > 0):
                with pysftp.Connection(credentials['host'],username=credentials['username'],private_key=credentials['privatekey'],port=22,cnopts=cnopts) as connection:
                    if connection.isdir(credentials['sftp_path']):
                        sftpoperations().direxists(connection,credentials,local_files,filestopush,self.logger)
                    else:
                        connection.mkdir(credentials['sftp_path'],mode=777)
                        sftpoperations().direxists(connection,credentials,local_files,filestopush,self.logger)
                    # close conn
                    connection.close()
            else:
                self.logger.warning('No files available to push')
        except:
            self.logger.error(sys.exc_info())
    
    def data_pull(self):
        try:
            credentials = ftpinfo().sftp_Pull()
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            with pysftp.Connection(credentials['host'],username=credentials['username'],private_key=credentials['privatekey'],port=22,cnopts=cnopts) as connection:
                connection.chdir(credentials['sftp_path']+"/")                
                sftpfiles = connection.listdir(credentials['sftp_path']+"/")
                if connection.isdir(credentials['sftp_move']):
                    pass
                else:     
                    connection.mkdir(credentials['sftp_move'],mode=777)
                
                for item in sftpfiles:
                    if os.path.isfile(credentials['sftp_pulled']+item):
                        os.remove(credentials['sftp_pulled']+item)
                        connection.get(credentials['sftp_path']+"/"+item,credentials['sftp_pulled']+item)
                        connection.rename(credentials['sftp_path']+"/"+item,credentials['sftp_move']+item)
                        self.logger.info(item + "successfully pulled to location" + credentials['sftp_pulled'])
                    else:
                        connection.get(credentials['sftp_path']+"/"+item,credentials['sftp_pulled']+item)
                        connection.rename(credentials['sftp_path']+"/"+item,credentials['sftp_move']+item)
                        self.logger.info(item + "successfully pulled to location" + credentials['sftp_pulled'])
                # close conn
                connection.close()
        except:
            self.logger.error(sys.exc_info())
                            

