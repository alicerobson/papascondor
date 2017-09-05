## Simple Papas Run
## Runs papas using as a sequence of tools
## The reconstructed particles are written to a ROOT file

#
#  To run PapasTools
#  > ./run gaudirun.py Sim/SimPapas/options/simple_papastool_clic.py


import argparse
recoparser = argparse.ArgumentParser()
recoparser.add_argument('-o','--routput', type=str, default='output.root', help='output.root')
recoparser.add_argument('-i','--rinput', type=str, default='./ee_Z_ddbar.root', help='ee_Z_ddbar.root')
recoparser.add_argument('-m','--rmag', type=float, help='2.')
recoparser.add_argument('-n','--rmaxevents', type=int,default = 10, help='10')
recoargs, _ = recoparser.parse_known_args()

outputfilename = recoargs.routput
inputfilename = recoargs.rinput
rrmag = recoargs.rmag
rmaxevents = recoargs.rmaxevents

print "=================================="
print "input = ", inputfilename
print "output = ", outputfilename
print "mag = ", rrmag
print "maxevents = ", rmaxevents
print "=================================="

#

from Gaudi.Configuration import *
from Configurables import ApplicationMgr, FCCDataSvc, PodioOutput
from GaudiKernel import SystemOfUnits as units


### Example of pythia configuration file to generate events
pythiafile="Sim/SimPapas/data/ee_ZH_Zmumu_Hbb.txt"

#### Data service
podioevent = FCCDataSvc("EventDataSvc")

from Configurables import  HepMCFileReader
from Configurables import PythiaInterface, GenAlg
### PYTHIA algorithm
pythia8gentool = PythiaInterface("Pythia8Interface", Filename=pythiafile)
pythia8gen = GenAlg("Pythia8", SignalProvider=pythia8gentool)
pythia8gen.hepmc.Path = "hepmcevent"

from Configurables import HepMCToEDMConverter
### Reads an HepMC::GenEvent from the data service and writes a collection of EDM Particles
hepmc_converter = HepMCToEDMConverter("Converter")
hepmc_converter.hepmc.Path="hepmcevent"
hepmc_converter.genparticles.Path="GenParticle"
hepmc_converter.genvertices.Path="Genvertex"

from Configurables import PapasAlg, PapasImportParticlesTool
from Configurables import PapasSimulatorTool, PapasMergeClustersTool, PapasBuildBlocksTool
from Configurables import PapasSimplifyBlocksTool, PapasPFReconstructorTool, PapasExportParticlesTool

from Configurables import ClicFieldSvc, ClicTrackerSvc, ClicEcalSvc, ClicHcalSvc
fieldsvc = ClicFieldSvc("ClicFieldSvc", magnitude=rrmag); #todo add in remaining parameters
ecalsvc = ClicEcalSvc("ClicEcalSvc", emin = [.5, .5]);
hcalsvc = ClicHcalSvc("ClicHcalsvc");
trackersvc = ClicTrackerSvc("ClicTrackerSvc");

from Configurables import ClicDetSvc
detservice = ClicDetSvc("ClicDetSvc",
                        ecalService = "ClicEcalSvc",
                        hcalService = "ClicHcalSvc",
                        trackerService = "ClicTrackerSvc",
                        fieldService = "ClicFieldSvc");

#Notes:
#
# The PapasAlg allows a configurable set of tools to be run (see below).
# The Papas::Event is passed to each of the tools and new collections are then added into the papas::Event.
# Thus subsequent tools can access previously made collections.
# The papas::Event uses a short hand to label the collections that it contains:
# see https://github.com/alicerobson/FCCSW/blob/papas0.8.1/Sim/doc/FastSimulationUsingPapas.md
# TODO update this link when pull request has gone through
#read in pythia generated particles, write out reconstructed particles (fcc EDM format)
papasalg = PapasAlg("papasalg",
                    tools=["PapasImportParticlesTool/importer", #reads in gen_particles and creates papas particles.
                           "PapasSimulatorTool/papassim", #simulates smeared clusters and tracks
                           "PapasMergeClustersTool/ecalmerge", #merges clusters ECAL
                           "PapasMergeClustersTool/hcalmerge", #merged clusters HCAL
                           "PapasBuildBlocksTool/blockbuilder", #build blocks of linked clusters and tracks
                           "PapasSimplifyBlocksTool/blocksimplifier", #simplifies the blocks
                           "PapasPFReconstructorTool/reconstructor"], #reconstructs particles based on the blocks
                    exportTool ="PapasExportParticlesTool/exporter", #export papas reconstructed particles to fcc particles
                    #seed = 0xdeadbeef,#seed random generator
                            physicsDebugFile = 'papasPhysicsdd.out', #write out papas physics to file
                            detService = "ClicDetSvc") #name of detector service

#Papas importer
importer = PapasImportParticlesTool("importer")
importer.genparticles.Path='GenParticle' #name of the input pythia particles collection

#Papas simulation
#reads in papas particles and simulated true and smeared cluster and tracks
papassimtool = PapasSimulatorTool("papassim", particleSubtype="s")
#Papas Merge Clusters
#takes smeared ecal and hcal clusters and merges overlapping clusters
papasmergeecaltool = PapasMergeClustersTool("ecalmerge", TypeAndSubtype="es") #run merge on clusters of type "es" = ecal smeared

papasmergehcaltool = PapasMergeClustersTool("hcalmerge", TypeAndSubtype="hs") #run merge on clusters of type "hs" = hcal smeared

#Papas Construct Blocks of connected clusters and tracks
papasblockbuildertool = PapasBuildBlocksTool("blockbuilder",
                                             ecalSubtype="m", #use merged ecal clusters collection
                                             hcalSubtype="m", #use merged ecal clusters collection
                                             trackSubtype="s") #use smeared tracks collection
#Papas simplify the blocks structures
papasblocksimplifiertool = PapasSimplifyBlocksTool("blocksimplifier", blockSubtype="r") #use the reconstucted blocks from previous step

#Papas Reconstruct particles from blocks
papaspfreconstructortool = PapasPFReconstructorTool("reconstructor", blockSubtype ="s") #use blocks collection from block simplifier

#export reconstructed particles to root file
papasexportparticlestool = PapasExportParticlesTool("exporter", particleSubtype="r") #use the reconstructed particles as input
papasexportparticlestool.recparticles.Path='papasreconstructed' #name of output reconstructed particles in fcc format

#output fcc particles to root
from Configurables import PodioOutput
out = PodioOutput("out",
                  OutputLevel=INFO, filename=outputfilename)
out.outputCommands = ["keep *"]

from Configurables import ApplicationMgr
ApplicationMgr(
    ## all algorithms should be put here
    TopAlg=[pythia8gen, hepmc_converter, papasalg, out],
    EvtSel='NONE',
    ## number of events
    EvtMax=rmaxevents,
    ## all services should be put here
    ExtSvc = [podioevent, detservice],
    OutputLevel = DEBUG
 )
