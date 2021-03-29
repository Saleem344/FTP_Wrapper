# import libraries
import os,shutil
from decouple import config


class ftpoperations:
        
    def localfileexits(self,credentials,item,logger):
            if (os.path.exists(credentials['ftp_pushed']+item)):
                os.remove(credentials['ftp_pushed']+item)
                shutil.move(credentials['ftp_push']+item,credentials['ftp_pushed']+item)
                logger.info(item+' is successfully moved to local directory')                   
            else:
                shutil.move(credentials['ftp_push']+item,credentials['ftp_pushed']+item)
                logger.info(item+' is successfully moved to local directory') 
    
    def ftppushoverwrite(self,credentials,connection,item,logger):
        read_file = open(credentials['ftp_push']+item,'rb')
        connection.delete(item)
        connection.storbinary('STOR %s' % item,read_file)
        logger.info(item+' file successfully pushed to '+credentials['ftp_path']+"/") 
        read_file.close()

    def ftppush(self,credentials,connection,item,logger):
        read_file = open(credentials['ftp_push']+item,'rb')
        connection.storbinary('STOR %s' % item,read_file)
        logger.info(item+' file successfully pushed to '+credentials['ftp_path']+"/") 
        read_file.close()

    def ftpdirexists(self,connection,credentials,filestopush,localfiles,logger):
        # files list
        connection.cwd(credentials['ftp_path']+"/")
        #loop for files
        if config("ftpfileoverwrite") == "yes":
            ftpfiles = set(connection.nlst())
            for index,filetopush in enumerate(localfiles):
                if filestopush[index] in filetopush:
                    if  filetopush in ftpfiles:
                        ftpoperations().ftppushoverwrite(credentials,connection,filetopush,logger)
                    else:
                        ftpoperations().ftppush(credentials,connection,filetopush,logger)
                    ftpoperations().localfileexits(credentials,filetopush,logger)
        else:
             for index,filetopush in enumerate(localfiles):
                if filestopush[index] in filetopush:
                    ftpoperations().ftppush(credentials,connection,filetopush,logger)
                    ftpoperations().localfileexits(credentials,filetopush,logger)
