set term png
set output "exp1_delay.png"
set title "Experienmnet 1 Latency"
set xlabel "CBR[Mbps]"
set ylabel "Latency[ms]"
set grid
plot 'latency.dat' using 2:4 with lp pt 2 lw 1 linecolor rgb "red" title 'Tahoe',\
 'latency.dat' using 2:5 with lp pt 8 lw 1 lt 1 linecolor rgb "#006400" title 'Reno',\
 'latency.dat' using 2:6 with lp pt 3 lw 1 lt 1 linecolor rgb "#FF8C00" title 'NewReno',\
 'latency.dat' using 2:7 with lp pt 4 lw 1 lt 1 linecolor rgb "blue" title 'Vegas'
