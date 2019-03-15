#!/usr/bin/env python

import os


# Getting all the data from the trace file into variables.
class C:
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

# Opening all the data files to be used for generating graphs.
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

# Varying CBR rate from 1 to 12 until bottleneck capacity.
for cbr_rate in range(1, 13):
    for var in ['Reno&Reno', 'Newreno&Reno', 'Vegas&Vegas', 'Newreno&Vegas']:

        # Throughput of the two variants of TCP
        filename = "exp2_output/experiment2_" + str(var) + "_" + str(cbr_rate) + ".out"
        f = open(filename)
        lines = f.readlines()
        f.close()
        # Initialise counts
        begin1 = begin2 = 10.0
        end1 = end2 = 0.0
        received1 = received2 = 0
        for line in lines:
            entry = C(line)
            if entry.flow_id == "1":  # TCP stream for first TCP variant
                if entry.event_type == "+" and entry.from_node == "0":
                    if entry.time < begin1:
                        begin1 = entry.time
                if entry.event_type == "r":
                    received1 += entry.packet_size * 8
                    end1 = entry.time
            if entry.flow_id == "2":  # TCP stream for second TCP variant
                if entry.event_type == "+" and entry.from_node == "4":
                    if entry.time < begin2:
                        begin2 = entry.time
                if entry.event_type == "r":
                    received2 += entry.packet_size * 8
                    end2 = entry.time

        # Throughputs of the two TCP variants.
        throughput1 = received1 / (end1 - begin1) / (1024 * 1024)
        throughput2 = received2 / (end2 - begin2) / (1024 * 1024)

        # Droprate of the two TCP variants for CBR rate from 1 to 12
        filename = "exp2_output/experiment2_" + str(var) + "_" + str(cbr_rate) + ".out"
        f = open(filename)
        lines = f.readlines()
        f.close()
        # Initialise the counters.
        scount1 = rcount1 = 0
        scount2 = rcount2 = 0

        for line in lines:
            entry = C(line)
            if entry.flow_id == "1":  # First TCP variant
                if entry.event_type == "+":
                    scount1 += 1
                if entry.event_type == "r":
                    rcount1 += 1
            if entry.flow_id == "2":  # Second TCP variant
                if entry.event_type == "+":
                    scount2 += 1
                if entry.event_type == "r":
                    rcount2 += 1

        if scount1 == 0:
            droprate1 = 0
        else:
            # Droprate for first TCP variant
            droprate1 = float(scount1 - rcount1) / float(scount1)

        if scount2 == 0:
            droprate2 = 0
        else:
            # Droprate for second TCP variant
            droprate2 = float(scount1 - rcount1) / float(scount1)

        # Latency of the two TCP variants with varying CBR rate.
        filename = "exp2_output/experiment2_" + str(var) + "_" + str(cbr_rate) + ".out"
        tcl_file = open(filename)
        lines = tcl_file.readlines()
        tcl_file.close()

        # Using dictionary to store the durations
        tcp1_start_dict = {}
        tcp1_end_dict = {}
        tcp1_total_duration = 0.0
        tcp1_num_packets = 0

        tcp2_start_dict = {}
        tcp2_end_dict = {}
        tcp2_total_duration = 0.0
        tcp2_num_packets = 0

        for line in lines:
            entry = C(line)

            # latency calculation for first TCP variant
            if entry.flow_id == "1":
                if entry.from_node == "0" and entry.event_type == "+":
                    # tracking start time of all packets originating from node 0 for the first TCP flow that are
                    # queueing
                    tcp1_start_dict[entry.sequence_num] = entry.time
                elif entry.to_node == "0" and entry.event_type == "r":
                    # tracking end time of all packets returning ACKs at node 0 for the first TCP flow
                    tcp1_end_dict[entry.sequence_num] = entry.time
            # latency calculation for second TCP variant
            if entry.flow_id == "2":
                if entry.from_node == "4" and entry.event_type == "+":
                    # tracking start time of all packets originating from node 0 for the second TCP flow that are
                    # queueing
                    tcp2_start_dict[entry.sequence_num] = entry.time
                elif entry.to_node == "4" and entry.event_type == "r":
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

        # Writing to final files based on the TCP combination compared.
        if var == 'Reno&Reno':
            f1.write("Rate: " + str(cbr_rate) + ' ' + str(throughput1) + ' ' + str(throughput2) + '\n')
            f2.write("Rate: " + str(cbr_rate) + ' ' + str(droprate1) + ' ' + str(droprate2) + '\n')
            f3.write("Rate: " + str(cbr_rate) + ' ' + str(tcp1_delay) + ' ' + str(tcp2_delay) + '\n')
        elif var == 'Newreno&Reno':
            f4.write("Rate: " + str(cbr_rate) + ' ' + str(throughput1) + ' ' + str(throughput2) + '\n')
            f5.write("Rate: " + str(cbr_rate) + ' ' + str(droprate1) + ' ' + str(droprate2) + '\n')
            f6.write("Rate: " + str(cbr_rate) + ' ' + str(tcp1_delay) + ' ' + str(tcp2_delay) + '\n')
        elif var == 'Vegas&Vegas':
            f7.write("Rate: " + str(cbr_rate) + ' ' + str(throughput1) + ' ' + str(throughput2) + '\n')
            f8.write("Rate: " + str(cbr_rate) + ' ' + str(droprate1) + ' ' + str(droprate2) + '\n')
            f9.write("Rate: " + str(cbr_rate) + ' ' + str(tcp1_delay) + ' ' + str(tcp2_delay) + '\n')
        elif var == 'Newreno&Vegas':
            f10.write("Rate: " + str(cbr_rate) + ' ' + str(throughput1) + ' ' + str(throughput2) + '\n')
            f11.write("Rate: " + str(cbr_rate) + ' ' + str(droprate1) + ' ' + str(droprate2) + '\n')
            f12.write("Rate: " + str(cbr_rate) + ' ' + str(tcp1_delay) + ' ' + str(tcp2_delay) + '\n')

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
