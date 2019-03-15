#!/usr/bin/env python

import os

TCP_Variant2 = ['Reno_Reno', 'Newreno_Reno', 'Vegas_Vegas', 'Newreno_Vegas']

ns_command = "/course/cs4700f12/ns-allinone-2.35/bin/ns "


class Record:
    def __init__(self, line):
        contents = line.split()
        self.event_type = contents[0]
        self.time = float(contents[1])
        self.from_node = contents[2]
        self.to_node = contents[3]
        self.pkt_type = contents[4]
        self.pkt_size = int(contents[5])
        self.flow_id = contents[7]
        self.src_addr = contents[8]
        self.dst_addr = contents[9]
        self.sequence_num = contents[10]
        self.pkt_id = contents[11]


def get_throughput(var, rate):
    filename = "exp2_output/experiment2_" + str(var) + "_" + str(rate) + ".out"
    f = open(filename)
    lines = f.readlines()
    f.close()
    # Set counters
    start_time1 = start_time2 = 10.0
    end_time1 = end_time2 = 0.0
    recvdSize1 = recvdSize2 = 0

    for line in lines:
        record = Record(line)
        if record.flow_id == "1":  # TCP stream from 1 to 4
            if record.event_type == "+" and record.from_node == "0":
                if (record.time < start_time1):
                    start_time1 = record.time
            if record.event_type == "r":
                recvdSize1 += record.pkt_size * 8
                end_time1 = record.time
        if record.flow_id == "2":  # TCP stream from 5 to 6
            if record.event_type == "+" and record.from_node == "4":
                if record.time < start_time2:
                    start_time2 = record.time
            if record.event_type == "r":
                recvdSize2 += record.pkt_size * 8
                end_time2 = record.time

                # print('DEBUG:' + str(recvdSize) + ' ' + str(end_time) + ' ' + str(start_time))
    th1 = recvdSize1 / (end_time1 - start_time1) / (1024 * 1024)
    th2 = recvdSize2 / (end_time2 - start_time2) / (1024 * 1024)
    return str(th1) + '\t' + str(th2)


def get_drop_rate(var, rate):
    filename = "exp2_output/experiment2_" + str(var) + "_" + str(rate) + ".out"
    f = open(filename)
    lines = f.readlines()
    f.close()

    sendNum1 = recvdNum1 = 0
    sendNum2 = recvdNum2 = 0

    for line in lines:
        record = Record(line)
        if record.flow_id == "1":
            if record.event_type == "+":
                sendNum1 += 1
            if record.event_type == "r":
                recvdNum1 += 1
        if record.flow_id == "2":
            if record.event_type == "+":
                sendNum2 += 1
            if record.event_type == "r":
                recvdNum2 += 1

    dr1 = 0 if sendNum1 == 0 else float(sendNum1 - recvdNum1) / float(sendNum1)
    dr2 = 0 if sendNum2 == 0 else float(sendNum2 - recvdNum2) / float(sendNum2)
    return str(dr1) + '\t' + str(dr2)


def getLatency(var, rate):
    filename = "exp2_output/experiment2_" + str(var) + "_" + str(rate) + ".out"
    tcl_file = open(filename)
    lines = tcl_file.readlines()
    tcl_file.close()

    tcp1_start_dict = {}
    tcp1_end_dict = {}
    tcp1_total_duration = 0.0
    tcp1_num_packets = 0

    tcp2_start_dict = {}
    tcp2_end_dict = {}
    tcp2_total_duration = 0.0
    tcp2_num_packets = 0

    for line in lines:
        entry = Record(line)

        if entry.flow_id == "1":
            if entry.from_node == "0" and entry.event_type == "+":
                # tracking start time of all packets originating from node 0 for the first TCP flow that are
                # queueing
                tcp1_start_dict[entry.sequence_num] = entry.time
            elif entry.to_node == "0" and entry.event_type == "r":
                # tracking end time of all packets returning ACKs at node 0 for the first TCP flow
                tcp1_end_dict[entry.sequence_num] = entry.time

        if entry.flow_id == "2":
            if entry.from_node == "4" and entry.event_type == "+":
                # tracking start time of all packets originating from node 0 for the second TCP flow that are
                # queueing
                tcp2_start_dict[entry.sequence_num] = entry.time
            elif entry.to_node == "0" and entry.event_type == "r":
                # tracking end time of all packets returning ACKs at node 0 for the second TCP flow
                tcp2_end_dict[entry.sequence_num] = entry.time

    for key in tcp1_start_dict:
        if key in tcp1_end_dict.keys():
            period = tcp1_end_dict[key] - tcp1_start_dict[key]
            if period > 0:
                tcp1_total_duration += period
                tcp1_num_packets += 1

    for key in tcp2_start_dict:
        if key in tcp2_end_dict.keys():
            period = tcp2_end_dict[key] - tcp2_start_dict[key]
            if period > 0:
                tcp2_total_duration += period
                tcp2_num_packets += 1

    if tcp1_num_packets == 0:
        tcp1_delay = 0
    else:
        tcp1_delay = tcp1_total_duration / tcp1_num_packets * 1000

    if tcp2_num_packets == 0:
        tcp2_delay = 0
    else:
        tcp2_delay = tcp2_total_duration / tcp2_num_packets * 1000

    return str(tcp1_delay) + '\t' + str(tcp2_delay)


# Generate trace file
for var in TCP_Variant2:
    for rate in range(1, 11):
        tcps = var.split('_')
        os.system(ns_command + "experiment2.tcl " + tcps[0] + " " + tcps[1] + " " + str(rate))

f11 = open('exp2_data/exp2_Reno_Reno_throughput.dat', 'w')
f12 = open('exp2_data/exp2_Reno_Reno_droprate.dat', 'w')
f13 = open('exp2_data/exp2_Reno_Reno_delay.dat', 'w')
f21 = open('exp2_data/exp2_Newreno_Reno_throughput.dat', 'w')
f22 = open('exp2_data/exp2_Newreno_Reno_droprate.dat', 'w')
f23 = open('exp2_data/exp2_Newreno_Reno_delay.dat', 'w')
f31 = open('exp2_data/exp2_Vegas_Vegas_throughput.dat', 'w')
f32 = open('exp2_data/exp2_Vegas_Vegas_droprate.dat', 'w')
f33 = open('exp2_data/exp2_Vegas_Vegas_delay.dat', 'w')
f41 = open('exp2_data/exp2_Newreno_Vegas_throughput.dat', 'w')
f42 = open('exp2_data/exp2_Newreno_Vegas_droprate.dat', 'w')
f43 = open('exp2_data/exp2_Newreno_Vegas_delay.dat', 'w')
for rate in range(1, 13):
    for var in TCP_Variant2:
        if var == 'Reno_Reno':
            f11.write(str(rate) + '\t' + get_throughput(var, rate) + '\n')
            f12.write(str(rate) + '\t' + get_drop_rate(var, rate) + '\n')
            f13.write(str(rate) + '\t' + getLatency(var, rate) + '\n')
        if var == 'Newreno_Reno':
            f21.write(str(rate) + '\t' + get_throughput(var, rate) + '\n')
            f22.write(str(rate) + '\t' + get_drop_rate(var, rate) + '\n')
            f23.write(str(rate) + '\t' + getLatency(var, rate) + '\n')
        if var == 'Vegas_Vegas':
            f31.write(str(rate) + '\t' + get_throughput(var, rate) + '\n')
            f32.write(str(rate) + '\t' + get_drop_rate(var, rate) + '\n')
            f33.write(str(rate) + '\t' + getLatency(var, rate) + '\n')
        if var == 'Newreno_Vegas':
            f41.write(str(rate) + '\t' + get_throughput(var, rate) + '\n')
            f42.write(str(rate) + '\t' + get_drop_rate(var, rate) + '\n')
            f43.write(str(rate) + '\t' + getLatency(var, rate) + '\n')

f11.close()
f12.close()
f13.close()
f21.close()
f22.close()
f23.close()
f31.close()
f32.close()
f33.close()
f41.close()
f42.close()
f43.close()
