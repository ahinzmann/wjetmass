# HEPDATA

## init environment

```
 !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/data/dust/user/hinzmann/qganalysis/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/data/dust/user/hinzmann/qganalysis/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/data/dust/user/hinzmann/qganalysis/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/data/dust/user/hinzmann/qganalysis/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
```

## create HepData entry

```
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_18-09-24/FullRunII/CombinedFit_results.root CombinedFit_results.root
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_N2Cut_18-09-24/FullRunII/CombinedFit_results.root CombinedFit_results_N2Cut.root
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_18-09-24/FullRunII/plots/pretty_unfold_sigma/m_unfold_suminclusive.pdf .
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_18-09-24/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt0inclusive.pdf .
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_18-09-24/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt1inclusive.pdf .
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_18-09-24/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt2inclusive.pdf .
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_18-09-24/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt3inclusive.pdf .
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_N2Cut_18-09-24/FullRunII/plots/pretty_unfold_sigma/m_unfold_suminclusive.pdf m_unfold_suminclusive_N2Cut.pdf
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_N2Cut_18-09-24/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt0inclusive.pdf m_unfold_pt0inclusive_N2Cut.pdf
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_N2Cut_18-09-24/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt1inclusive.pdf m_unfold_pt1inclusive_N2Cut.pdf
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_N2Cut_18-09-24/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt2inclusive.pdf m_unfold_pt2inclusive_N2Cut.pdf
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_N2Cut_18-09-24/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt3inclusive.pdf m_unfold_pt3inclusive_N2Cut.pdf
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_18-09-24NoMatching/FullRunII/plots/pretty_unfold_sigma/m_unfold_suminclusive.pdf ./m_unfold_suminclusive_NoMatching.pdf
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_18-09-24NoMatching/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt0inclusive.pdf ./m_unfold_pt0inclusive_NoMatching.pdf
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_18-09-24NoMatching/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt1inclusive.pdf ./m_unfold_pt1inclusive_NoMatching.pdf
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_18-09-24NoMatching/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt2inclusive.pdf ./m_unfold_pt2inclusive_NoMatching.pdf
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_18-09-24NoMatching/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt3inclusive.pdf ./m_unfold_pt3inclusive_NoMatching.pdf
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_N2Cut_18-09-24NoMatching/FullRunII/plots/pretty_unfold_sigma/m_unfold_suminclusive.pdf m_unfold_suminclusive_N2Cut_NoMatching.pdf
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_N2Cut_18-09-24NoMatching/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt0inclusive.pdf m_unfold_pt0inclusive_N2Cut_NoMatching.pdf
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_N2Cut_18-09-24NoMatching/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt1inclusive.pdf m_unfold_pt1inclusive_N2Cut_NoMatching.pdf
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_N2Cut_18-09-24NoMatching/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt2inclusive.pdf m_unfold_pt2inclusive_N2Cut_NoMatching.pdf
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_N2Cut_18-09-24NoMatching/FullRunII/plots/pretty_unfold_sigma/m_unfold_pt3inclusive.pdf m_unfold_pt3inclusive_N2Cut_NoMatching.pdf
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

# possibly need to fix python
alias python=python3
unset PYTHONPATH
unset PYTHONHOME
cd CMSSW_13_2_0/src
cmsenv
cd ../..
```

## run generation and analysis

```
cmsRun CMSSW_13_2_0/src/Rivet/SMP/test/runRivetAnalyzer_WJET_13TeV_cfg.py
cmsRun CMSSW_13_2_0/src/Rivet/SMP/test/runRivetAnalyzer_WJET_MadgraphPythia_13TeV_cfg.py
cmsRun CMSSW_13_2_0/src/Rivet/SMP/test/runRivetAnalyzer_WJET_MadgraphHerwig_13TeV_cfg.py

export RIVET_DATA_PATH=$RIVET_DATA_PATH:/afs/desy.de/user/h/hinzmann/wjetmass/CMSSW_13_2_0/src/Rivet/SMP/data/

rivet-mkhtml -c CMSSW_13_2_0/src/Rivet/SMP/data/CMS_2024_wjetmass.plot WJET_Pythia8_CP5_Apr2024.yoda
rivet-mkhtml -c CMSSW_13_2_0/src/Rivet/SMP/data/CMS_2024_wjetmass.plot WJET_MadgraphPythia_12Sep2024.yoda:'Title=Madgraph+Pythia':ErrorBars=1:PolyMarker=triangle:DotScale=1.5 WJET_MadgraphHerwig_12Sep2024.yoda:'Title=Madgraph+Herwig':ErrorBars=1:LineStyle=dotted:PolyMarker=diamond:DotScale=1.5 WJET_Pythia8_CP5_12Sep2024.yoda:'Title=Pythia':ErrorBars=1:LineStyle=dashed:PolyMarker=square:DotScale=1.5
rivet-mkhtml -c CMSSW_13_2_0/src/Rivet/SMP/data/CMS_2024_wjetmass.plot WJET_MadgraphPythia_5Sep2024.yoda:'Title=Madgraph+Pythia':ErrorBars=1:PolyMarker=triangle:DotScale=1.5 WJET_MadgraphHerwig_5Sep2024.yoda:'Title=Madgraph+Herwig':ErrorBars=1:LineStyle=dotted:PolyMarker=diamond:DotScale=1.5 --no-rivet-refs
```

## modify code

```
cd CMSSW_13_2_0/src
# Rivet/SMP/src/CMS_2024_wjetmass.cc
scram b -j8
```

## running with condor

```
edit condor.sh and modify outputfile names and output directories to needs
test if it runs locally with some random seed (here 123): source condor.sh 123
submit one job (can be repeated multiple times): condor_submit condor.submit
watch job status: condor_q
check logfiles: gen*.log, gen*.o, gen*.e
check outputfiles: /data/dust/user/hinzmann/job*
```

## estimate model uncertainty

python plot_model_uncertainty_map.py

## measure W mass

cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_N2Cut_18-09-24/FullRunII/poi_correlation_matrix.npy poi_correlation_matrix-withN2.npy
cp /data/dust/user/hinzmann/jetmass/JetMass/rhalph/UnfoldingParticleNet_18-09-24/FullRunII/poi_correlation_matrix.npy poi_correlation_matrix-noN2.npy

python make_w_fit.py

