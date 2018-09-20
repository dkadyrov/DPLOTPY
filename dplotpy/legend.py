# class legend

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
