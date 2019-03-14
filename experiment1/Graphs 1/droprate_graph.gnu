set term png
set output "exp1_droprate.png"
set title "Experienmnet 1 Drop Rate"
set xlabel "CBR[Mbps]"
set ylabel "Drop Rate"
set grid
plot 'droprate.dat' using 2:4 with lp pt 4 lw 2 lt 2 linecolor rgb "green" title 'Tahoe',\
 'droprate.dat' using 2:5 with lp pt 4 lw 1 lt 2 linecolor rgb "purple" title 'Reno',\
 'droprate.dat' using 2:6 with lp pt 4 lw 1 lt 2 linecolor rgb "red" title 'NewReno',\
 'droprate.dat' using 2:7 with lp pt 4 lw 1 lt 2 linecolor rgb "blue" title 'Vegas'
