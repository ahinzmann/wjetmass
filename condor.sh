#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /afs/desy.de/user/h/hinzmann/wjetmass/CMSSW_13_2_0/src/
cmsenv
mkdir /nfs/dust/cms/user/hinzmann/job$1
cd /nfs/dust/cms/user/hinzmann/job$1
cmsRun /afs/desy.de/user/h/hinzmann/wjetmass/CMSSW_13_2_0/src/Rivet/SMP/test/runRivetAnalyzer_WJET_MadgraphPythia_13TeV_cfg.py process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=$1 process.RandomNumberGeneratorService.generator.initialSeed=$1 process.RAWSIMoutput.fileName=WJET_MadgraphPythia_inHepMC$1.root process.process.LHEoutput.fileName=WJET_MadgraphPythia_inLHE$1.root process.rivetAnalyzer.OutputFile=WJET_MadgraphPythia$1.yoda
