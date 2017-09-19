#!/bin/bash

#path of the software
echo "Export paths"
export SOFTWARE_PATH_AFS=/afs/cern.ch/user/a/alrobson/dettest/FCCSW
#export SOFTWARE_PATH_PAPAS=/afs/cern.ch/user/a/alrobson/FCCSW/papas

export CMTCONFIG=x86_64-slc6-gcc62-opt

echo "Copy a working directory"
cp -r $SOFTWARE_PATH_AFS .

cd ./FCCSW/
echo "Init"
echo pwd
pwd
source init.sh afs
echo "LS:"
ls -al

./run gaudirun.py Examples/options/example_options.py

#copy to EOS
echo "LS:"
ls -al


