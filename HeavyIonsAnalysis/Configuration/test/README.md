2023.10.03 [Please refer to this repo:dir for all info](https://github.com/cfmcginn/production/tree/main/HIRun2023/forestPPRef)
# General building instruction
Some small amount of files for getting the forest to run w/ the pp RECO miniAOD

To build with the forest, start by following:
https://twiki.cern.ch/twiki/bin/view/CMS/HiForestSetup#Setup_for_13_2_X_2023_PbPb_data

```
cmsrel CMSSW_13_2_4
cd CMSSW_13_2_4/src
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

#Add the B finder
#Based on:
#https://github.com/jusaviin/HiForestSetupPbPbRun2023#test-the-configuration
git clone -b 13XX_miniAOD https://github.com/milanchestojanovic/Bfinder.git --depth 1
source Bfinder/test/DnBfinder_to_Forest_132X_miniAOD.sh

#Rebuild 
scram b	-j8
```

You should now be good to run,

```
cd HeavyIonsAnalysis/Configuration/test
cmsRun forest_miniAOD_run3_ppRECO_DATA.py
```

If this works, build is ready to produce


---
# Forest production
- Forest codes:
  - [forest_miniAOD_run3_ppRECO_DATA.py](forest_miniAOD_run3_ppRECO_DATA.py)
    - Add zdcanalyzer
  - [forest_miniAOD_run3_ppRECO_DATA_lowerDcut.py](forest_miniAOD_run3_ppRECO_DATA_lowerDcut.py)
    - Add zdcanalyzer
    - Relax track pt, Dpt cuts
- Crab jobs:
  - [crabForestTemplateWithEmap.py](crabForestTemplateWithEmap.py)
- Output paths:
  - lxplus: `/eos/cms/store/group/phys_heavyions/yuchenc/run3RapidValidation/`
  - svmithi03: `/home/data/run3RapidValidation/`
- Production history:
  | version | run range | note |
  |---|---|---|
  | v0 | run 374719-375195 | only D0 candidate tree |
