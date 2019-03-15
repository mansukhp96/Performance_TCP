# Start here for latency exp 2
# TODO -- add trace file path to open
filename = ""
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
    entry = C(line)

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

# TODO -- you now have both TCP flow's delay
