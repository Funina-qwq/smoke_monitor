import win32serviceutil
import win32service
import win32event 

class PythonService(win32serviceutil.ServiceFramework):
      _svc_name_ = "PythonService"
      _svc_display_name_ = "Python Service Test"
      _svc_description_ = "E2ec service"

      def __init__(self, args):
          super().__init__(args)
          self.hWaitStop = win32event.CreateEvent(None,0,0,None)

      def SvcDoRun(self):
         # main()
          print(123)
          win32event.WaitForSingleObject(self.hWaitStop,win32event.INFINITE)

      def SvcStop(self):
          self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
          win32event.SetEvent(self.hWaitStop)
          
if __name__ == "__main__":      
   win32serviceutil.HandleCommandLine(PythonService)