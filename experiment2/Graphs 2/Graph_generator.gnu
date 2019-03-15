set term png
set output "exp2_NewReno_Reno_delay.png"
set title "Experienmnet 2 NewReno-Reno Latency"
set xlabel "CBR[Mbps]"
set ylabel "Delay[ms]"
set grid
set key left
plot 'Newreno_Reno_delay.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'NewReno',\
 'Newreno_Reno_delay.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'Reno'

set term png
set output "exp2_NewReno_Reno_droprate.png"
set title "Experienmnet 2 NewReno-Reno Drop Rate"
set xlabel "CBR[Mbps]"
set ylabel "Drop Rate"
set grid
set key left
plot 'Newreno_Reno_droprate.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'NewReno',\
 'Newreno_Reno_droprate.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'Reno'

set term png
set output "exp2_NewReno_Reno_throughput.png"
set title "Experienmnet 2 NewReno-Reno Throughtput"
set xlabel "CBR[Mbps]"
set ylabel "Throughput[Mbps]"
set grid
plot 'Newreno_Reno_throughput.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'NewReno',\
 'Newreno_Reno_throughput.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'Reno'

set term png
set output "exp2_NewReno_Vegas_delay.png"
set title "Experienmnet 2 NewReno-Vegas Latency"
set xlabel "CBR[Mbps]"
set ylabel "Delay[ms]"
set grid
set key left
plot 'Newreno_Vegas_delay.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'NewReno',\
 'Newreno_Vegas_delay.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'Vegas'

set term png
set output "exp2_NewReno_Vegas_droprate.png"
set title "Experienmnet 2 NewReno-Vegas Drop Rate"
set xlabel "CBR[Mbps]"
set ylabel "Drop Rate"
set grid
set key left
plot 'Newreno_Vegas_droprate.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'NewReno',\
 'Newreno_Vegas_droprate.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'Vegas'

set term png
set output "exp2_NewReno_Vegas_throughput.png"
set title "Experienmnet 2 NewReno-Vegas Throughtput"
set xlabel "CBR[Mbps]"
set ylabel "Throughput[Mbps]"
set grid
plot 'Newreno_Vegas_throughput.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'NewReno',\
 'Newreno_Vegas_throughput.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'Vegas'

set term png
set output "exp2_Reno_Reno_delay.png"
set title "Experienmnet 2 Reno-Reno Latency"
set xlabel "CBR[Mbps]"
set ylabel "Delay[ms]"
set grid
set key left
plot 'Reno_Reno_delay.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'Reno[1-4]',\
 'Reno_Reno_delay.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'Reno[5-6]'

set term png
set output "exp2_Reno_Reno_droprate.png"
set title "Experienmnet 2 Reno-Reno Drop Rate"
set xlabel "CBR[Mbps]"
set ylabel "Drop Rate"
set grid
set key left
plot 'Reno_Reno_droprate.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'Reno[1-4]',\
 'Reno_Reno_droprate.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'Reno[5-6]'

set term png
set output "exp2_Reno_Reno_throughput.png"
set title "Experienmnet 2 Reno-Reno Throughtput"
set xlabel "CBR[Mbps]"
set ylabel "Throughput[Mbps]"
set grid
plot 'Reno_Reno_throughput.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'Reno[1-4]',\
 'Reno_Reno_throughput.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'Reno[5-6]'

set term png
set output "exp2_Vegas_Vegas_delay.png"
set title "Experienmnet 2 Vegas-Vegas Latency"
set xlabel "CBR[Mbps]"
set ylabel "Delay[ms]"
set grid
set key left
plot 'Vegas_Vegas_delay.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'Vegas[1-4]',\
 'Vegas_Vegas_delay.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'Vegas[5-6]'

set term png
set output "exp2_Vegas_Vegas_droprate.png"
set title "Experienmnet 2 Vegas-Vegas Drop Rate"
set xlabel "CBR[Mbps]"
set ylabel "Drop Rate"
set grid
set key left
plot 'Vegas_Vegas_droprate.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'Vegas[1-4]',\
 'Vegas_Vegas_droprate.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'Vegas[5-6]'

set term png
set output "exp2_Vegas_Vegas_throughput.png"
set title "Experienmnet 2 Vegas-Vegas Throughtput"
set xlabel "CBR[Mbps]"
set ylabel "Throughput[Mbps]"
set grid
plot 'Vegas_Vegas_throughput.dat' using 2:3 with lp pt 2 lw 1 linecolor rgb "red" title 'Vegas[1-4]',\
 'Vegas_Vegas_throughput.dat' using 2:4 with lp pt 8 lw 1 lt 1 linecolor rgb "blue" title 'Vegas[5-6]'
