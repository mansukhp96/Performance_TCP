#!/usr/bin/env python

import os

TCP_Variant = ['Tahoe', 'Reno', 'Newreno', 'Vegas']


class Record:
    def __init__(self, line):
        contents = line.split()
        self.event = contents[0]
        self.time = float(contents[1])
        self.from_node = contents[2]
        self.to_node = contents[3]
        self.pkt_type = contents[4]
        self.pkt_size = int(contents[5])
        # self.src_addr = contents[8]
        # self.dst_addr = contents[9]
        self.seq_num = contents[10]
        # self.pkt_id = contents[11]


# Generate trace file
for var in TCP_Variant:
    for rate in range(1, 11):
        os.system("/course/cs4700f12/ns-allinone-2.35/bin/ns " + "experiment1.tcl " + var + " " + str(rate))

f1 = open('exp1_throughput.dat', 'w')
f2 = open('exp1_droprate.dat', 'w')
f3 = open('exp1_delay.dat', 'w')

for rate in range(1, 11):
    str_throughput = ''
    str_droprate = ''
    str_latency = ''

    for var in TCP_Variant:
        # Open the throughput files for TCP variants and rates and calculate the throughput.
        filename = "experiment1_" + var + "_" + str(rate) + ".out"
        f = open(filename)
        lines = f.readlines()
        f.close()
        start_time = 10.0
        end_time = 0.0
        recvdSize = 0
        for line in lines:
            record = Record(line)
            if record.pkt_type in ["tcp", "ack"]:
                if record.event == "+" and record.from_node == "0":
                    if record.time < start_time:
                        start_time = record.time
                if record.event == "r":
                    recvdSize += record.pkt_size * 8
                    end_time = record.time
                    # print('DEBUG:' + str(recvdSize) + ' ' + str(end_time) + ' ' + str(start_time))
        str_throughput = str_throughput + '\t' + str(recvdSize / (end_time - start_time) / (1024 * 1024))

        # Open the droprate files for TCP Variants and rates and calculate the droprate.
        filename = "experiment1_" + var + "_" + str(rate) + ".out"
        f = open(filename)
        lines = f.readlines()
        f.close()
        sendNum = recvdNum = 0
        for line in lines:
            record = Record(line)
            if record.pkt_type in ["tcp", "ack"]:
                if record.event == "+":
                    sendNum += 1
                if record.event == "r":
                    recvdNum += 1
        if sendNum == 0:
            str_droprate = '0'
        else:
            str_droprate = str_droprate + '\t' + str(float(sendNum - recvdNum) / float(sendNum))

        # Open the latency files for TCP Variants and rates and calculate the delay.
        filename = "experiment1_" + var + "_" + str(rate) + ".out"
        f = open(filename)
        lines = f.readlines()
        f.close()
        start_time = {}
        end_time = {}
        total_duration = 0.0
        total_packet = 0
        for line in lines:
            record = Record(line)
            if record.pkt_type in ["tcp", "ack"]:
                if record.event == "+" and record.from_node == "0":
                    start_time.update({record.seq_num: record.time})
                if record.event == "r" and record.to_node == "0":
                    end_time.update({record.seq_num: record.time})
        packets = {x for x in start_time.viewkeys() if x in end_time.viewkeys()}
        for i in packets:
            start = start_time[i]
            end = end_time[i]
            duration = end - start
            if duration > 0:
                total_duration += duration
                total_packet += 1
        if total_packet == 0:
            str_latency = '0'
        str_latency = str_latency + '\t' + str(total_duration / total_packet * 1000)

    f1.write(str(rate) + str_throughput + '\n')
    f2.write(str(rate) + str_droprate + '\n')
    f3.write(str(rate) + str_latency + '\n')
f1.close()
f2.close()
f3.close()
