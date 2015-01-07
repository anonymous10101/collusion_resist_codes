set term postscript eps size 3.5,2.62 font 'Times, 24
set output 'img_up_ratio_dis.eps'

set xlabel 'Number of colluded users'
set ylabel 'Loss of platform utility'

set key off
plot 'ratio_group_dis.txt' using 1:4:5  w boxerror

set term x11
set output
