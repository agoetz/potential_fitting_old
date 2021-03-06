#!/bin/bash

gcn=generate_configs_normdistrbn

mkdir logs
mkdir diffs

err=0

python3 nmcgen.py settings.ini h2o.xyz h2o.opt.xyz normal_modes configs.xyz
if [ $? -ne 0 ]
then
    echo "Error: Execution of generate_nm_configs.py failed"
    err=$(($err+1))
fi

ndiff -quiet -abserr 1.e-5 expected/h2o.opt.xyz h2o.opt.xyz > diffs/h2o.opt.xyz.dif
if [ $? -ne 0 ]
then
    echo "Error: optimized geometries differ - check diffs/h2o.opt.xyz.dif"
    err=$(($err+1))
fi

ndiff -quiet -abserr 1.e-5 expected/normal_modes normal_modes > diffs/normal_modes.dif
if [ $? -ne 0 ]
then
    echo "Error: normalmodes differ - check diffs/normal_modes.dif"
    err=$(($err+1))
fi

ndiff -quiet -abserr 1.e-5 expected/configs.xyz configs.xyz > diffs/configs.xyz.dif
if [ $? -ne 0 ]
then
    echo "Error: configurations differ - check diffs/configs.xyz.dif"
    err=$(($err+1))
fi

if [ $err -ne 0 ]
then
    echo "test failed"
else
    echo "test passed"
    ./clean_test.sh
fi

exit $err
