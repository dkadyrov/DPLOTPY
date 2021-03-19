import csv 
import numpy as np
import win32ui
import dde

class curve(object):
    def __init__(self, xdata, ydata, zdata='', title="", label="", line=1, symbol=0):
        self.xdata = xdata
        self.ydata = ydata
        self.zdata = zdata

        self.data = [self.xdata, self.ydata]

        if len(self.zdata) != 0:
            self.data.append(self.zdata)

        self.title = title
        self.label = label

        lines = [1,2,3,4,5,6,7]
        
        try: 
            if int(line) in lines: 
                self.line = int(line)
            else:
                raise ValueError("Define a line style (1-7). This must be an integer or a string representation")
        except: 
            #TODO 
            raise Exception("Define a line style (1-7). This must be an integer or a string representation") 

        symbols = []
        for i in range(0, 35):
            symbols.append(i)
        symbols.append([261, 270, 284, 288])

        try: 
            if int(symbol) in symbols: 
                self.symbol = int(symbol)
            else:
                raise ValueError('Define a symbol style (1-34, 261-269, 284, 288). This can be a string or integer input. For available symbols please visit http://www.dplot.com/help/index.htm?dplotfile.htm')
        except: 
            #TODO 
            raise ValueError('Define a symbol style (1-34, 261-269, 284, 288). This can be a string or integer input. For available symbols please visit http://www.dplot.com/help/index.htm?dplotfile.htm')

class legend(object):
    def __init__(self, x=0, y=0, anchor='top right'):
        anchor_dict = { 
            'left': 0,
            'center': 1,
            'right': 2,
            'top': 0,
            'middle': 4,
            'bottom': 8
        }

        self.x = x
        self.y = y

        # TODO Exception Handling
        if type(anchor) == str:
            anchor_str = anchor.split()
            for a in anchor_str:
                if a in ['top', 'middle', 'bottom']:
                    self.anchory = anchor_dict[a]
                if a in ['left', 'center', 'right']:
                    self.anchorx = anchor_dict[a]
            if a not in ['top', 'middle', 'bottom','left', 'center', 'right']:
                raise ValueError('Define an anchor using \"left\", \"center\", \"right\" for x-anchor and \"top\", \"middle\", \"bottom\" for y-anchor. Example: anchor=\'top right\' or anchor=[0 4]')

        if type(anchor) == list:
            self.anchorx = int(anchor[0])
            self.anchory = int(anchor[1])

class plot(object): 
    def __init__(self, curve=None, title="", subtitle="", xlabel="", ylabel="", scale=1, xlim=None, ylim=None):
        if curve == None: 
            self.curves = []
        else: 
            self.curves = [curve]
        
        self.title = title
        self.subtitle = subtitle
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.scale = str(scale)

        self.xlim = xlim #TODO
        self.ylim = ylim 

        self.legend = legend(x=0, y=0, anchor='top right')

    def add_curve(self, curve):
        self.curves.append(curve) 

    def show(self):
        """
        Shows the plot in active DPlot Window. Uses DDE interface - 
        see "Programmer's Reference" in DPlot help. Currently will plot 2D 
        curves. It will generate the data points for 3D contour curves but not
        display them -- this is because error handling must be done
        to ensure a valid triangular mesh can be generated. 

        Returns
        -------
        None.

        """
        #open the DDE channel
        self.server = None
        self.channel = None
        self.server = dde.CreateServer()
        self.server.Create("TestClient")
        self.channel = dde.CreateConversation(self.server)        
        try:
            self.channel.ConnectTo("DPlot","System")
        except:
            self.server.Shutdown()
            self.server = None
            self.channel = None
            raise Exception('Could not connect to DPlot. (Is it open?)')
        # open a new file
        num_dims = len(self.curves[0].data)
        if num_dims == 3:
            self.channel.Exec('[filenew(3)]')
        else:
            self.channel.Exec('[filenew()]')
        # Turn off min-max-mean check until writing is complete
        self.channel.Exec('[DeferMinMaxCheck(1)]')
        
        # plot the curves
        for curve_num,curve in enumerate(self.curves):
            # check to see if xy or xyz data
            num_dims = len(curve.data)
            # Create the output strings for data exchange
            sCurveNum = str(curve_num+1)
            Data = [None]*curve.xdata.size*num_dims
            Data[::num_dims] = curve.xdata.tolist()
            Data[1::num_dims] = curve.ydata.tolist()
            if num_dims == 3:
                Data[2::num_dims] = curve.zdata.tolist()
            sData = [str(data) for data in Data]
            sOutput = ','.join(([str(curve.xdata.size)] + sData))
            #Select Curve Number
            self.channel.Exec('[SelectCurve('+sCurveNum+')]')
            # Write data
            if num_dims == 3:
                self.channel.Exec('[XYZEx(0,'+sOutput+')]')
            else:
                self.channel.Exec('[XYXY('+sOutput+')]')
            # Write attributes
            # Legend
            self.channel.Exec('[Legend('+ sCurveNum+',"'+curve.title +'")]')
            # Label
            self.channel.Exec('[CurveLabel('+ sCurveNum+',"'+ curve.label+'")]')
            # Linetype
            sCurveLT = str(curve.line)
            self.channel.Exec('[LineType('+sCurveNum+','+sCurveLT+')]')
            # Symbol
            sCurveSymbol = str(curve.symbol)
            self.channel.Exec('[SymbolType('+sCurveNum+','+sCurveSymbol+')]')
        '''
        TODO - XYZ plots. Note that XYZ plots must form a valid triangular
        mesh. So have to perform error handling to make sure x,y,z form a grid,etc.
        '''
        if num_dims == 3:
            pass
            #self.channel.Exec('[XYZRegen()]')
            #self.channel.Exec('[ViewRedraw()]')
        # Title, Subtitle, Axis Labels
        self.channel.Exec('[Title1("'+self.title+'")]')
        self.channel.Exec('[Title2("'+self.subtitle+'")]')
        self.channel.Exec('[XAxisLabel("'+self.xlabel+'")]')
        self.channel.Exec('[YAxisLabel("'+self.ylabel+'")]')
        
        # Turn back on functionality
        self.channel.Exec('[DeferMinMaxCheck(0)]')
        # shutdown the DDE server and cleanup
        self.server.Shutdown()
        self.server = None
        self.channel = None

    def save(self, filename):
        filename += ".grf"

        with open(filename, 'w', newline='') as f: 
            f.write('DPlot v1.6\n')

            if self.curves[0].zdata == None:
                f.write('data\n')
            else:
                f.write('3DR\n')

            n = int(len(self.curves)) # Number of Curves

            f.write('%d\n'%n) # Print number of curves

            writer = csv.writer(f, delimiter = ',') # initialize csv writer

            for i in range(n):
                f.write('%d\n' %len(self.curves[i].xdata))
                if self.curves[i].zdata == None:
                    writer.writerows(zip(self.curves[i].xdata,self.curves[i].ydata))
                else:
                    writer.writerows(zip(self.curves[i].xdata,self.curves[i].ydata,self.curves[i].zdata))
                f.write('%s,%s\n' %(self.curves[i].line, self.curves[i].symbol))
                f.write('%s\n' %(self.curves[i].title)) # Curve Legend Title
                f.write('%s\n' %(self.curves[i].label)) # Curve Label

            f.write('%s\n' %self.title)
            f.write('%s\n' %self.subtitle)
            f.write('%s\n' %self.xlabel)
            f.write('%s\n' %self.ylabel)
            f.write('%s\n' %self.scale)

            # TODO Write Legend info
            if self.legend: 
                f.write('%f,%f,%d %d\n'%(self.legend.x,self.legend.y,self.legend.anchorx,self.legend.anchory))
                
            if self.xlim:
                f.write('ManualScaleX\n')
                f.write('%f,%f' %(self.xlim[0], self.xlim[1]))
            if self.ylim:
                f.write('ManualScaleY\n')
                f.write('%f,%f' %(self.ylim[0], self.ylim[1]))


x = np.linspace(0, 2*np.pi, 100)
y_sin = np.sin(x)
y_cos = np.cos(x)

sin_curve = curve(x, y_sin, title='Sine Wave 2021')
cos_curve = curve(x,y_cos,title='Cos Curve',line=3,symbol=3)
plt = plot(sin_curve,title="Main Title",subtitle='Subtitle',
           xlabel="x (units)", ylabel="y (units)")
plt.add_curve(cos_curve)
plt.show()
#plt.save("test")

y = x
z = x*np.sin(y)
z_curve = curve(x,y,zdata=z,title='x+sin(y)')
#plt2 = plot(z_curve)
#plt2.show()