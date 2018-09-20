# class.py
class curve(object):
    def __init__(self, xdata, ydata, zdata=None, title='', label='', line='1', symbol='0'):
        self.xdata = xdata
        self.ydata = ydata
        self.data = [   self.xdata,
                        self.ydata]
        if zdata:
            self.zdata = zdata
            self.data.append(self.zdata)
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
    pass
