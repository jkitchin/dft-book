#!/bin/bash
# A utility for calculating the vibrational intensities from VASP output (OUTCAR)
# (C) David Karhanek, 2011-03-25, ICIQ Tarragona, Spain (www.iciq.es)
# extract Born effective charges tensors
printf "..reading OUTCAR"
BORN_NROWS=`grep NIONS OUTCAR | awk '{print $12*4+1}'`
if [ `grep 'BORN' OUTCAR | wc -l` = 0 ] ; then \
   printf " .. FAILED! Born effective charges missing! Bye! \n\n" ; exit 1 ; fi
grep "in e, cummulative" -A $BORN_NROWS OUTCAR > born.txt
# extract Eigenvectors and eigenvalues
if [ `grep 'SQRT(mass)' OUTCAR | wc -l` != 1 ] ; then \
   printf " .. FAILED! Restart VASP with NWRITE=3! Bye! \n\n" ; exit 1 ; fi
EIG_NVIBS=`grep -A 2000 'SQRT(mass)' OUTCAR | grep 'cm-1' | wc -l`
EIG_NIONS=`grep NIONS OUTCAR | awk '{print $12}'`
EIG_NROWS=`echo "($EIG_NIONS+3)*$EIG_NVIBS+3" | bc`
grep -A $(($EIG_NROWS+2)) 'SQRT(mass)' OUTCAR | tail -n $(($EIG_NROWS+1)) | sed 's/f\/i/fi /g' > eigenvectors.txt
printf " ..done\n"
# set up a new directory, split files - prepare for parsing
printf "..splitting files"
mkdir intensities ; mv born.txt eigenvectors.txt intensities/
cd intensities/
let NBORN_NROWS=BORN_NROWS-1
let NEIG_NROWS=EIG_NROWS-3
let NBORN_STEP=4
let NEIG_STEP=EIG_NIONS+3
tail -n $NBORN_NROWS born.txt > temp.born.txt
tail -n $NEIG_NROWS eigenvectors.txt > temp.eige.txt
mkdir inputs ; mv born.txt eigenvectors.txt inputs/
split -a 3 -d -l $NEIG_STEP temp.eige.txt temp.ei.
split -a 3 -d -l $NBORN_STEP temp.born.txt temp.bo.
mkdir temps01 ; mv temp.born.txt temp.eige.txt temps01/
for nu in `seq 1 $EIG_NVIBS` ; do
 let nud=nu-1 ; ei=`printf "%03u" $nu` ; eid=`printf "%03u" $nud` ; mv temp.ei.$eid eigens.vib.$ei
done
for s in `seq 1 $EIG_NIONS` ; do
 let sd=s-1 ; bo=`printf "%03u" $s` ; bod=`printf "%03u" $sd` ; mv temp.bo.$bod borncs.$bo
done
printf " ..done\n"
# parse deviation vectors (eig)
printf "..parsing eigenvectors"
let sad=$EIG_NIONS+1
for nu in `seq 1 $EIG_NVIBS` ; do
 nuu=`printf "%03u" $nu`
 tail -n $sad eigens.vib.$nuu | head -n $EIG_NIONS | awk '{print $4,$5,$6}' > e.vib.$nuu.allions
 split -a 3 -d -l 1 e.vib.$nuu.allions temp.e.vib.$nuu.ion.
 for s in `seq 1 $EIG_NIONS` ; do
  let sd=s-1; bo=`printf "%03u" $s`; bod=`printf "%03u" $sd`; mv temp.e.vib.$nuu.ion.$bod e.vib.$nuu.ion.$bo
 done
done
printf " ..done\n"
# parse born effective charge matrices (born)
printf "..parsing eff.charges"
for s in `seq 1 $EIG_NIONS` ; do
 ss=`printf "%03u" $s`
 awk '{print $2,$3,$4}' borncs.$ss | tail -3 > bornch.$ss
done
mkdir temps02 ; mv eigens.* borncs.* temps02/
printf " ..done\n"
# parse matrices, multiply them and collect squares (giving intensities)
printf "..multiplying matrices, summing "
for nu in `seq 1 $EIG_NVIBS` ; do
 nuu=`printf "%03u" $nu`
 int=0.0
 for alpha in 1 2 3 ;  do            # summing over alpha coordinates
  sumpol=0.0
  for s in `seq 1 $EIG_NIONS` ; do   # summing over atoms
   ss=`printf "%03u" $s`
   awk -v a="$alpha" '(NR==a){print}' bornch.$ss > z.ion.$ss.alpha.$alpha
   # summing over beta coordinates and multiplying Z(s,alpha)*e(s) done by the following awk script
   paste z.ion.$ss.alpha.$alpha  e.vib.$nuu.ion.$ss | \
   awk '{pol=$1*$4+$2*$5+$3*$6; print $0,"  ",pol}' > matr-vib-${nuu}-alpha-${alpha}-ion-${ss}
  done
  sumpol=`cat matr-vib-${nuu}-alpha-${alpha}-ion-* | awk '{sum+=$7} END {print sum}'`
  int=`echo "$int+($sumpol)^2" | sed 's/[eE]/*10^/g' |  bc -l`
 done
 freq=`awk '(NR==1){print $8}' temps02/eigens.vib.$nuu`
 echo "$nuu $freq $int">> exact.res.txt
 printf "."
done
printf " ..done\n"
# format results, normalize intensities
printf "..normalizing intensities"
max=`awk '(NR==1){max=$3} $3>=max {max=$3} END {print max}' exact.res.txt`
awk -v max="$max" '{printf "%03u %6.1f %5.3f\n",$1,$2,$3/max}' exact.res.txt > results.txt
printf " ..done\n"
# clean up, display results
printf "..finalizing:\n"
mkdir temps03; mv bornch.* e.vib.*.allions temps03/
mkdir temps04; mv z.ion* e.vib.*.ion.* temps04/
mkdir temps05; mv matr-* temps05/
mkdir results; mv *res*txt results/
let NMATRIX=$EIG_NVIBS**2
printf "%5u atoms found\n%5u vibrations found\n%5u matrices evaluated" \
       $EIG_NIONS $EIG_NVIBS $NMATRIX > results/statistics.txt
  # fast switch to clean up all temporary files
  rm -r temps*
cat results/results.txt