set term postscript eps size 3.5,2.62 font 'Times, 24
set output 'img_tr_loss_dis.eps'

set xlabel 'Number of colluded users'
set ylabel 'Loss of user utility (avg.)'

set key off
plot 'loss_truthful_dis.txt' using 1:2:3  w boxerror

set term x11
set output
