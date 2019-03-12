#Creating a simulator
global s all_trace
set s [new Simulator]

#Taking the TCP Variant and CBR BW as parameter
set var [lindex $argv 0]
set rate [lindex $argv 1]

#Setting the trace file
set all_trace [open exp1_output/experiment1${var}_${rate}.out w]
$s trace-all $all_trace

#Final end procedure to send all the trace log into a trace file
proc flush {} {
    global s nam_trace all_trace
    $s flush-trace
    close $all_trace
    exit
}

#Node creation
set n1 [$s node]
set n2 [$s node]
set n3 [$s node]
set n4 [$s node]
set n5 [$s node]
set n6 [$s node]

#Creating the links
$s duplex-link $n1 $n2 10Mb 10ms DropTail
$s duplex-link $n2 $n3 10Mb 10ms DropTail
$s duplex-link $n5 $n2 10Mb 10ms DropTail
$s duplex-link $n6 $n3 10Mb 10ms DropTail
$s duplex-link $n4 $n3 10Mb 10ms DropTail

#Attaching a UDP to a node
set udp [new Agent/UDP]
$s attach-agent $n2 $udp
set null [new Agent/Null]
$s attach-agent $n3 $null
$s connect $udp $null

#Attaching CBR
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set rate_ ${rate}mb

#Adding a TCP sender module
if {$var eq "Tahoe"} {
	set tcp [new Agent/TCP]
} else {
	set tcp [new Agent/TCP/$var]
}

#Direct traffic from n1 to sink at n4
$s attach-agent $n1 $tcp
set sink [new Agent/TCPSink]
$s attach-agent $n4 $sink
$s connect $tcp $sink

#Setup an FTP traffic generator on tcp
set ftp [new Application/FTP]
$ftp attach-agent $tcp

#Scheduling start and stop times
$s at 0 "$cbr start"
$s at 0 "$ftp start"
$s at 6 "$ftp stop"
$s at 6 "$cbr stop"

#Flush after end time to race file.
$s at 6 "flush"

#Run the simulation
$s run