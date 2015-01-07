set term postscript eps size 3.5,2.62 font 'Times, 24
set output 'img_up_perturb_dis.eps'

set xlabel 'Perturbation size'
set ylabel 'Loss of platform utility'

set key off
plot 'perturb_group_dis.txt' using 1:4:5  w boxerror

set term x11
set output
