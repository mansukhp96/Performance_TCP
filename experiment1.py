#!/usr/bin/env python

import os

TCP = ['Tahoe', 'Reno', 'Newreno', 'Vegas']


class C:
    def __init__(self, line):
        contents = line.split()
        self.event = contents[0]
        self.time = float(contents[1])
        self.from_node = contents[2]
        self.to_node = contents[3]
        self.pkt_type = contents[4]
        self.pkt_size = int(contents[5])
        self.seq_num = contents[10]


# Generate trace file
for var in TCP:
    for rate in range(1, 16):
        os.system("/course/cs4700f12/ns-allinone-2.35/bin/ns " + "experiment1.tcl " + var + " " + str(rate))

f1 = open('exp1_data/1_throughput.dat', 'w')
f2 = open('exp1_data/1_droprate.dat', 'w')
f3 = open('exp1_data/1_latency.dat', 'w')

for rate in range(1, 16):
    str_throughput = ''
    str_droprate = ''
    str_latency = ''

    for var in TCP:
        # Open the throughput files for TCP variants and rates and calculate the throughput.
        filename = "exp1_output/experiment1_" + var + "_" + str(rate) + ".out"
        f = open(filename)
        lines = f.readlines()
        f.close()
        start_time = 10.0
        end_time = 0.0
        recvdSize = 0
        for line in lines:
            cur = C(line)
            if cur.pkt_type in ["tcp", "ack"]:
                if cur.event == "+" and cur.from_node == "0":
                    if cur.time < start_time:
                        start_time = cur.time
                if cur.event == "r":
                    recvdSize += cur.pkt_size * 8
                    end_time = cur.time
        str_throughput = str_throughput + '\t' + str(recvdSize / (end_time - start_time) / (1024 * 1024))

        # Open the droprate files for TCP Variants and rates and calculate the droprate.
        filename = "exp1_output/experiment1_" + var + "_" + str(rate) + ".out"
        f = open(filename)
        lines = f.readlines()
        f.close()
        sendNum = recvdNum = 0
        for line in lines:
            cur = C(line)
            if cur.pkt_type in ["tcp", "ack"]:
                if cur.event == "+":
                    sendNum += 1
                if cur.event == "r":
                    recvdNum += 1
        if sendNum == 0:
            str_droprate = '0'
        else:
            str_droprate = str_droprate + '\t' + str(float(sendNum - recvdNum) / float(sendNum))

        # Open the latency files for TCP Variants and rates and calculate the delay.
        filename = "exp1_output/experiment1_" + var + "_" + str(rate) + ".out"
        f = open(filename)
        lines = f.readlines()
        f.close()
        start_dict = {}
        end_dict = {}
        total_duration = 0.0
        num_packets = 0

        for line in lines:
            entry = C(line)
            if entry.pkt_type in ["tcp", "ack"]:
                if entry.from_node == "0" and entry.event == "+":
                    # tracking start time of all packets originating from node 0 that are queueing
                    start_dict[entry.seq_num] = entry.time
                elif entry.to_node == "0" and entry.event == "r":
                    # tracking end time of all packets returning ACKs at node 0
                    end_dict[entry.seq_num] = entry.time

        for key in start_dict:
            if key in end_dict.keys():
                period = end_dict[key] - start_dict[key]
                if period > 0:
                    total_duration += period
                    num_packets += 1

        if num_packets == 0:
            str_latency = '0' # CHECK -- str latency
        str_latency = str_latency + '\t' + str(total_duration / num_packets * 1000)

    f1.write("Rate: " + str(rate) + " Throughputs: " + str_throughput + '\n')
    f2.write("Rate: " + str(rate) + " Droprates: " + str_droprate + '\n')
    f3.write("Rate: " + str(rate) + " Latencies: " + str_latency + '\n')

f1.close()
f2.close()
f3.close()
