# Creating a simulator
global s all_trace
set s [new Simulator]

# TCP variant
set tcp_var [lindex $argv 0]
# Queueing algorithm
set que_alg [lindex $argv 1]
# CBR BW
set cbr_rate 8

# Setting the trace file
set all_trace [open exp3_output/experiment3_${tcp_var}_${que_alg}.out w]
$s trace-all $all_trace

# Final end procedure to send all the trace log into a trace file
proc flush {} {
    global s nam_trace all_trace
    $s flush-trace
    close $all_trace
    puts "Success!!!!"
    exit
}

# Node creation
set n1 [$s node]
set n2 [$s node]
set n3 [$s node]
set n4 [$s node]
set n5 [$s node]
set n6 [$s node]

# Creating the links
$s duplex-link $n1 $n2 10Mb 10ms ${que_alg}
$s duplex-link $n2 $n3 10Mb 10ms ${que_alg}
$s duplex-link $n5 $n2 10Mb 10ms ${que_alg}
$s duplex-link $n6 $n3 10Mb 10ms ${que_alg}
$s duplex-link $n4 $n3 10Mb 10ms ${que_alg}

# Define queue limit
$s queue-limit	$n1 $n2 10
$s queue-limit	$n5 $n2 10
$s queue-limit	$n2 $n3 10
$s queue-limit	$n4 $n3 10
$s queue-limit	$n6 $n3 10

# Attaching a UDP to a node
set udp [new Agent/UDP]
$s attach-agent $n5 $udp
set null [new Agent/Null]
$s attach-agent $n6 $null
$s connect $udp $null

# Attaching CBR
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set rate_ ${cbr_rate}mb

# Adding a TCP sender module as Reno
if {$tcp_var eq "SACK" || $tcp_var eq "sack"} {
	set tcp [new Agent/TCP/Sack1]
	set sink [new Agent/TCPSink/Sack1]
} else {
	set tcp [new Agent/TCP/Reno]
}

# Direct traffic from n1 to sink at n4
$s attach-agent $n1 $tcp
set sink [new Agent/TCPSink]
$s attach-agent $n4 $sink
$s connect $tcp $sink

# Setup an FTP traffic generator on TCP
set ftp [new Application/FTP]
$ftp attach-agent $tcp

# Scheduling start and stop times
$s at 0 "$ftp start"
$s at 3 "$cbr start"
$s at 6 "$ftp stop"
$s at 6 "$cbr stop"

# Flush after end time to race file
$s at 6 "flush"

# Run the simulation
$s run
puts "Success!!"