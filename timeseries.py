'''
This script describes an object to store TimeSeries data.
'''

from sorted_collection import SortedCollection

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


class TimeSeries(SortedCollection):

    def __init__(self, name=None):
        super().__init__(key=lambda x: x.time)
        self.name = name
        self._duration = None

    def __str__(self):
        return '{} timepoints spanning {} '.format(len(self), self.duration)

    def __repr__(self):
        return str(self)

    @property
    def duration(self):
        return self._duration

    @duration.getter
    def duration(self):
        return (self._keys[-1] - self._keys[0])

    def add_tp(self,tp):

        self.insert(tp)
        tp_index = self.index(tp)
        if tp_index > 0:
            last_tp = self[tp_index-1]
            tp.last_tp = last_tp
            last_tp.next_tp = tp
        try:
            next_tp = self[tp_index+1]
            tp.next_tp = next_tp
            next_tp.last_tp = tp
        except IndexError:
            pass

    def add_tp_to_end(self,tp):
        ''' Function to add a time point object at the end of the timeseries.'''

        ins_pos = len(self)
        last_tp_index = ins_pos-1

        if self._keys[last_tp_index] < tp.time:

            self._keys.insert(ins_pos, tp.time)
            self._items.insert(ins_pos, tp)

            last_tp = self[last_tp_index]
            tp.last_tp = last_tp
            last_tp.next_tp = tp

        else:
            raise IndexError('Time must be more than the last time stored.')

    def add_tp_to_beginning(self,tp):
        ''' Function to add a time point object at the beginning of the
        timeseries.'''

        ins_pos = 0
        next_tp_index = 1

        if self._tp_list[next_tp_index] > tp.time:

            self._keys.insert(ins_pos, tp.time)
            self._items.insert(ins_pos, tp)

            next_tp = self[next_tp_index]
            tp.next_tp = next_tp
            next_tp.last_tp = tp

        else:
            raise IndexError('Time must be less than the first time stored.')
