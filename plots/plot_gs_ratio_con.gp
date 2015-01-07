set term postscript eps size 3.5,2.62 font 'Times, 24
set output 'img_gs_ratio_con.eps'

set xlabel 'Number of colluded users'
set ylabel 'Ratio of losing users'

set key off
plot 'ratio_group_con.txt' using 1:2:3  w boxerror

set term x11
set output
