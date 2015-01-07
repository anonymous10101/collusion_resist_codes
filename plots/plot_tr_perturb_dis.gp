set term postscript eps size 3.5,2.62 font 'Times, 24
set output 'img_tr_perturb_dis.eps'

set xlabel 'Perturbation size'
set ylabel 'Loss of user utility (avg.)'

set key off
plot 'perturb_truthful_dis.txt' using 1:2:3  w boxerror

set term x11
set output
