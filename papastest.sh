#!/bin/bash

#path of the software
echo "Export paths"
export SOFTWARE_PATH_AFS=/afs/cern.ch/user/a/alrobson/FCCSW/FCCSW
export SOFTWARE_PATH_PAPAS=/afs/cern.ch/user/a/alrobson/FCCSW/papas

export CMTCONFIG=x86_64-slc6-gcc62-opt
export outputfilename=papasout.root

echo "Copy a working directory"
cp -r $SOFTWARE_PATH_AFS .
cp -r $SOFTWARE_PATH_PAPAS .

cd papas/
echo "Init papas"
source init.sh afs
cd ../FCCSW/
echo "Init"
source init.sh afs

echo "run"
echo "cluster: " $1
echo "job: " $2
echo "pythiafile: " $3
echo "field: " $4
echo "maxevents: " $5

pwd
LD_PRELOAD=build.$BINARY_TAG/lib/libPapasUtils.so ./run fccrun.py ../simple_papastool_condor.py --rpythiainput  $3 --routput $outputfilename --rmag $4 --rmaxevents $5

#copy to EOS
echo "LS:"
ls -l $outputfilename
export directory=/eos/user/a/alrobson/condor/outputfccmulti_$1
echo $directory
if [ ! -d $directory ]; then
echo make $directory
mkdir $directory
fi
echo "copy" xrdcp $outputfilename $directory/${outputfilename%.*}_$4_$2.${outputfilename##*.}
xrdcp $outputfilename $directory/${outputfilename%.*}_$4_$2.${outputfilename##*.}

#or copy locally
export directory2=../outputfcc_$1
echo $directory2
if [ ! -d $directory2 ]; then
echo make $directory2
mkdir $directory2
fi
echo "copy" xrdcp $outputfilename $directory2/${outputfilename%.*}_$4_$2.${outputfilename##*.}
xrdcp $outputfilename $directory2/${outputfilename%.*}_$4_$2.${outputfilename##*.}

echo "Cleaning"
cd ../
rm -rf FCCSW


