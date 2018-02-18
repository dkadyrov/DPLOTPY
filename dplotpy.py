import csv

class curve(object):
    def __init__(self, xdata, ydata, title='', label='', line='1', symbol='0'):
        self.xdata = xdata
        self.ydata = ydata
        self.data = [self.xdata, self.ydata]
        self.title = title
        self.label = label

        #TODO Line definitions (1-7)
        lines = [1, 2, 3, 4, 5, 6, 7]
        for l in lines:
            lines.append(str(l))
        print(line)
        if line in lines:
            print('True')
            self.line = line
        else:
            raise ValueError('Define a line style (1-7). This can be a string or integer input.')

        #TODO Symbol definitions (1-34, 261-269, 284, 288)
        symbols = []
        for i in range (0,35):
            symbols.append(i)
        for i in range(261,270):
            symbols.append(i)
        symbols.append(284)
        symbols.append(288)
        for s in symbols:
            symbols.append(str(s))
        if symbol in symbols:
            self.symbol = symbol
        else:
            raise ValueError('Define a symbol style (1-34, 261-269, 284, 288). This can be a string or integer input. For available symbols please visit http://www.dplot.com/help/index.htm?dplotfile.htm')


class legend(object):
    def __init__(self, x=0, y=0, anchor='top right'):
        anchor_dict = { 'left':0,
                        'center':1,
                        'right':2,
                        'top':0,
                        'middle':4,
                        'bottom':8}

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

class xyplot(object):

    #TODO add more parameters to self
    def __init__(self, curve=None, title='', subtitle='', xlabel='', ylabel='', scale='1', xlim=None, ylim=None):
        if curve is None:
            self.curves = []
        else:
            self.curves = [curve]

        self.title = title
        self.subtitle = subtitle
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.scale = str(scale)

        # TODO Extras
        self.xlim = xlim # TODO Add error handling
        self.ylim = xlim

        self.legend = legend(0, 0, anchor='top right')

    def add_curve(self, curve):
        self.curves.append(curve)

    def save(self, filename):
        filename = filename + '.grf'
        with open(filename, 'w', newline='') as f:
            f.write('DPlot v1.6\n')
            f.write('data\n')

            n = int(len(self.curves)) # Number of Curves

            f.write('%d\n'%n) # Print number of curves

            writer = csv.writer(f, delimiter = ',') # initialize csv writer

            for i in range(n):
                f.write('%d\n' %len(self.curves[i].xdata))
                writer.writerows(zip(self.curves[i].xdata,self.curves[i].ydata))
                f.write('%s,%s\n' %(self.curves[i].line, self.curves[i].symbol))
                f.write('%s\n' %(self.curves[i].title)) # Curve Legend Title
                f.write('%s\n' %(self.curves[i].label)) # Curve Label

            f.write('%s\n'%self.title)
            f.write('%s\n'%self.subtitle)
            f.write('%s\n'%self.xlabel)
            f.write('%s\n'%self.ylabel)
            f.write('%s\n'%self.scale)

            # TODO Write Legend info
            f.write('%f,%f,%d %d\n'%(self.legend.x,self.legend.y,self.legend.anchorx,self.legend.anchory))
            if self.xlim:
                f.write('ManualScaleX\n')
                f.write('%f,%f' %(self.xlim[0], self.xlim[1]))
            if self.ylim:
                f.write('ManualScaleY\n')
                f.write('%f,%f' %(self.ylim[0], self.ylim[1]))
