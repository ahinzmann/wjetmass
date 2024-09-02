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
cp /nfs/dust/cms/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_07-08-23/FullRunII/CombinedFit_results.root CombinedFit_results.root
cp /nfs/dust/cms/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_N2Cut_02-04-24/FullRunII/CombinedFit_results.root CombinedFit_results_N2Cut.root
cp /nfs/dust/cms/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_07-08-23/FullRunII/plots/pretty_unfold_sigma/m_unfold_suminclusive.pdf .
cp /nfs/dust/cms/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_07-08-23/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt0inclusive.pdf .
cp /nfs/dust/cms/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_07-08-23/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt1inclusive.pdf .
cp /nfs/dust/cms/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_07-08-23/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt2inclusive.pdf .
cp /nfs/dust/cms/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_07-08-23/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt3inclusive.pdf .
cp /nfs/dust/cms/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_N2Cut_02-04-24/FullRunII/plots/pretty_unfold_sigma/m_unfold_suminclusive.pdf m_unfold_suminclusive_N2Cut.pdf
cp /nfs/dust/cms/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_N2Cut_02-04-24/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt0inclusive.pdf m_unfold_pt0inclusive_N2Cut.pdf
cp /nfs/dust/cms/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_N2Cut_02-04-24/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt1inclusive.pdf m_unfold_pt1inclusive_N2Cut.pdf
cp /nfs/dust/cms/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_N2Cut_02-04-24/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt2inclusive.pdf m_unfold_pt2inclusive_N2Cut.pdf
cp /nfs/dust/cms/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_N2Cut_02-04-24/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt3inclusive.pdf m_unfold_pt3inclusive_N2Cut.pdf
python3 make_hep_data.py
```

submit to sandbox of hepdata and download yoda files

# RIVET

ssh naf-cms.desy.de

## first setup

```
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=el9_amd64_gcc11
cd /afs/desy.de/user/c/chenemil/wjetmass/
cmsrel CMSSW_13_2_0
cd CMSSW_13_2_0/src
cmsenv
git-cms-init
git-cms-addpkg GeneratorInterface/RivetInterface
git-cms-addpkg Configuration/Generator
git clone https://github.com/chenemil/Rivet
#git clone ssh://git@gitlab.cern.ch:7999/hinzmann/Rivet.git
cd Rivet
git checkout wjetmass
source rivetSetup.sh
scram b -j8
```

## init environment

```
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=el9_amd64_gcc11
cd /afs/desy.de/user/c/chenemil/wjetmass/CMSSW_13_2_0/src/
cmsenv
cd Rivet
source rivetSetup.sh
cd /afs/desy.de/user/c/chenemil/wjetmass
alias python=python3
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

## running with condor

```
edit condor.sh and modify outputfile names and output directories to needs
test if it runs locally with some random seed (here 123): source condor.sh 123
submit one job (can be repeated multiple times): condor_submit condor.submit
watch job status: condor_q
check logfiles: madgraph*.log, madgraph*.o, madgraph*.e
check outputfiles: /nfs/dust/cms/user/hinzmann/job*
```
