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

    def __str__(self):
        return 'time:{}, next:{}, last:{}'.format(self.time, self.next_time,
                                            self.last_time)
    def __repr__(self):
        return str(self)

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
        self._tp_list = sorted(list(self.timepoints))
        self._duration = None

    def __len__(self):
        return len(self._tp_list)

    @property
    def duration(self):
        return self._duration

    @duration.getter
    def duration(self):
        return (self._tp_list[-1] - self._tp_list[0])

    def __str__(self):
        return '{} timepoints spanning {} '.format(len(self), self.duration)

    def __repr__(self):
        return str(self)

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

        if len(arr) == 0:
            return 0
        elif len(arr) == 1:
            if value > arr[0]:
                return indices[arr[0]] + 1
            else:
                return indices[arr[0]]
        else:
            arr_mid = int(len(arr)/2)
            arrLow  = arr[:arr_mid]
            arrHigh = arr[arr_mid:]

            if value>arrLow[-1]:
                out = self._insert_positon(arrHigh,value,indices)
            else:
                out = self._insert_positon(arrLow,value,indices)

        return out

    def _update_timepoint_list(self,tp):
        '''' Function to update the timepoint list and return the insert
        index.'''

        ins_pos = self._insert_positon(self._tp_list, tp.time)
        self._tp_list = self._tp_list[:ins_pos]+[tp.time]+self._tp_list[ins_pos:]

        return ins_pos

    def add_tp(self,tp):
        ''' Function to add a time point object to the timeseries.'''

        ins_pos = self._update_timepoint_list(tp)
        next_tp_index = ins_pos+1
        try:
            next_tp = self.timepoints[ self._tp_list[next_tp_index] ]
            tp.next_tp = next_tp
            next_tp.last_tp = tp
        except IndexError:
            pass

        last_tp_index = ins_pos-1
        if last_tp_index > 0:
            previous_tp = self.timepoints[ self._tp_list[last_tp_index] ]
            tp.last_tp = previous_tp
            previous_tp.next_tp = tp

        self.timepoints[tp.time] = tp

    def add_tp_to_end(self,tp):
        ''' Function to add a time point object at the end of the timeseries.'''

        ins_pos = self._update_timepoint_list(tp)
        last_tp_index = ins_pos-1
        if self._tp_list[last_tp_index] < tp.time:
            previous_tp = self.timepoints[ self._tp_list[last_tp_index] ]
            tp.last_tp = previous_tp
            self.timepoints[tp.time] = tp
            previous_tp.next_tp = tp

        else:
            raise IndexError('Time must be more than the last time stored.')

    def add_tp_to_beginning(self,tp):
        ''' Function to add a time point object at the beginning of the
        timeseries.'''

        ins_pos = self._update_timepoint_list(tp)
        next_tp_index = 1
        if self._tp_list[next_tp_index] > tp.time:
            next_tp = self.timepoints[ self._tp_list[next_tp_index] ]
            tp.next_tp = next_tp
            self.timepoints[tp.time] = tp
            next_tp.last_tp = tp

        else:
            raise IndexError('Time must be more than the last time stored.')
