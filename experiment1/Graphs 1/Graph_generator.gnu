set term png
set output "exp1_throughput.png"
set title "Exp1: Throughput of TCP Variants"
set xlabel "CBR RATE(Mbps)"
set ylabel "THROUGHPUT(Mbps)"
plot 'throughput.dat' using 2:4 with lp pt 2 lw 1 linecolor rgb "red" title 'TAHOE',\
 'throughput.dat' using 2:5 with lp pt 8 lw 1 lt 1 linecolor rgb "#006400" title 'RENO',\
 'throughput.dat' using 2:6 with lp pt 3 lw 1 lt 1 linecolor rgb "#FF8C00" title 'NEWRENO',\
 'throughput.dat' using 2:7 with lp pt 4 lw 1 lt 1 linecolor rgb "blue" title 'VEGAS'

set term png
set output "exp1_droprate.png"
set title "Exp1: Droprate of TCP Variants"
set xlabel "CBR RATE(Mbps)"
set ylabel "DROPRATE(packets)"
plot 'droprate.dat' using 2:4 with lp pt 4 lw 2 lt 2 linecolor rgb "green" title 'TAHOE',\
 'droprate.dat' using 2:5 with lp pt 4 lw 1 lt 2 linecolor rgb "purple" title 'RENO',\
 'droprate.dat' using 2:6 with lp pt 4 lw 1 lt 2 linecolor rgb "red" title 'NEWRENO',\
 'droprate.dat' using 2:7 with lp pt 4 lw 1 lt 2 linecolor rgb "blue" title 'VEGAS'

set term png
set output "exp1_delay.png"
set title "Exp1: Latency of TCP variants"
set xlabel "CBR RATE(Mbps)"
set ylabel "LATENCY(ms)"
plot 'latency.dat' using 2:4 with lp pt 2 lw 1 linecolor rgb "red" title 'Tahoe',\
 'latency.dat' using 2:5 with lp pt 8 lw 1 lt 1 linecolor rgb "#006400" title 'Reno',\
 'latency.dat' using 2:6 with lp pt 3 lw 1 lt 1 linecolor rgb "#FF8C00" title 'NewReno',\
 'latency.dat' using 2:7 with lp pt 4 lw 1 lt 1 linecolor rgb "blue" title 'Vegas'
