#/bin/bash

years="2013"
satellites="avhrr-m02"


for year in $years; do

    for satellite in $satellites; do


	bsub -q short-serial -W 06:00 -o out16.log -e out16.err python2.7 one_file_sstcomp.py drifter-sst $year $satellite 


	
    done

done