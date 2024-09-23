#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /afs/desy.de/user/h/hinzmann/wjetmass/CMSSW_13_2_0/src/
cmsenv
mkdir /tmp/job$1
cd /tmp/job$1
cmsRun /afs/desy.de/user/h/hinzmann/wjetmass/CMSSW_13_2_0/src/Rivet/SMP/test/runRivetAnalyzer_WJET_$2_13TeV_cfg.py seed=$1

mkdir /nfs/dust/cms/user/hinzmann/jetmass/gen$2
mkdir /nfs/dust/cms/user/hinzmann/jetmass/gen$2/genjob$1
mv *.root /nfs/dust/cms/user/hinzmann/jetmass/gen$2/genjob$1
mv *.yoda /nfs/dust/cms/user/hinzmann/jetmass/gen$2/genjob$1

rm cmsgrid_final.lhe
rm InterfaceMatchbox*
rm HerwigConfig.in
