import sys
import dotenv
import os
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
import time
import win32serviceutil
import win32service
import win32event
import socket
import servicemanager
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
        socket.setdefaulttimeout(60)
        self.isAlive = True

    def SvcStop(self):
        self.isAlive = False
        self.logger.info("service is stop...")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
            
    def SvcDoRun(self):
        self.isAlive = True
        self.logger.info("service is running...")
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        self.main()
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def main(self):
        try:
            schedule.every().day.at("10:00").do(mainclass().ftp_delete)
            schedule.every().day.at("10:30").do(deletefiles().delete_logs)
            while self.isAlive:
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

        
if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(FTPService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(FTPService)