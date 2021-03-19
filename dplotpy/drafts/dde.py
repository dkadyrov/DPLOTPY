import win32ui
import dde
import pandas as pd

class DDE_Channel(object):
    def __init__(self,server=None,chanel=None):
        # Open the Server
        self.server = dde.CreateServer()
        self.server.Create("TestClient")
        self.channel = dde.CreateConversation(s)
        
        try:
            self.channel.ConnectTo("DPlot","System")
        except:
            CloseDPLOTServer()
            raise Exception('Could not connect to DPlot. (is it open?)')
    
    def __del__(self):
        CloseDPLOTServer(self.server)
     
    def CloseDPLOTServer(self):
        self.server.Destroy()
        
    def PlotXY(self,curve):
        self.df = pd.DataFrame({'x':curve.xdata,'y':curve.ydata})
        self.df.set_index('x',inplace=True)
        self.df.to_clipboard()
        
        self.channel.Exec('[filenew()paste()]')