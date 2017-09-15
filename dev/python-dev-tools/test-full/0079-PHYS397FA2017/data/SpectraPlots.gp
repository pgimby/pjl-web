set term postscript eps enhanced
set output 'XRaySpec-Angle.eps'

reset
set multiplot layout 2,1 title "(un)Attenuated X-Ray Spectra" font ",18"
set xtics 10

set ylabel 'Count' offset graph 0,-.6


plot 'FullXRaySpec-Angle.dat' u 1:2:4 w yerrorbars title "Count (no acrylic)" lc rgb 'black', \
'FullXRaySpecSupplement.dat' u 1:3 w lp pt 7 lt 1 ps .4 lc rgb 'blue' title 'Supplementary Data'

set xlabel 'Angle (Degrees)'
set ylabel ""

plot 'AttenuatedXRaySpec-Angle.dat' using 1:2:4 w yerrorbars notitle, \
'AttenuatedXRaySpec-Angle.dat' w l title 'Count (with acrylic)' lc rgb 'red' lt 1 lw 2
unset multiplot

!epstopdf 'XRaySpec-Angle.eps' && rm 'XRaySpec-Angle.eps'






set output 'XRaySpec-Wavelength.eps'

reset
set multiplot layout 2,1 title "(un)Attenuated X-Ray Spectra" font ",18"
set format x "%4.2E"

set ylabel 'Count' offset graph 0,-.6


plot 'FullXRaySpec-Wavelength.dat' u 1:2:3 w yerrorbars notitle lc rgb 'black', \
'FullXRaySpec-Wavelength.dat' u 1:2 w l lc rgb 'red' lt 1 lw 2 title "Count (no acrylic)", \
'FullXRaySpecSupplement.dat' u 5:3 w lp pt 7 lt 1 ps .4 lc rgb 'blue' title 'Supplementary Data'


set xlabel 'Wavelength (m)'
set ylabel ""

plot 'AttenuatedXRaySpec-Wavelength.dat' using 1:2:3 w yerrorbars notitle lc rgb 'black', \
'AttenuatedXRaySpec-Wavelength.dat' u 1:2 w l title 'Count (with acrylic)' lc rgb 'red' lt 1 lw 2
unset multiplot

!epstopdf 'XRaySpec-Wavelength.eps' && rm 'XRaySpec-Wavelength.eps'






set output 'XRaySpec-Energy.eps'

reset
set multiplot layout 2,1 title "(un)Attenuated X-Ray Spectra" font ",18"
#set format x "%g"
set xtics 2.0

set ylabel 'Count' offset graph 0,-.6


plot 'FullXRaySpec-Energy.dat' u 1:2:3 w yerrorbars notitle lc rgb 'black', \
'FullXRaySpec-Energy.dat' u 1:2 w l lc rgb 'red' lt 1 lw 2 title "Count (no acrylic)", \
'FullXRaySpecSupplement.dat' u 7:3 w lp pt 7 lt 1 ps .4 lc rgb 'blue' title 'Supplementary Data'

set xlabel 'Energy (keV)'
set ylabel ""

plot 'AttenuatedXRaySpec-Energy.dat' using 1:2:3 w yerrorbars notitle, \
'AttenuatedXRaySpec-Energy.dat' u 1:2 w l title 'Count (with acrylic)' lc rgb 'red' lt 1 lw 2
unset multiplot

!epstopdf 'XRaySpec-Energy.eps' && rm 'XRaySpec-Energy.eps'





set output 'HugoData-Angle.eps'

reset
set title "Attenuated X-Ray Spectra" font ",18"
#set format x "%g"
set xrange [0:*]
set xtics 2.0

set ylabel 'Count'
set xlabel 'Angle (degrees)'

plot 'HugoDataCuLiF.dat' u 1:2:3 w yerrorbars notitle lc rgb 'black', \
'HugoDataCuLiF.dat' u 1:2 w l lc rgb 'red' lw 2 lt 1 notitle
#'FullXRaySpec-Energy.dat' u 1:2 w l lc rgb 'red' lt 1 lw 2 title "Count (no acrylic)", \
#'FullXRaySpecSupplement.dat' u 7:3 w lp pt 7 lt 1 ps .4 lc rgb 'blue' title 'Supplementary Data'



!epstopdf 'HugoData-Angle.eps' && rm 'HugoData-Angle.eps'






