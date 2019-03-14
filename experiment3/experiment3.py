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
        tcl_file = open(filename)
        lines = tcl_file.readlines()
        tcl_file.close()
        # Start here for throughput exp3
        log_period = 0
        tcp_recvdPacketSize = 0
        cbr_recvdPacketSize = 0
        # TODO -- set the appropriate file path
        throughput = open('TODO')
        for line in lines:
            entry = C(line)
            # tracking the TCP flow to monitor total packets received
            if entry.pkt_type in ['tcp', 'ack']:
                if entry.event == "r":
                    tcp_recvdPacketSize += entry.pkt_size * 8
            # tracking the CBR flow to monitor total packets received
            if entry.pkt_type == "cbr":
                # considering only the packets being received at node 6
                if entry.event == "r" and entry.to_node == "5":
                    cbr_recvdPacketSize += entry.pkt_size * 8

            # using log_period to only write data to the throughput file after an interval of 1 sec
            if entry.time - log_period > 1:
                tcp_throughput = tcp_recvdPacketSize / (1024 * 1024)
                cbr_throughput = cbr_recvdPacketSize / (1024 * 1024)
                # TODO -- write into file with some format
                throughput.write("TODO")
                log_period += 1
                # TODO -- generate graph for both conditions: resetting the recvdPacketSizes to zero and remaining unchanged

        throughput.close()
        # throughput END

        # Open the latency files for TCP Variants and rates and calculate the delay.
        filename = "exp3_output/experiment3_" + tcp_var + "_" + str(que_alg) + ".out"
        tcl_file = open(filename)
        lines = tcl_file.readlines()
        tcl_file.close()
        # Start here for latency exp3
        log_period = 0
        # TODO -- set the appropriate file path
        latency = open('TODO')

        tcp_start_dict = {}
        tcp_end_dict = {}
        tcp_total_duration = 0.0
        tcp_num_packets = 0

        cbr_start_dict = {}
        cbr_end_dict = {}
        cbr_total_duration = 0.0
        cbr_num_packets = 0

        for line in lines:
            entry = C(line)

            # tracking the TCP flow to monitor start and end time of packets with unique sequence ID
            if entry.pkt_type in ["tcp", "ack"]:
                if entry.from_node == "0" and entry.event == "+":
                    # tracking start time of all packets originating from node 1 that are queueing
                    tcp_start_dict[entry.seq_num] = entry.time
                elif entry.to_node == "0" and entry.event == "r":
                    # tracking end time of all packets returning ACKs at node 1
                    tcp_end_dict[entry.seq_num] = entry.time

            # tracking the CBR flow to monitor start and end time of packets with unique sequence ID
            if entry.pkt_type == "cbr":
                if entry.from_node == "4" and entry.event == "+":
                    # tracking start time of all packets (CBR traffic) originating from node 5 that are queueing
                    tcp_start_dict[entry.seq_num] = entry.time
                elif entry.to_node == "5" and entry.event == "r":
                    # tracking end time of all packets (CBR traffic) received at node 6
                    tcp_end_dict[entry.seq_num] = entry.time

            # using log_period to only write data to the latency file after an interval of 1 sec
            if entry.time - log_period > 1:

                # total duration and number of packets for the TCP flow
                for key in tcp_start_dict:
                    if key in tcp_end_dict.keys():
                        period = tcp_end_dict[key] - tcp_start_dict[key]
                        if period > 0:
                            tcp_total_duration += period
                            tcp_num_packets += 1

                # total duration and number of packets for the CBR flow
                for key in cbr_start_dict:
                    if key in cbr_end_dict.keys():
                        period = cbr_end_dict[key] - cbr_start_dict[key]
                        if period > 0:
                            cbr_total_duration += period
                            cbr_num_packets += 1

                if tcp_num_packets == 0:
                    tcp_delay = 0
                else:
                    tcp_delay = tcp_total_duration / tcp_num_packets * 1000

                if cbr_num_packets == 0:
                    cbr_delay = 0
                else:
                    cbr_delay = cbr_total_duration / cbr_num_packets * 1000

                # TODO -- write into file with some format
                latency.write("TODO")
                # TODO -- generate graph for both conditions: resetting the recvdPacketSizes to zero and remaining unchanged

        latency.close()

    f1.write("Algorithm: " + str(que_alg) + " Throughputs: " + str_throughput + '\n')
    f3.write("Algorithm: " + str(que_alg) + " Latencies: " + str_latency + '\n')

f1.close()
f3.close()
