import sys
import dotenv
import os
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
import time
import win32serviceutil
import win32service
import win32event
import schedule
from app import mainclass
from infrastructure.utilities.app_logs import logs
from infrastructure.utilities.delete import deletefiles


class FTPService(win32serviceutil.ServiceFramework):
    
    _svc_name_ = os.environ["ftpservicename"]
    _svc_display_name_ = os.environ["ftpservicename"]
    _svc_description_ = "Armax FTP Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self.logger = logs().file_logs('ftp')
        self.run = True

    def SvcDoRun(self):
        self.logger.info("service is running...")
        try:
            schedule.every().day.at("10:00").do(mainclass().ftp_delete)
            schedule.every().day.at("10:30").do(deletefiles().delete_logs)
            while self.run:
                try:
                    if os.environ["ftpoperation"] == "push":
                        mainclass().ftp_push()
                    elif os.environ["ftpoperation"] == "pull":
                        mainclass().ftp_pull()
                    schedule.run_pending()
                    time.sleep(60)
                except:
                    self.logger.error(sys.exc_info()[1])
        except:
            self.logger.error(sys.exc_info()[1])
                
    def SvcStop(self):
        self.logger.info("service is stop...")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.run = False


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(FTPService)