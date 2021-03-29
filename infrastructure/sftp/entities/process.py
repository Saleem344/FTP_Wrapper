# import libraries
import os,shutil
from decouple import config


class sftpoperations:
        
    def localfileexits(self,credentials,item,logger):
            if (os.path.exists(credentials['sftp_pushed']+item)):
                os.remove(credentials['sftp_pushed']+item)
                shutil.move(credentials['sftp_push']+item,credentials['sftp_pushed']+item)
                logger.info(item+' is successfully moved to local directory')                   
            else:
                shutil.move(credentials['sftp_push']+item,credentials['sftp_pushed']+item)
                logger.info(item+' is successfully moved to local directory') 
    
    def sftppushoverwrite(self,credentials,connection,item,logger):
        connection.remove(credentials['sftp_path']+"/"+item)
        connection.put(credentials['sftp_push']+item, credentials['sftp_path'] +"/"+item)
        logger.info(item+' file successfully pushed to '+credentials['sftp_path']) 

    def sftppush(self,credentials,connection,item,logger):
        connection.put(credentials['sftp_push']+item, credentials['sftp_path']+"/"+item)
        logger.info(item+' file successfully pushed to '+credentials['sftp_path']) 

    def direxists(self,connection,credentials,localfiles,filestopush,logger):
        connection.chdir(credentials['sftp_path']+"/")
        if config("ftpfileoverwrite") == "yes":
            for index,filetopush in enumerate(localfiles):
                if filestopush[index] in filetopush:
                    if connection.isfile(credentials['sftp_path'] +"/"+ filetopush):
                        sftpoperations().sftppushoverwrite(credentials,connection,filetopush,logger)
                    else:
                        sftpoperations().sftppush(credentials,connection,filetopush,logger)
                    sftpoperations().localfileexits(credentials,filetopush,logger)
        else:
            for index,filetopush in enumerate(localfiles):
                if filestopush[index] in filetopush:
                    sftpoperations().sftppush(credentials,connection,filetopush,logger)
                    sftpoperations().localfileexits(credentials,filetopush,logger)
