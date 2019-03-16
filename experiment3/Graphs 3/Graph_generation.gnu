set term png
set output "exp3_Reno_Droptail_throughput.png"
set title "Exp:3 Reno and DropTail Throughtput"
set xlabel "TIME (s)"
set ylabel "THROUGHPUT(Mbps)"
plot 'Reno_DropTail_throughput.dat' using 2:4 with lp pt 2 lw 2 linecolor rgb "red" title 'CBR',\
 'Reno_DropTail_throughput.dat' using 2:6 with lp pt 3 lw 1 lt 2 linecolor rgb "blue" title 'TCP'

set term png
set output "exp3_Reno_RED_throughput.png"
set title "Exp:3 Reno and RED Throughtput"
set xlabel "TIME (s)"
set ylabel "THROUGHPUT(Mbps)"
plot 'Reno_RED_throughput.dat' using 2:4 with lp pt 2 lw 2 linecolor rgb "red" title 'CBR',\
 'Reno_RED_throughput.dat' using 2:6 with lp pt 3 lw 1 lt 2 linecolor rgb "blue" title 'TCP'

set term png
set output "exp3_SACK_Droptail_throughput.png"
set title "Exp:3 SACK and DropTail Throughtput"
set xlabel "TIME (s)"
set ylabel "THROUGHPUT(Mbps)"
plot 'SACK_DropTail_throughput.dat' using 2:4 with lp pt 2 lw 2 linecolor rgb "red" title 'CBR',\
 'SACK_DropTail_throughput.dat' using 2:6 with lp pt 3 lw 1 lt 2 linecolor rgb "blue" title 'TCP'

set term png
set output "exp3_SACK_RED_throughput.png"
set title "Exp:3 SACK and RED Throughtput"
set xlabel "TIME (s)"
set ylabel "THROUGHPUT(Mbps)"
plot 'SACK_RED_throughput.dat' using 2:4 with lp pt 2 lw 2 linecolor rgb "red" title 'CBR',\
 'SACK_RED_throughput.dat' using 2:6 with lp pt 3 lw 1 lt 2 linecolor rgb "blue" title 'TCP'

set term png
set output "exp3_Reno_latency.png"
set title "Exp:3 Reno Latency"
set xlabel "TIME(s)"
set ylabel "LATENCY(ms)"
plot 'Reno_RED_latency.dat' using 2:6 with lp pt 2 lw 2 linecolor rgb "red" title 'RED',\
 'Reno_DropTail_latency.dat' using 2:6 with lp pt 3 lw 1 lt 2 linecolor rgb "blue" title 'DropTail'

set term png
set output "exp3_SACK_latency.png"
set title "Exp:3 SACK Latency"
set xlabel "TIME(s)"
set ylabel "LATENCY(ms)"
plot 'SACK_RED_latency.dat' using 2:6 with lp pt 2 lw 2 linecolor rgb "red" title 'RED',\
 'SACK_DropTail_latency.dat' using 2:6 with lp pt 3 lw 1 lt 2 linecolor rgb "blue" title 'DropTail'
