# MC productions for peripheral PbPb Hydjet events

## MC productions for peripheral PbPb Hydjet events and reconstruction in CMSSW with pp RECO 
### Build your area in CMSSW_13_2_10
```
cmsrel CMSSW_13_2_10
cd CMSSW_13_2_10/src
cmsenv
git cms-init

git cms-merge-topic cfmcginn:pyt8PhotonFlux_13_2_X
git remote add cfmcginn https://github.com/cfmcginn/cmssw.git

#Will need to move the fragment here
git cms-addpkg Configuration/Generator

```


### 2) GEN-SIM step
- Run the driver command:
```
cmsDriver.py Configuration/GenProduction/python/HIN-HINPbPbSpring23GS-00015-fragment.py --python_filename HIN-HINPbPbSpring23GS-00015_bMin15_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:HIN-HINPbPbSpring23GS-00015_bMin15.root --conditions 130X_mcRun3_2023_realistic_HI_v18 --beamspot Realistic2023PbPbCollision --step GEN,SIM --scenario HeavyIons --geometry DB:Extended --era Run3_pp_on_PbPb --no_exec --mc -n 100000
```
- Modify the cfg script to produce only the impact-parameter-biased sample by adding [this line](HIN-HINPbPbSpring23GS-00015_bMin15_cfg.py#L277):
`process.generator.bMin = 15.`

