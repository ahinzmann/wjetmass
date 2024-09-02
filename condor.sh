#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /afs/desy.de/user/h/hinzmann/wjetmass/CMSSW_13_2_0/src/
cmsenv
mkdir /nfs/dust/cms/user/hinzmann/jetmass/gen$2/job$1
cd /nfs/dust/cms/user/hinzmann/jetmass/gen$2/job$1
cmsRun /afs/desy.de/user/h/hinzmann/wjetmass/CMSSW_13_2_0/src/Rivet/SMP/test/runRivetAnalyzer_WJET_$2_13TeV_cfg.py process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=$1 process.RandomNumberGeneratorService.generator.initialSeed=$1 process.RAWSIMoutput.fileName="WJET_$2_inHepMC$1.root" process.LHEoutput.fileName="WJET_$2_inLHE$1.root" process.rivetAnalyzer.OutputFile="WJET_$2$1.yoda"
rm cmsgrid_final.lhe
