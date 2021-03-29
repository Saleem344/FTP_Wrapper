from decouple import config
import os,sys
sys.path.append(config("systempath"))
import ftplib
from infrastructure.utilities.app_logs import logs
from infrastructure.utilities.credential import ftpinfo
from infrastructure.ftp.entities.process import ftpoperations

class FTP_Operations:
    def __init__(self):
        self.logger = logs().file_logs('ftp')

    def data_push(self):
        try:
            credentials = ftpinfo().ftp_Push()
            # files list
            local_files = sorted(
                list(os.listdir(credentials['ftp_push'])), reverse=False)
            filestopush = sorted([x for x in [element.split("_")[-1][:len(config("filenameendingformat"))]  for element in local_files]])
            # check file count
            if(len(local_files) > 0):
                # connection
                connection = ftplib.FTP(
                    credentials['host'], credentials['username'], credentials['password'])
                ftpdir = set(connection.nlst())
                if str(credentials['ftp_path']).split("/")[-1] in ftpdir:
                    ftpoperations().ftpdirexists(connection,credentials,filestopush,local_files,self.logger)
                    # close conn
                    connection.quit()
                else:
                    connection.mkd(credentials['ftp_path'])
                    ftpoperations().ftpdirexists(connection,credentials,filestopush,local_files,self.logger)
                    # close conn
                    connection.quit()
            else:
                self.logger.warning('No files available to push')
        except:
            self.logger.error(sys.exc_info())

    def data_pull(self):
        try:
            credentials = ftpinfo().ftp_Pull()
            # connection
            connection = ftplib.FTP(
                credentials['host'], credentials['username'], credentials['password'])
            
            # files list
            connection.cwd(credentials['ftp_path']+"/")
            FTP_files = sorted(list(connection.nlst()), reverse=False)
            self.logger.info('FTP directory files count '+str(len(FTP_files)))

            # loop for files
            for item in FTP_files:
                # check file is already available
                if(os.path.exists(credentials['pulled']+item)):
                    os.remove(credentials['pulled']+item)
                    write_file = open(credentials['pulled']+item, 'wb')
                    connection.retrbinary("RETR %s" %item, write_file.write)
                    self.logger.info(item+' file successfully pulled from ' +
                                credentials['ftp_path'])
                    connection.delete(item)
                    write_file.close()
                else:
                    write_file = open(credentials['pulled']+item, 'wb')
                    connection.retrbinary("RETR %s" %item, write_file.write)
                    self.logger.info(item+' file successfully pulled from ' +
                                credentials['ftp_path'])
                    connection.delete(item)
                    write_file.close()
            # close conn
            connection.quit()
        except:
            self.logger.error(sys.exc_info())
