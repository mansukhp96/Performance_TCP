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
        os.system("/course/cs4700f12/ns-allinone-2.35/bin/ns " + "experiment3.tcl " + str(tcp_var) + " " + str(que_alg))

# f1 = open("exp3_output/experiment3_Reno_Droptail_throughput.out")
# f2 = open("exp3_output/experiment3_Reno_RED_throughput.out")
# f3 = open("exp3_output/experiment3_SACK_Droptail_throughput.out")
# f4 = open("exp3_output/experiment3_SACK_RED_throughput.out")
# f5 = open("exp3_output/experiment3_Reno_DropTail_latency.out")
# f6 = open("exp3_output/experiment3_Reno_RED_latency.out")
# f7 = open("exp3_output/experiment3_SACK_DropTail_latency.out")
# f8 = open("exp3_output/experiment3_SACK_RED_latency.out")

# TODO -- shouldn't the opening and closing of throughput and latency files be outside the for loop?

for que_alg in ['DropTail', 'RED']:
    for tcp_var in ['Reno', 'SACK']:
        # Open the throughput files for TCP variants and rates and calculate the throughput.
        filename = "exp3_output/experiment3_" + str(tcp_var) + "_" + str(que_alg) + ".out"
        tcl_file = open(filename)
        lines = tcl_file.readlines()
        tcl_file.close()
        # Start here for throughput exp3
        log_period = 0
        tcp_recvdPacketSize = 0
        cbr_recvdPacketSize = 0
        # TODO -- set the appropriate file path
        throughput = open('exp3_data/3_' + str(tcp_var) + '_' + str(que_alg) + '_throughput.dat', 'w')
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
                throughput.write(
                    "time: " + str(log_period) + " CBR: " + str(cbr_throughput) + " TCP: " + str(tcp_throughput) + '\n')
                log_period += 1
                # TODO -- generate graph for both conditions: resetting the recvdPacketSizes to zero and remaining unchanged
                tcp_recvdPacketSize = 0
                cbr_recvdPacketSize = 0

        throughput.close()
        # throughput END

        # Droprate
        filename = "exp3_output/experiment3_" + str(tcp_var) + "_" + str(que_alg) + ".out"
        f = open(filename)
        lines = f.readlines()
        f.close()
        log_period = 0
        sendNum = 0
        recvdNum = 0
        sendNum1 = 0
        recvdNum1 = 0
        dropratef = open('exp3_data/3_' + str(tcp_var) + '_' + str(que_alg) + '_droprate.dat', 'w')
        for line in lines:
            entry = C(line)
            # Packet type is tcp and it's acks within which we need to count sent - received / sent
            if entry.pkt_type in ['tcp', 'ack']:
                # Packets in the queue
                if entry.event == "+":
                    sendNum += 1
                # Packets received
                if entry.event == "r":
                    recvdNum += 1
            if entry.pkt_type == 'cbr':
                # Packets in the queue
                if entry.event == "+":
                    sendNum1 += 1
                # Packets received
                if entry.event == "r":
                    recvdNum1 += 1
            if entry.time - log_period > 1:
                if sendNum == 0:
                    droprate = 0
                else:
                    droprate = float(sendNum - recvdNum) / float(sendNum)
                if sendNum1 == 0:
                    droprate1 = 0
                else:
                    droprate1 = float(sendNum1 - recvdNum1) / float(sendNum1)
                dropratef.write(
                    "time: " + str(log_period) + " CBR: " + str(droprate1) + " TCP: " + str(droprate) + '\n')
                log_period += 1
                sendNum = 0
                recvdNum = 0
                sendNum1 = 0
                recvdNum1 = 0
                droprate = 0
                droprate1 = 0

        dropratef.close()

        # Open the latency files for TCP Variants and rates and calculate the delay.
        filename = "exp3_output/experiment3_" + str(tcp_var) + "_" + str(que_alg) + ".out"
        tcl_file = open(filename)
        lines = tcl_file.readlines()
        tcl_file.close()
        # Start here for latency exp3
        log_period = 0
        # TODO -- set the appropriate file path
        latency = open('exp3_data/3_' + str(tcp_var) + '_' + str(que_alg) + '_latency.dat', 'w')

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
                    cbr_start_dict[entry.seq_num] = entry.time
                elif entry.to_node == "5" and entry.event == "r":
                    # tracking end time of all packets (CBR traffic) received at node 6
                    cbr_end_dict[entry.seq_num] = entry.time

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
                latency.write("time: " + str(log_period) + " CBR: " + str(cbr_delay) + " TCP: " + str(tcp_delay) + '\n')
                # TODO -- generate graph for both conditions: resetting the recvdPacketSizes to zero and remaining unchanged
                log_period += 1
                tcp_start_dict = {}
                tcp_end_dict = {}
                tcp_total_duration = 0.0
                tcp_num_packets = 0
                cbr_start_dict = {}
                cbr_end_dict = {}
                cbr_total_duration = 0.0
                cbr_num_packets = 0

        latency.close()
