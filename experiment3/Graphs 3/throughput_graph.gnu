set term png
set output "exp3_Reno_Droptail_throughput.png"
set title "Experienmnet 3 Reno and DropTail Throughtput"
set xlabel "Time [Seconds]"
set ylabel "Throughput[Mbps]"
set grid
plot 'Reno_DropTail_throughput.dat' using 2:4 with lp pt 2 lw 1 linecolor rgb "red" title 'CBR',\
 'Reno_DropTail_throughput.dat' using 2:6 with lp pt 8 lw 1 lt 1 linecolor rgb "#blue" title 'TCP'

set term png
set output "exp3_Reno_RED_throughput.png"
set title "Experienmnet 3 Reno and RED Throughtput"
set xlabel "Time [Seconds]"
set ylabel "Throughput[Mbps]"
set grid
plot 'Reno_RED_throughput.dat' using 2:4 with lp pt 2 lw 1 linecolor rgb "red" title 'CBR',\
 'Reno_RED_throughput.dat' using 2:6 with lp pt 8 lw 1 lt 1 linecolor rgb "#blue" title 'TCP'

set term png
set output "exp3_SACK_Droptail_throughput.png"
set title "Experienmnet 3 SACK and DropTail Throughtput"
set xlabel "Time [Seconds]"
set ylabel "Throughput[Mbps]"
set grid
plot 'SACK_DropTail_throughput.dat' using 2:4 with lp pt 2 lw 1 linecolor rgb "red" title 'CBR',\
 'SACK_DropTail_throughput.dat' using 2:6 with lp pt 8 lw 1 lt 1 linecolor rgb "#blue" title 'TCP'

set term png
set output "exp3_SACK_RED_throughput.png"
set title "Experienmnet 3 SACK and RED Throughtput"
set xlabel "Time [Seconds]"
set ylabel "Throughput[Mbps]"
set grid
plot 'SACK_RED_throughput.dat' using 2:4 with lp pt 2 lw 1 linecolor rgb "red" title 'CBR',\
 'SACK_RED_throughput.dat' using 2:6 with lp pt 8 lw 1 lt 1 linecolor rgb "#blue" title 'TCP'
