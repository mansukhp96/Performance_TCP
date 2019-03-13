set term png
set output "exp1_throughput.png"
set title "Experienmnet 1 Throughtput"
set xlabel "CBR[Mbps]"
set ylabel "Throughput[Mbps]"
set grid
plot 'throughput.dat' using 2:4 with lp pt 2 lw 1 linecolor rgb "red" title 'Tahoe',\
 'throughput.dat' using 2:5 with lp pt 8 lw 1 lt 1 linecolor rgb "#006400" title 'Reno',\
 'throughput.dat' using 2:6 with lp pt 3 lw 1 lt 1 linecolor rgb "#FF8C00" title 'NewReno',\
 'throughput.dat' using 2:7 with lp pt 4 lw 1 lt 1 linecolor rgb "blue" title 'Vegas'
