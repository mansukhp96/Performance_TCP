#!/usr/bin/env python

import os


class Record:
    def __init__(self, line):
        contents = line.split()
        self.event_type = contents[0]
        self.time = float(contents[1])
        self.from_node = contents[2]
        self.to_node = contents[3]
        self.packet_type = contents[4]
        self.packet_size = int(contents[5])
        self.flow_id = contents[7]
        self.sequence_num = contents[10]


# Generate trace file
for var in ['Reno&Reno', 'Newreno&Reno', 'Vegas&Vegas', 'Newreno&Vegas']:
    for cbr_rate in range(1, 13):
        TCP_vars = var.split('&')
        os.system(
            "/course/cs4700f12/ns-allinone-2.35/bin/ns " + "experiment2.tcl " + TCP_vars[0] + " " + TCP_vars[
                1] + " " + str(cbr_rate))

f1 = open('exp2_data/exp2_Reno&Reno_throughput.dat', 'w')
f2 = open('exp2_data/exp2_Reno&Reno_droprate.dat', 'w')
f3 = open('exp2_data/exp2_Reno&Reno_delay.dat', 'w')
f4 = open('exp2_data/exp2_Newreno&Reno_throughput.dat', 'w')
f5 = open('exp2_data/exp2_Newreno&Reno_droprate.dat', 'w')
f6 = open('exp2_data/exp2_Newreno&Reno_delay.dat', 'w')
f7 = open('exp2_data/exp2_Vegas&Vegas_throughput.dat', 'w')
f8 = open('exp2_data/exp2_Vegas&Vegas_droprate.dat', 'w')
f9 = open('exp2_data/exp2_Vegas&Vegas_delay.dat', 'w')
f10 = open('exp2_data/exp2_Newreno&Vegas_throughput.dat', 'w')
f11 = open('exp2_data/exp2_Newreno&Vegas_droprate.dat', 'w')
f12 = open('exp2_data/exp2_Newreno&Vegas_delay.dat', 'w')

for cbr_rate in range(1, 13):
    for var in ['Reno&Reno', 'Newreno&Reno', 'Vegas&Vegas', 'Newreno&Vegas']:

        # thrput
        filename = "exp2_output/experiment2_" + str(var) + "_" + str(cbr_rate) + ".out"
        f = open(filename)
        lines = f.readlines()
        f.close()
        # Set counters
        start_time1 = start_time2 = 10.0
        end_time1 = end_time2 = 0.0
        recvdSize1 = recvdSize2 = 0

        for line in lines:
            entry = Record(line)
            if entry.flow_id == "1":  # TCP stream from 1 to 4
                if entry.event_type == "+" and entry.from_node == "0":
                    if entry.time < start_time1:
                        start_time1 = entry.time
                if entry.event_type == "r":
                    recvdSize1 += entry.packet_size * 8
                    end_time1 = entry.time
            if entry.flow_id == "2":  # TCP stream from 5 to 6
                if entry.event_type == "+" and entry.from_node == "4":
                    if entry.time < start_time2:
                        start_time2 = entry.time
                if entry.event_type == "r":
                    recvdSize2 += entry.packet_size * 8
                    end_time2 = entry.time

                    # print('DEBUG:' + str(recvdSize) + ' ' + str(end_time) + ' ' + str(start_time))
        th1 = recvdSize1 / (end_time1 - start_time1) / (1024 * 1024)
        th2 = recvdSize2 / (end_time2 - start_time2) / (1024 * 1024)

        # droprate
        filename = "exp2_output/experiment2_" + str(var) + "_" + str(cbr_rate) + ".out"
        f = open(filename)
        lines = f.readlines()
        f.close()

        sendNum1 = recvdNum1 = 0
        sendNum2 = recvdNum2 = 0

        for line in lines:
            entry = Record(line)
            if entry.flow_id == "1":
                if entry.event_type == "+":
                    sendNum1 += 1
                if entry.event_type == "r":
                    recvdNum1 += 1
            if entry.flow_id == "2":
                if entry.event_type == "+":
                    sendNum2 += 1
                if entry.event_type == "r":
                    recvdNum2 += 1

        dr1 = 0 if sendNum1 == 0 else float(sendNum1 - recvdNum1) / float(sendNum1)
        dr2 = 0 if sendNum2 == 0 else float(sendNum2 - recvdNum2) / float(sendNum2)

        # latency
        filename = "exp2_output/experiment2_" + str(var) + "_" + str(cbr_rate) + ".out"
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

        if var == 'Reno&Reno':
            f1.write(str(cbr_rate) + ' ' + str(th1) + ' ' + str(th2) + '\n')
            f2.write(str(cbr_rate) + ' ' + str(dr1) + ' ' + str(dr2) + '\n')
            f3.write(str(cbr_rate) + ' ' + str(tcp1_delay) + ' ' + str(tcp2_delay) + '\n')
        elif var == 'Newreno&Reno':
            f4.write(str(cbr_rate) + ' ' + str(th1) + ' ' + str(th2) + '\n')
            f5.write(str(cbr_rate) + ' ' + str(dr1) + ' ' + str(dr2) + '\n')
            f6.write(str(cbr_rate) + ' ' + str(tcp1_delay) + ' ' + str(tcp2_delay) + '\n')
        elif var == 'Vegas&Vegas':
            f7.write(str(cbr_rate) + ' ' + str(th1) + ' ' + str(th2) + '\n')
            f8.write(str(cbr_rate) + ' ' + str(dr1) + ' ' + str(dr2) + '\n')
            f9.write(str(cbr_rate) + ' ' + str(tcp1_delay) + ' ' + str(tcp2_delay) + '\n')
        elif var == 'Newreno&Vegas':
            f10.write(str(cbr_rate) + ' ' + str(th1) + ' ' + str(th2) + '\n')
            f11.write(str(cbr_rate) + ' ' + str(dr1) + ' ' + str(dr2) + '\n')
            f12.write(str(cbr_rate) + ' ' + str(tcp1_delay) + ' ' + str(tcp2_delay) + '\n')

f1.close()
f2.close()
f3.close()
f4.close()
f5.close()
f6.close()
f7.close()
f8.close()
f9.close()
f10.close()
f11.close()
f12.close()
