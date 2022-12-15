import sys
import pprint
import numpy as np
import multiprocessing as mp

class Beacon():
    def __init__(self, location, sensor):
        self.location = location
        self.sensor = sensor
        self.sensor_distance = self.manhattan_distance(location, sensor)

    def manhattan_distance(self,p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    def check_distince_in_range(self, p1,p2):
        if self.manhattan_distance(p1,p2)<=self.sensor_distance:
            return True
        else:
            return False

def runner(y, size,sensors):
    print(f"y:{y}")

    beacon_rows = np.zeros(size, dtype='int')
    #create coverage per sensor on row
    for sensor in sensors:
        distance_to_line = abs(sensor.sensor[1] - y)
        distance_remaining = sensor.sensor_distance - distance_to_line
        if distance_remaining >= 0:
            beacon_rows[max(sensor.sensor[0] - distance_remaining,0) : min(sensor.sensor[0] + distance_remaining + 1, size)] = 1

    if sum(beacon_rows)<size:
        print('*** HERE ***')
        print(np.where(beacon_rows == 0)[0][0],y)
        print(np.where(beacon_rows == 0)[0][0] * 4000000 +y)

        with open('output.txt', 'w') as f:
            # Write the string to the file.
            f.writelines([str(np.where(beacon_rows == 0)[0][0]) +'\n', str(y) +'\n',  str(np.where(beacon_rows == 0)[0][0] * 4000000 +y)])

        return np.where(beacon_rows == 0)[0][0] * 4000000 +y

if __name__ == '__main__':
    with open('inputs/day15.txt') as f:

        min_beacon_x =  sys.maxsize
        max_beacon_x = 0


        sensors = []
        beacons = {}
        for line in f:
            sensor_beacon = line.split(':')

            sensor_x = int(sensor_beacon[0].split('=')[1].split(',')[0])
            sensor_y = int(sensor_beacon[0].split('=')[2])

            beacon_x = int(sensor_beacon[1].split('=')[1].split(',')[0])
            beacon_y = int(sensor_beacon[1].split('=')[2])
            min_beacon_x = min(min_beacon_x, beacon_x)
            max_beacon_x = max(max_beacon_x, beacon_x)

            sensors.append(Beacon((beacon_x,beacon_y), (sensor_x,sensor_y)) )
            beacons[beacon_x, beacon_y] = 1

            #calculate which values in row 10 are covered by snesors
        size = 4000000
        args = []

        for i in range(0, size):
            args.append((i,size,sensors))

        with mp.Pool(16) as p:
            result = p.starmap(runner, args)

        print(result)