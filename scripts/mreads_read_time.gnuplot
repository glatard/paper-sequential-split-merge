set terminal pdfcairo color
set border 3 front lt black linewidth 1.000 dashtype solid
set boxwidth 0.5 absolute
set style fill solid 0.50 border lt -1
unset key
set pointsize 0.5

set style data boxplot
set xtics border in scale 0,0 nomirror norotate  autojustify
set xtics  norangelimit
set datafile separator ","

 

set xtics ("6g-hdd" 1, "6g-ssd" 2, "9g-hdd" 3, "9g-ssd" 4, "12g-hdd" 5, "12g-ssd" 6)
unset format y
unset ydata
unset xrange
unset logscale x
unset format x
set boxwidth 0.5
set xlabel "Merging strategy - Multiple Reads: Read Time on HDD and SSD" 
set ylabel "Read Time (s)"
set output "../figures/benchmark-mreads-hdd-ssd-read-time.pdf"
plot '../data/data_hdd.csv' using (1):1, '' using (3):6, '' using (5):11, '../data/data_ssd.csv' using (2):1, '' using (4):6, '' using (6):11
 
