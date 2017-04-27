'''
This script can be used to parse out the timeseries data from the raw
files obtained from Intel
'''

import csv
from datetime import datetime

from timeseries import TimePoint, TimeSeries

def parse_header(header):

    #user,measure,timestamp-start,timestamp-end,value
    time_ind = header.index('timestamp-start')
    data_ind = header.index('value')

    return time_ind, data_ind

def parse_data_line(line,file_type,time_ind,data_ind):

    ''' Function to parse the data depending on the file type i.e. either
    tremor calls or movement data.'''

    time_point = datetime.strptime( line[time_ind], '%Y-%m-%d %H:%M:%S.%f')

    if file_type == 'tremor':
        # sc012l,Tremor Score,2016-03-29 19:18:55.000,,{Value=0.0}
        data_value = float(line[data_ind].split('=')[1].split('}')[0])

    elif file_type == 'movement':
        # sc012l,Pebble Accelerometer,2016-03-29 19:35:47.807,
        #         ,{z=-960.0, y=-120.0, x=-360.0}

        temp = line[data_ind:data_ind+3]
        temp = map(lambda x: x.strip('}').strip('{'), temp)
        data_value = map(lambda x: float(x.split('=')[1]), temp)

    else:
        raise typeerror('wrong file type. only "tremor" or \
                                                "movement" allowed')

    return time_point, data_value

def initialize_time_series(data_line,time_ind,data_ind):

    TS = TimeSeries()
    date, value = parse_data_line(data_line,file_type,time_ind,data_ind)
    timepoint = TimePoint(date,value)
    TS.add_tp(timepoint)

    return TS


def parse_file(file_path,file_type,outp_file_path):

    with open(file_path,'r',newline='') as csv_file:

        csv_data = csv.reader(csv_file)
        header = next(csv_data)
        time_ind, data_ind = parse_header(header)

        # Set the first time point object
        line = next(csv_data)
        TS = initialize_time_series(line,time_ind, data_ind)

        line = next(csv_data)
        while line:
            try:
                date, value = parse_data_line(line,file_type,
                                                time_ind,data_ind)
                current_tp = TimePoint(date,value)
                TS.add_tp_to_end(current_tp)

                # Update the line
                line = next(csv_data)

            except StopIteration:
                break

        print(TS)
        print(TS._tp_list)
        for i in TS._tp_list:
            print(i,TS.timepoints[i])

if __name__ == '__main__':

    import sys

    inp_file = sys.argv[1]
    outp_file = sys.argv[2]
    file_type = sys.argv[3]

    parse_file(inp_file,file_type,outp_file)

    '''
    t = TimeSeries()
    x = [1,4,5,9,12,15,21,27]
    d = 0
    q = t._insert_positon(x, d)
    x = x[0:q]+[d]+x[q:]

    print(q,x)
    '''
