#!/bin/bash
# reformat intensities, just normal modes: 3N -> (3N-6)
printf "..reformatting and normalizing intensities"
cd intensities/results/
nlns=`wc -l exact.res.txt | awk '{print $1}' `; let bodylns=nlns-6
head -n $bodylns exact.res.txt > temp.reform.res.txt
max=`awk '(NR==1){max=$3} $3>=max {max=$3} END {print max}' temp.reform.res.txt`
awk -v max="$max" '{print $1,$2,$3/max}' temp.reform.res.txt > exact.reform.res.txt
awk -v max="$max" '{printf "%03u %6.1f %5.3f\n",$1,$2,$3/max}' temp.reform.res.txt > reform.res.txt
printf " ..done\n..normal modes:\n"
rm temp.reform.res.txt
cat reform.res.txt
cd ../..