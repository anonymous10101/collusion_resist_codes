set term postscript eps size 3.5,2.62 font 'Times, 24
set output 'img_tk.eps'

set xtics 200
set xlabel 'Number of users'
set ylabel 'Size of the least Tk'

set key off
set multiplot
plot 'privacy_dis.txt' using 1:2:3  w boxerror

unset multiplot

set term x11
set output
