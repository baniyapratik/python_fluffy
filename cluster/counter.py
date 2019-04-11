from __future__ import print_function

import sys
import time
from functools import partial
sys.path.append("../")
from raft_service.PySyncObj.pysyncobj import SyncObj, replicated

class TestObj(SyncObj):

    def __init__(self, selfNodeAddr, otherNodeAddrs):
        super(TestObj, self).__init__(selfNodeAddr, otherNodeAddrs)
        self.__counter = 0

    @replicated
    def incCounter(self):
        self.__counter += 1
        return self.__counter

    @replicated
    def addValue(self, value, cn):
        self.__counter += value
        return self.__counter, cn

    def getCounter(self):
        return self.__counter


    def onAdd(res, err, cnt):
        print('onAdd %d:' % cnt, res, err)