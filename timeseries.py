'''
This script describes an object to store TimeSeries data.
'''

class TimePoint(object):

    def __init__(self, time, value, last_tp=None, next_tp=None):

        self.time = time
        self.value = value
        self._next_tp = next_tp
        self._last_tp = last_tp
        self.next_time = None
        self.last_time = None

        if next_tp != None:
            self.next_time = self.next_tp.time - self.time
        if last_tp != None:
            self.last_time = self.time - self.last_tp.time

    @property
    def next_tp(self):
        return self._next_tp

    @next_tp.setter
    def next_tp(self,value):
        ''' Defines the set attribute function for the next time point.'''
        try:
            assert( isinstance(value, TimePoint))
        except AssertionError:
            raise TypeError('next_tp has to be a TimePoint object')

        self._next_tp = value
        self.next_time = self.next_tp.time - self.time

    @property
    def last_tp(self):
        return self._last_tp

    @last_tp.setter
    def last_tp(self,value):
        ''' Defines the set attribute function for the previous time point.'''
        try:
            assert( isinstance(value, TimePoint))
        except AssertionError:
            raise TypeError('last_tp has to be a TimePoint object')

        self._last_tp = value
        self.last_time = self.time - self.last_tp.time

class TimeSeries(object):

    def __init__(self, name=None):

        self.name = name
        self._start_tp = None
        self.timepoints = {}
        self._tp_list = list(self.timepoints)

    @property
    def start_tp(self):
        return self._start_tp

    @start_tp.setter
    def start_tp(self,value):
        try:
            assert( isinstance(value, TimePoint))
        except AssertionError:
            raise TypeError('last_tp has to be a TimePoint object')

        self._start_tp = value

    def _insert_positon(self,arr,value,indices=None):
        ''' Function to determine the insert position of a time point in a list
        of sorted time points. '''

        if indices == None:
            indices = {x: arr.index(x) for x in arr}
            
        if len(arr) == 1:
            if value > arr[0]:
                return indices[arr[0]] + 1
            else:
                return indices[arr[0]]
        else:
            arr_mid = len(arr)/2
            arrLow  = arr[:arr_mid]
            arrHigh = arr[arr_mid:]

            if value>arrLow[-1]:
                out = self._insert_positon(arrHigh,value,indices)
            else:
                out = self._insert_positon(arrLow,value,indices)

        return out


    def add_tp(self,tp):
        ''' Function to add a time point object to the timeseries.'''
        insert_postion
