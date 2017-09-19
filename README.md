# htcondor_test
testing htcondor for fccsw papas (with gaudi) at cern

Before any condor jobs are run fccsw must be installed and compiled. 
using papasdet branch from Alice. NB Make sure to initialize the FCC software stack using local init.sh which calls  init_fcc_local.sh in order to setup papas 1.1.0

git clone  git@github.com:alicerobson/papas.git
cd FCCSW
git checkout origin/papasdet
source init.sh
make -j12

Now you can start to submit jobs
cd ../papascondor


Edit multipapas.sub to have correct directories

create some output directories for condor:

    mkdir output error log

submit a single cluster of three jobs:

    condor_submit multipapas.sub

each job runs the script =mkdirs.py=

check your jobs:

    condor_q

