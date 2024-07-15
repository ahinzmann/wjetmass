# HEPDATA

## init environment

```
 !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/nfs/dust/cms/user/hinzmann/qganalysis/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/nfs/dust/cms/user/hinzmann/qganalysis/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/nfs/dust/cms/user/hinzmann/qganalysis/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/nfs/dust/cms/user/hinzmann/qganalysis/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
```

## create HepData entry

```
python make_hep_data.py
```

submit to sandbox of hepdata and download yoda files

# RIVET

ssh naf-cms.desy.de

## first setup

```
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc11
cd /afs/desy.de/user/h/hinzmann/wjetmass/
cmsrel CMSSW_13_2_0
cd CMSSW_13_2_0/src
cmssw-el7 --bind /nfs:/nfs
cmsenv
git-cms-init
git-cms-addpkg GeneratorInterface/RivetInterface
git-cms-addpkg Configuration/Generator
git clone https://gitlab.cern.ch/hinzmann/Rivet.git
cd Rivet
git remote add cms-gen https://gitlab.cern.ch/cms-gen/Rivet.git
git checkout jetwmass
source rivetSetup.sh
scram b -j8

# CMSSW singularity is missing latex commands
cp /usr/bin/latex /afs/desy.de/user/c/chenemil/wjetmass/CMSSW_13_2_0/src/Rivet/scripts
cp /usr/bin/dvips /afs/desy.de/user/c/chenemil/wjetmass/CMSSW_13_2_0/src/Rivet/scripts
cp /usr/bin/ps2pdf /afs/desy.de/user/c/chenemil/wjetmass/CMSSW_13_2_0/src/Rivet/scripts
cp /usr/bin/conver /afs/desy.de/user/c/chenemil/wjetmass/CMSSW_13_2_0/src/Rivet/scripts
```

## init environment

```
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc11
cd /afs/desy.de/user/c/chenemil/wjetmass/CMSSW_13_2_0/src/
cmssw-el7 --bind /nfs:/nfs
cmsenv
cd Rivet
source rivetSetup.sh
cd /afs/desy.de/user/c/chenemil/wjetmass
```

## run analysis

```
cmsRun CMSSW_13_2_0/src/Rivet/SMP/test/runRivetAnalyzer_WJET_13TeV_cfg.py

export RIVET_DATA_PATH=$RIVET_DATA_PATH:/afs/desy.de/user/h/hinzmann/wjetmass/CMSSW_13_2_0/src/Rivet/SMP/data/

rivet-mkhtml -c CMSSW_13_2_0/src/Rivet/SMP/data/CMS_2024_wjetmass.plot WJET_Pythia8_CP5_Apr2024.yoda
```

## modify code

```
cd CMSSW_13_2_0/src
# Rivet/SMP/src/CMS_2024_wjetmass.cc
scram b -j8
```

## running madgraph

```
cmsRun CMSSW_13_2_0/src/Rivet/SMP/test/runRivetAnalyzer_WJET_MadgraphPythia_13TeV_cfg.py
cmsRun CMSSW_13_2_0/src/Rivet/SMP/test/runRivetAnalyzer_WJET_MadgraphHerwig_13TeV_cfg.py
```
