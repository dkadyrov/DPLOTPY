import win32ui
import dde
import pandas as pd
import numpy as np
import dplotpy

class DDE_Channel(object):
    def __init__(self):
        # Open the Server
        self.server = None
        self.channel = None
        self.server = dde.CreateServer()
        self.server.Create("TestClient")
        self.channel = dde.CreateConversation(self.server)
        
        try:
            self.channel.ConnectTo("DPlot","System")
        except:
            self.CloseDPLOTServer(self.server)
            raise Exception('Could not connect to DPlot. (is it open?)')
    
    def __del__(self):
        self.CloseDPLOTServer(self.server)
     
    def CloseDPLOTServer(self,server):
        self.server.Shutdown()
        #self.server.Destroy()
    
    def NewXYPlot(self,plottype=None):
        plot_types = [None,1,3,5]
        try:
            if plottype in plot_types:
                pass
            else:
                raise ValueError('Plottype must be blank or 1,3,5')
        except:
            raise Exception('Plottype must be blank or 1,3,5')
        if plottype == None:
            self.channel.Exec('[filenew()]')
        else:
            self.channel.Exec('[filenew('+str(plottype)+')]')
        self.channel.Exec('[FileArrays(10,10000)]')
        
    def PlotXY(self,curve):
        # Put the curve data into a datafame and set the index to X
        self.df = pd.DataFrame({'x':curve.xdata,'y':curve.ydata})
        self.df.set_index('x',inplace=True)
        # Then copy to clipboard and paste into a new file
        self.df.to_clipboard()        
        self.channel.Exec('[paste()]')
    
    def UpdatePlotCurveProperties(self,curve):
        pass
    

x = np.linspace(0, 2*np.pi, 100)
y_sin = np.sin(x)
y_cos = np.cos(x)

sin_curve = dplotpy.curve(x, y_sin, title='Sine Wave')
cos_curve = dplotpy.curve(x, y_cos, title='Cos Wave')
plt = dplotpy.plot(sin_curve)
ch = DDE_Channel()
ch.NewXYPlot()
ch.PlotXY(sin_curve)
ch.PlotXY(cos_curve)
ch.CloseDPLOTServer(ch.server)