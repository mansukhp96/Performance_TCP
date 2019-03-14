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
for tcp_var in ['Reno/Reno', 'Newreno/Reno', 'Vegas/Vegas', 'Newreno/Vegas']:
    tcp_vars = tcp_var.split('/')
    for cbr_rate in range(1, 13):
        os.system("/course/cs4700f12/ns-allinone-2.35/bin/ns " + "experiment2.tcl " + tcp_vars[0] + " " + tcp_vars[
            1] + " " + str(cbr_rate))

# Data files used for graph generation.
f1 = open('exp2_data/2_Reno/Reno_throughput.dat', 'w')
f2 = open('exp2_data/2_Reno/Reno_droprate.dat', 'w')
f3 = open('exp2_data/2_Reno/Reno_latency.dat', 'w')
f4 = open('exp2_data/2_Newreno/Reno_throughput.dat', 'w')
f5 = open('exp2_data/2_Newreno/Reno_droprate.dat', 'w')
f6 = open('exp2_data/2_Newreno/Reno_latency.dat', 'w')
f7 = open('exp2_data/2_Vegas/Vegas_throughput.dat', 'w')
f8 = open('exp2_data/2_Vegas/Vegas_droprate.dat', 'w')
f9 = open('exp2_data/2_Vegas/Vegas_latency.dat', 'w')
f10 = open('exp2_data/2_Newreno/Vegas_throughput.dat', 'w')
f11 = open('exp2_data/2_Newreno/Vegas_droprate.dat', 'w')
f12 = open('exp2_data/2_Newreno/Vegas_latency.dat', 'w')

# CBR rate varying between 1 and 12mb until it reaches bottleneck capacity.
for cbr_rate in range(1, 13):
    throughput1 = ''
    droprate1 = ''
    latency = ''
    throughput2 = ''
    droprate2 = ''
    latency2 = ''

    for tcp_var in ['Tahoe', 'Reno', 'Newreno', 'Vegas']:
        # Open the throughput files for TCP variants and rates and calculate the throughput.
        filename = "exp1_output/experiment1_" + tcp_var + "_" + str(cbr_rate) + ".out"
        f = open(filename)
        lines = f.readlines()
        f.close()
        start_time1 = start_time2 = 10.0
        end_time1 = end_time2 = 0.0
        recvdSize1 = recvdSize2 = 0
        for line in lines:
            entry = C(line)
            if entry.packet_type in ['tcp', 'ack'] and entry.from_node == '0':
                # Calculate period of time to send packets from node 1.
                if entry.event_type == "+" and entry.from_node == "0":
                    if entry.time < start_time1:
                        start_time1 = entry.time
                # Calculate size of packets in that period.
                if entry.event_type == "r":
                    recvdSize1 += entry.packet_size * 8
                    end_time1 = entry.time
            if entry.packet_type in ['tcp', 'ack'] and entry.from_node == '4':
                # Calculate period of time to send packets from node 1.
                if entry.event_type == "+" and entry.from_node == "4":
                    if entry.time < start_time2:
                        start_time2 = entry.time
                # Calculate size of packets in that period.
                if entry.event_type == "r":
                    recvdSize2 += entry.packet_size * 8
                    end_time2 = entry.time
        # Final throughput data to be written into file.
        throughput1 = throughput1 + '\t' + str(recvdSize1 / (end_time1 - start_time1) / (1024 * 1024))
        throughput2 = throughput2 + '\t' + str(recvdSize2 / (end_time2 - start_time2) / (1024 * 1024))

        # Open the droprate files for TCP Variants and rates and calculate the droprate.
        filename = "exp1_output/experiment1_" + tcp_var + "_" + str(cbr_rate) + ".out"
        f = open(filename)
        lines = f.readlines()
        f.close()
        sendNum1 = recvdNum1 = 0
        sendNum2 = recvdNum2 = 0
        for line in lines:
            entry = C(line)
            # Packet type is tcp and it's acks within which we need to count sent - received / sent
            if entry.packet_type in ["tcp", "ack"] and entry.flow_id == '1':
                # Packets in the queue
                if entry.event_type == "+":
                    sendNum1 += 1
                # Packets received
                if entry.event_type == "r":
                    recvdNum1 += 1
            if entry.packet_type in ["tcp", "ack"] and entry.flow_id == '1':
                # Packets in the queue
                if entry.event_type == "+":
                    sendNum2 += 1
                # Packets received
                if entry.event_type == "r":
                    recvdNum2 += 1
        if sendNum1 == 0:
            droprate1 = '0'
        else:
            # Final droprate to be written into file.
            droprate1 = droprate1 + '\t' + str(float(sendNum1 - recvdNum1) / float(sendNum1))
        if sendNum2 == 0:
            droprate2 = '0'
        else:
            # Final droprate to be written into file.
            droprate2 = droprate2 + '\t' + str(float(sendNum2 - recvdNum2) / float(sendNum2))

        # Open the latency files for TCP Variants and rates and calculate the delay.
        filename = "exp1_output/experiment1_" + tcp_var + "_" + str(cbr_rate) + ".out"
        f = open(filename)
        lines = f.readlines()
        f.close()
        start_dict = {}
        end_dict = {}
        total_duration = 0.0
        num_packets = 0

        for line in lines:
            entry = C(line)
            if entry.packet_type in ["tcp", "ack"]:
                if entry.from_node == "0" and entry.event_type == "+":
                    # tracking start time of all packets originating from node 0 that are queueing
                    start_dict[entry.sequence_num] = entry.time
                elif entry.to_node == "0" and entry.event_type == "r":
                    # tracking end time of all packets returning ACKs at node 0
                    end_dict[entry.sequence_num] = entry.time

        for key in start_dict:
            if key in end_dict.keys():
                period = end_dict[key] - start_dict[key]
                if period > 0:
                    total_duration += period
                    num_packets += 1

        if num_packets == 0:
            latency = '0'
        # Final latency to be written into file.
        latency = latency + '\t' + str(total_duration / num_packets * 1000)

    f1.write("Rate: " + str(cbr_rate) + " Throughputs: " + throughput + '\n')
    f2.write("Rate: " + str(cbr_rate) + " Droprates: " + droprate + '\n')
    f3.write("Rate: " + str(cbr_rate) + " Latencies: " + latency + '\n')

f1.close()
f2.close()
f3.close()
