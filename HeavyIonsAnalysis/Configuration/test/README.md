2023.10.03 [Please refer to this repo:dir for all info](https://github.com/cfmcginn/production/tree/main/HIRun2023/forestPPRef)
# General building instruction
Some small amount of files for getting the forest to run w/ the pp RECO miniAOD

To build with the forest, start by following:
https://twiki.cern.ch/twiki/bin/view/CMS/HiForestSetup#Setup_for_13_2_X_2023_PbPb_data

```
cmsrel CMSSW_13_2_6_patch2
cd CMSSW_13_2_6_patch2/src
cmsenv
git cms-init

git cms-merge-topic CmsHI:forest_CMSSW_13_2_X
git remote add cmshi git@github.com:CmsHI/cmssw.git
scram b -j8
```

At this point we have a good build, and need to add some python and the B finder

```
#Grab the additional python
git clone https://github.com/cfmcginn/production
cp production/HIRun2023/forestPPRef/ak* HeavyIonsAnalysis/JetAnalysis/python/
cp production/HIRun2023/forestPPRef/forest_miniAOD_run3_ppRECO_DATA.py HeavyIonsAnalysis/Configuration/test/
rm -rf production

###### B/D finder in forest v0 ######
#Add the B finder
#Based on:
#https://github.com/jusaviin/HiForestSetupPbPbRun2023#test-the-configuration
#git clone -b 13XX_miniAOD https://github.com/milanchestojanovic/Bfinder.git --depth 1
#source Bfinder/test/DnBfinder_to_Forest_132X_miniAOD.sh
###### B/D finder in forest v0 ######

###### B/D finder in forest v1 and later ######
git clone -b Dfinder_13XX_miniAOD https://github.com/boundino/Bfinder.git --depth 1
source Bfinder/test/DnBfinder_to_Forest_132X_miniAOD.sh
scram b -j4
mkdir -p dfinder && cp HeavyIonsAnalysis/Configuration/test/forest_miniAOD_run3_DATA_wDfinder.py dfinder/ # taking data as an example
cd dfinder/
###### B/D finder in forest v1 and later ######
# so that you get the latest fixed Bfinder from Jing.

###### fetch the forest setting in the UPC repo ######
git clone https://github.com/ginnocen/UPCopenHFanalysis
cp UPCopenHFanalysis/productions/dataPbPbUPC2023RecoForest/forest_miniAOD_run3_ppRECO_DATA_lowerDcut.py HeavyIonsAnalysis/Configuration/test/
cp UPCopenHFanalysis/productions/dataPbPbUPC2023RecoForest/crabForestTemplateWithEmap_promptReco_base.py HeavyIonsAnalysis/Configuration/test/
cp UPCopenHFanalysis/productions/dataPbPbUPC2023RecoForest/submitScript.sh HeavyIonsAnalysis/Configuration/test/
###### fetch the forest setting in the UPC repo ######

#Rebuild 
scram b	-j8
```

You should now be good to run,

```
cd HeavyIonsAnalysis/Configuration/test
### local test
cmsRun forest_miniAOD_run3_ppRECO_DATA_lowerDcut.py
### crab job
python3 crabForestTemplateWithEmap_promptReco_base.py <run_no> # this script will submit 20 HIForward PDs
```

If this works, build is ready to produce

---
# Forest production
- Forest codes:
  - ~~[forest_miniAOD_run3_ppRECO_DATA.py](forest_miniAOD_run3_ppRECO_DATA.py)~~
    - [v0] Add zdcanalyzer
    - [v1] TDirectory's: ggHiNtuplizer, muonAnalyzerPP, Dfinder w/ more channels, Bfinder, particleFlowAnalyser
    - [v1] Skimmed with good lumi, pprimaryVertexFilter, HLT paths
    - Deprecated since v2
  - [forest_miniAOD_run3_ppRECO_DATA_lowerDcut.py](forest_miniAOD_run3_ppRECO_DATA_lowerDcut.py)
    - [v0] Add zdcanalyzer
    - [v0] Relax track pt, Dpt cuts
    - [v1] TDirectory's: ggHiNtuplizer, muonAnalyzerPP, Dfinder w/ more channels, Bfinder, particleFlowAnalyser
    - [v1] Skimmed with good lumi, pprimaryVertexFilter, HLT paths
    - [v1] Dfinder: pt thresh = 0.2, turn off lambda channel (subject to crab job limitation)
    - [v2] Dfinder cut: trkPt=.5, Dpt=1.5, With MET filters, single EG HLT path
    - [v3] using reRECO dataset
    - [v3] update Dfinder cut: trkPt=.5, Dpt=1, svpvDistanceCut_lowptD=1
    - [v3] using golden json
    - [v3] turn on cluster compatibility filter
    - [v3] move from CMSSW_13_2_4 to CMSSW_13_2_6_patch2
- Crab jobs:
  - For streamer: [crabForestTemplateWithEmap_base.py](crabForestTemplateWithEmap_base.py)
  - For prompt-reco: [crabForestTemplateWithEmap_promptReco_base.py](crabForestTemplateWithEmap_promptReco_base.py)
- Output paths:
  - lxplus: `/eos/cms/store/group/phys_heavyions/yuchenc/run3RapidValidation/`
  - svmithi03: `/home/data/run3RapidValidation/`
- Production history:
  - Streamer:
    | version | run range | note |
    |---|---|---|
    | v0 | run 374719-375195 | only D0 candidate tree |
    | v1 | run 375202-375317 | [bc86464](https://github.com/janice-cat/cmssw/commit/bc86464cc74b8295dd0963bc60848dd2cda99d72) [new] TDirectory's: ggHiNtuplizer, muonAnalyzerPP, Dfinder w/ more channels, Bfinder, particleFlowAnalyser; [new] Skimmed with good lumi, pprimaryVertexFilter, HLT paths; because of crab job memory limits, (1) B finder is turned off or (2) Dfinder: pt thresh = 0.2, turn off lambda channel |

  - Prompt reco:
    | version | run range | note |
    |---|---|---|
    | v1 | run 374804 | [bc86464](https://github.com/janice-cat/cmssw/commit/bc86464cc74b8295dd0963bc60848dd2cda99d72) [new] TDirectory's: ggHiNtuplizer, muonAnalyzerPP, Dfinder w/ more channels, Bfinder, particleFlowAnalyser; [new] Skimmed with good lumi, pprimaryVertexFilter, HLT paths |
    | v2 | run 374804 - run 375202 | [a010239](https://github.com/janice-cat/cmssw/commit/a0102398a65ed9960004a31ab8f9dcb841c305e4) Dfinder cut: trkPt=.5, Dpt=1.5; [baa9991](https://github.com/janice-cat/cmssw/commit/baa999103e4a72dc162417817a6925f0aa81406b) [new] add MET filter TTree; single EG HLT paths |
    | v3 | (runs to be submitted: [project](https://github.com/users/janice-cat/projects/2/views/1)) | [e241320](https://github.com/janice-cat/cmssw/commit/e241320767e23bdd2db04a4e55c3c7bbe3fcfb89), [49eb507](https://github.com/janice-cat/cmssw/commit/49eb50748963ed76c195fa4109358b1639fff2bd) |

- After crab submission, merging the forest files at `svmithi03`:
  1) To check the job status and rename the forest crab directory (@`lxplus`):
  ```bash
  python3 renameCrabDir.py <run_no:integer>
  ``` 
  This will prompt up some questions if the jobs are all done or part of them are failed. One can just hit the corresponding answers
  

  2) After 20 PDs are done and renamed (for a run), one can merge the forest files (@`svmithi03`):
  ```bash
  python3 mergeForest.py <run_no:integer>
  ```
  This will create the following scripts and logs:
  - `/home/data/run3RapidValidation/reReco_run<run>_v3/script/distributeJobs.py`: the mother script to submit parallel jobs for 20 PDs
  - `/home/data/run3RapidValidation/reReco_run<run>_v3/script/mergeJobs_HIForward{PD}.sh`: the atomic merging script. This will be copied to the home directory, and the copied script will be killed once the job is done. So one can monitor the remaining scripts to see which is not done.
  - `/home/data/run3RapidValidation/reReco_run<run>_v3/log/mergingDetails.log`: how the merged forests are batched
  - `/home/data/run3RapidValidation/reReco_run<run>_v3/log/mergeJobs_HIForward{PD}_forest{num}.log`: the hadd history for each merged forest file
