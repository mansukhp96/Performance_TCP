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
        self.sequence_num = contents[10]


# Generate trace file
for tcp_var in ['Tahoe', 'Reno', 'Newreno', 'Vegas']:
    for cbr_rate in range(1, 13):
        os.system("/course/cs4700f12/ns-allinone-2.35/bin/ns " + "experiment1.tcl " + tcp_var + " " + str(cbr_rate))

# Data files used for graph generation.
f1 = open('exp1_data/1_throughput.dat', 'w')
f2 = open('exp1_data/1_droprate.dat', 'w')
f3 = open('exp1_data/1_latency.dat', 'w')

# CBR rate varying between 1 and 12mb until it reaches bottleneck capacity.
for cbr_rate in range(1, 13):
    throughput = ''
    droprate = ''
    latency = ''

    for tcp_var in ['Tahoe', 'Reno', 'Newreno', 'Vegas']:
        # Open the throughput files for TCP variants and rates and calculate the throughput.
        filename = "exp1_output/experiment1_" + tcp_var + "_" + str(cbr_rate) + ".out"
        f = open(filename)
        lines = f.readlines()
        f.close()
        start_time = 10.0
        end_time = 0.0
        recvdSize = 0
        for line in lines:
            entry = C(line)
            # Packet type should be tcp since we are calculating the throughput for TCP variants.
            if entry.packet_type in ['tcp', 'ack']:
                # Calculate period of time to send packets from node 1.
                if entry.event_type == "+" and entry.from_node == "0":
                    if entry.time < start_time:
                        start_time = entry.time
                # Calculate size of packets in that period.
                if entry.event_type == "r" and entry.to_node == '3':
                    recvdSize += entry.packet_size * 8
                    end_time = entry.time
        # Final throughput data to be written into file.
        throughput = throughput + '\t' + str(recvdSize / (end_time - start_time) / (1024 * 1024))

        # Open the droprate files for TCP Variants and rates and calculate the droprate.
        filename = "exp1_output/experiment1_" + tcp_var + "_" + str(cbr_rate) + ".out"
        f = open(filename)
        lines = f.readlines()
        f.close()
        sendNum = 0
        recvdNum = 0
        for line in lines:
            entry = C(line)
            # Packet type is tcp and it's acks within which we need to count sent - received / sent
            if entry.packet_type in ["tcp", "ack"]:
                # Packets in the queue
                if entry.event_type == "+":
                    sendNum += 1
                # Packets received
                if entry.event_type == "r":
                    recvdNum += 1
        if sendNum == 0:
            droprate = '0'
        else:
            # Final droprate to be written into file.
            droprate = droprate + '\t' + str(float(sendNum - recvdNum) / float(sendNum))

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
            # Calculate the latency
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

    # Writing into the files finally to be used for generating graphs.
    f1.write("Rate: " + str(cbr_rate) + " Throughputs: " + throughput + '\n')
    f2.write("Rate: " + str(cbr_rate) + " Droprates: " + droprate + '\n')
    f3.write("Rate: " + str(cbr_rate) + " Latencies: " + latency + '\n')

f1.close()
f2.close()
f3.close()
