#!/usr/bin/env python

import os


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
for tcp_var in ['Reno', 'SACK']:
    for que_alg in ['DropTail', 'RED']:
        os.system("/course/cs4700f12/ns-allinone-2.35/bin/ns " + "experiment3.tcl " + tcp_var + " " + str(que_alg))

f1 = open('exp3_data/3_throughput.dat', 'w')
f3 = open('exp3_data/3_latency.dat', 'w')

for que_alg in ['DropTail', 'RED']:
    str_throughput = ''
    str_latency = ''

    for tcp_var in ['Reno', 'SACK']:
        # Open the throughput files for TCP variants and rates and calculate the throughput.
        filename = "exp3_output/experiment3_" + tcp_var + "_" + str(que_alg) + ".out"
        f = open(filename)
        lines = f.readlines()
        f.close()
        start_time = 10.0
        end_time = 0.0
        recvdSize = 0
        for line in lines:
            entry = C(line)
            if entry.pkt_type in ['tcp', 'ack']:
                if entry.event == "+" and entry.from_node == "0":
                    if entry.time < start_time:
                        start_time = entry.time
                if entry.event == "r":
                    recvdSize += entry.pkt_size * 8
                    end_time = entry.time
        str_throughput = str_throughput + '\t' + str(recvdSize / (end_time - start_time) / (1024 * 1024))

        # Open the latency files for TCP Variants and rates and calculate the delay.
        filename = "exp3_output/experiment3_" + tcp_var + "_" + str(que_alg) + ".out"
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
            str_latency = '0'  # CHECK -- str latency
        str_latency = str_latency + '\t' + str(total_duration / num_packets * 1000)

    f1.write("Algorithm: " + str(que_alg) + " Throughputs: " + str_throughput + '\n')
    f3.write("Algorithm: " + str(que_alg) + " Latencies: " + str_latency + '\n')

f1.close()
f3.close()
