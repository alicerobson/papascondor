# htcondor_test
testing htcondor for fccsw papas (with gaudi) at cern

Before any condor jobs are run papas libary and fccsw must be installed and compuîled. 




User must have installed and compiled papas library
30/8/2017 need logtest branch from Alice

git clone git@github.com:alicerobson/papas.git
cd papas
git checkout origin/logtest

source init.sh
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=../install ../
make -j 4
make install
cd ..


User must have installed and compiled fccsw
30/8/2017 need logte branch from Alice

git clone  git@github.com:alicerobson/papas.git
cd FCCSW
git checkout origin/logte


Now you can start to submit jobs
The papastest.sh


Make sure to initialize the FCC software stack in the usual way, for the latest version of the software.
e.g.:

    source /cvmfs/fcc.cern.ch/sw/0.8.1/init_fcc_stack.sh

create some output directories for condor:

    mkdir output error log

submit a single cluster of three jobs:

    condor_submit multiple.sub

each job runs the script =mkdirs.py=

check your jobs:

    condor_q

check that you are using the fcc accounting group: 

    condor_q -long | grep AccountingGroup

should give something like:

```
[python_toy]$ condor_q -long | grep AccountingGroup
AccountingGroup = "group_u_FCC.local_gen.cbern"
...
```

When the jobs are done, check the =output=, =log=, and =error= directories. 
In addition, each job creates an output directory called =output_<cluster_number>_<job_number>.
Each directory contains a file with something written in it.

Further information about htcondor: 
- A much better tutorial than the one of CERN! http://research.cs.wisc.edu/htcondor/tutorials/intl-grid-school-3/submit_first.html
- Condor documentation: https://research.cs.wisc.edu/htcondor/manual/

