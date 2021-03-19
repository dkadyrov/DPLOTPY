import csv
from curve import curve
from legend import legend

class plot(object):

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
            f.write('%f,%f,%d %d\n'%(self.legend.x,self.legend.y,self.legend.anchorx,self.legend.anchory))
            if self.xlim:
                f.write('ManualScaleX\n')
                f.write('%f,%f' %(self.xlim[0], self.xlim[1]))
            if self.ylim:
                f.write('ManualScaleY\n')
                f.write('%f,%f' %(self.ylim[0], self.ylim[1]))