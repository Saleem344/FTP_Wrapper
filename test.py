# ZPF
# encoding=utf-8
import win32timezone
from logging.handlers import TimedRotatingFileHandler
import win32serviceutil
import win32service
import win32event
import os
import logging
import inspect
import time
import shutil
 
 
class PythonService(win32serviceutil.ServiceFramework):
    _svc_name_ = "PythonService1" # 
    _svc_display_name_ = "Clearjob" #jobName displayed on windows services
    _svc_description_ = "Clear system files"
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._getLogger()
        self.path = 'D:\\WebSite'
        self.T = time.time()
        self.run = True
 
    def SvcDoRun(self):
        self.logger.info("service is run....")
        try:
            while self.run:
                self.logger.info('---Begin---')
                for path, name, file in os.walk('D:\\Website'):
                    if path == 'D:\\Website':
                        for IISname in name:
                            floder = []
                            for i in os.listdir(os.path.join(path, IISname)):
                                if i.isdigit():
                                    floder.append(int(i))
                            if len(floder) == 0:
                                pass
                            elif len(floder) >= 2: # Set up a reserved backup
                                floder.sort()
                                for x in floder[:(len(floder) - 2)]:
                                    self.logger.info("delete dir: %s" % os.path.join(os.path.join(path, IISname), str(x)))
                                    shutil.rmtree(os.path.join(os.path.join(path, IISname), str(x)))
 
                self.logger.info('---End---')
                time.sleep(10)
 
        except Exception as e:
            self.logger.info(e)
            time.sleep(60)
 
    def SvcStop(self):
        self.logger.info("service is stop....")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.run = False
 
 
if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(PythonService)