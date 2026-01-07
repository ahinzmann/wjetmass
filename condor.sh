#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /afs/desy.de/user/h/hinzmann/wjetmass/CMSSW_13_2_0/src/
cmsenv
mkdir /tmp/job$1
cd /tmp/job$1
export RIVET_DATA_PATH=$RIVET_DATA_PATH:/afs/desy.de/user/h/hinzmann/wjetmass/CMSSW_13_2_0/src/Rivet/SMP/data/
cmsRun /afs/desy.de/user/h/hinzmann/wjetmass/CMSSW_13_2_0/src/Rivet/SMP/test/runRivetAnalyzer_WJET_$2_13TeV_cfg.py analyze=0 seed=$1

mkdir /data/dust/user/hinzmann/jetmass/gen$2
mkdir /data/dust/user/hinzmann/jetmass/gen$2/genjob$1
mv *.root /data/dust/user/hinzmann/jetmass/gen$2/genjob$1
mv *.yoda /data/dust/user/hinzmann/jetmass/gen$2/genjob$1

rm cmsgrid_final.lhe
rm InterfaceMatchbox*
rm HerwigConfig.in
