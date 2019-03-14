# Creating a simulator
global s all_trace
set s [new Simulator]

# TCP variant 1
set tcp_var1 [lindex $argv 0]
# TCP variant 2
set tcp_var2 [lindex $argv 1]
# CBR BW
set rate [lindex $argv 2]

# Setting the trace file
set all_trace [open exp2_output/experiment2_${tcp_var1}_${tcp_var2}_${rate}.out w]
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
$s duplex-link $n1 $n2 10Mb 10ms DropTail
$s duplex-link $n2 $n3 10Mb 10ms DropTail
$s duplex-link $n5 $n2 10Mb 10ms DropTail
$s duplex-link $n6 $n3 10Mb 10ms DropTail
$s duplex-link $n4 $n3 10Mb 10ms DropTail

# Attaching a UDP to a node
set udp [new Agent/UDP]
$s attach-agent $n2 $udp
set null [new Agent/Null]
$s attach-agent $n3 $null
$s connect $udp $null

# Attaching CBR
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set rate_ ${rate}mb

# Adding a TCP sender module (Reno/NewReno/Vegas)
if {$tcp_var1 eq "Reno" || $tcp_var1 eq "Vegas"} {
    set tcp1 [new Agent/TCP/$tcp_var1]
} else {
    set tcp1 [new Agent/TCP/Newreno]
}

# Direct traffic from n1 to sink at n4
$tcp1 set class_ 1
$s attach-agent $n1 $tcp1
set sink1 [new Agent/TCPSink]
$s attach-agent $n4 $sink1
$s connect $tcp1 $sink1

# Adding a TCP sender module (Reno/Vegas)
if {$tcp_var2 eq "Reno" || $tcp_var2 eq "Vegas"} {
    set tcp2 [new Agent/TCP/$tcp_var2]
}

# Direct traffic from n5 to sink at n6
$tcp2 set class_ 2
$s attach-agent $n5 $tcp2
set sink2 [new Agent/TCPSink]
$s attach-agent $n6 $sink2
$s connect $tcp2 $sink2

# Setup an FTP traffic generator on TCP
set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcp2

# Scheduling start and stop times
$s at 0 "$cbr start"
$s at 0 "$ftp1 start"
$s at 0 "$ftp2 start"
$s at 6 "$ftp1 stop"
$s at 6 "$ftp2 stop"
$s at 6 "$cbr stop"

# Flush after end time to race file
$s at 6 "flush"

# Run the simulation
$s run
puts "Success!!!!"
