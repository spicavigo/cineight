# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="naved"
__date__ ="$22 Jun, 2010 1:32:06 PM$"

from utils.callback import Callback
cb = Callback()

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

def get_callback(request):
    if request.GET:
        data_id = request.GET['data_id'].split('+')
    else:
        data_id = request.POST['data_id'].split('+')
    func = cb._registry[data_id[0]]
    return func(request)
