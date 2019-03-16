set term png
set output "exp2_NewReno_Reno_delay.png"
set title "Exp:2 Latency of NEWRENO and RENO"
set xlabel "CBR RATE(Mbps)"
set ylabel "LATENCY(ms)"
set key left
plot 'Newreno_Reno_delay.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'NEWRENO',\
 'Newreno_Reno_delay.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'RENO'

set term png
set output "exp2_NewReno_Reno_droprate.png"
set title "Exp:2 Droprate of NEWRENO and RENO"
set xlabel "CBR RATE(Mbps)"
set ylabel "DROPRATE"
set key left
plot 'Newreno_Reno_droprate.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'NEWRENO',\
 'Newreno_Reno_droprate.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'RENO'

set term png
set output "exp2_NewReno_Reno_throughput.png"
set title "Exp:2 Throughtput of NEWRENO and RENO"
set xlabel "CBR RATE(Mbps)"
set ylabel "THROUGHPUT(Mbps)"
plot 'Newreno_Reno_throughput.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'NEWRENO',\
 'Newreno_Reno_throughput.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'RENO'

set term png
set output "exp2_NewReno_Vegas_delay.png"
set title "Exp:2 Latency of NEWRENO and VEGAS"
set xlabel "CBR RATE(Mbps)"
set ylabel "DELAY(ms)"
set key left
plot 'Newreno_Vegas_delay.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'NEWRENO',\
 'Newreno_Vegas_delay.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'VEGAS'

set term png
set output "exp2_NewReno_Vegas_droprate.png"
set title "Exp:2 Droprate of NEWRENO and VEGAS"
set xlabel "CBR RATE(Mbps)"
set ylabel "DROPRATE"
set key left
plot 'Newreno_Vegas_droprate.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'NEWRENO',\
 'Newreno_Vegas_droprate.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'VEGAS'

set term png
set output "exp2_NewReno_Vegas_throughput.png"
set title "Exp:2 Throughtput of NEWRENO and VEGAS"
set xlabel "CBR RATE(Mbps)"
set ylabel "THROUGHPUT(Mbps)"
plot 'Newreno_Vegas_throughput.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'NEWRENO',\
 'Newreno_Vegas_throughput.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'VEGAS'

set term png
set output "exp2_Reno_Reno_delay.png"
set title "Exp:2 Latency of RENO and RENO"
set xlabel "CBR RATE(Mbps)"
set ylabel "DELAY(ms)"
set key left
plot 'Reno_Reno_delay.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'RENO',\
 'Reno_Reno_delay.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'RENO'

set term png
set output "exp2_Reno_Reno_droprate.png"
set title "Exp:2 Drorate of RENO and RENO"
set xlabel "CBR RATE(Mbps)"
set ylabel "DROPRATE"
set key left
plot 'Reno_Reno_droprate.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'RENO',\
 'Reno_Reno_droprate.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'RENO'

set term png
set output "exp2_Reno_Reno_throughput.png"
set title "Exp:2 Throughtput of RENO and RENO"
set xlabel "CBR RATE(Mbps)"
set ylabel "THROUGHPUT(Mbps)"
plot 'Reno_Reno_throughput.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'RENO',\
 'Reno_Reno_throughput.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'RENO'

set term png
set output "exp2_Vegas_Vegas_delay.png"
set title "Exp:2 Latency of VEGAS and VEGAS"
set xlabel "CBR RATE(Mbps)"
set ylabel "DELAY(ms)"
set key left
plot 'Vegas_Vegas_delay.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'VEGAS',\
 'Vegas_Vegas_delay.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'VEGAS'

set term png
set output "exp2_Vegas_Vegas_droprate.png"
set title "Exp:2 Droprate of VEGAS and VEGAS"
set xlabel "CBR RATE(Mbps)"
set ylabel "DROPRATE"
set key left
plot 'Vegas_Vegas_droprate.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'VEGAS',\
 'Vegas_Vegas_droprate.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'VEGAS'

set term png
set output "exp2_Vegas_Vegas_throughput.png"
set title "Exp:2 Throughtput of VEGAS and VEGAS"
set xlabel "CBR RATE(Mbps)"
set ylabel "THROUGHPUT(Mbps)"
plot 'Vegas_Vegas_throughput.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'VEGAS',\
 'Vegas_Vegas_throughput.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'VEGAS'
