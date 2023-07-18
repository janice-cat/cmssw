# RawPrime study

## Settings
- CMSSW version: CMSSW_12_5_2
```bash
### source CMSSW version
cmsrel CMSSW_12_5_2
cd CMSSW_12_5_2/src/
cmsenv

### Add packages
git cms-addpkg DataFormats/SiStripCluster 			## cluster <-> approx cluster
git cms-addpkg RecoLocalTracker/SiStripClusterizer		## SiStripClusterizer

cd <somewhere>
git clone git@github.com:CesarBernardes/TrackingCode.git 	## track analyzer
git checkout -b CMSSW_12_5_0_trkAnalysis origin/CMSSW_12_5_0_trkAnalysis 
cd <cmssw-repo-path>/CMSSW_12_5_2/src/
ln -s <somewhere>/TrackingCode/HITrackingStudies ./

### compile
scram b -j8 
```