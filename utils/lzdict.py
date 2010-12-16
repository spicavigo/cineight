#!/usr/bin/env python
#
#       lzdict.py
#       
#       Copyright 2010 yousuf <yousuf@postocode53.com>
#       

class lzdict(dict):
    def __init__(self, *args, **kwargs):
        self.order = []
        super(lzdict, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if not key in self.order:
            self.order.append(key)
        super(lzdict, self).__setitem__(key, value)

    def __delitem__(self, key):
        self.order.remove(key)
        super(lzdict, self).__delitem__(key)

    def __iter__(self):
        for key in self.order:
            yield key

    def items(self):
        for key in self.order:
            yield key, self.__getitem__(key)

    def __deepcopy__(self, memo):
        obj = lzdict()
        for k,v in self.items():
            obj[k] = v
        #memo[self] = obj
        return obj
