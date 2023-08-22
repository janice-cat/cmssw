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
	#### modify the track analyzer (to get printout)
	cp -f <https://github.com/CmsHI/rawprime/blob/main/HITrackingStudies/AnalyzerCode/TrackAnalyzer.cc> HITrackingStudies/AnalyzerCode/src/TrackAnalyzer.cc
	cp <https://github.com/CmsHI/rawprime/blob/main/HITrackingStudies/HITrackingStudies/run_trkAna.py> HITrackingStudies/HITrackingStudies/test/

	### compile
	scram b -j8 
	```

	> `ls <cmssw-repo-path>/CMSSW_12_5_2/src/`:
 
	```bash
	DataFormats/  HITrackingStudies@  README-rawprime.md  RecoLocalTracker/
	```

## Produce FEVT level file
```bash
cd RecoLocalTracker/SiStripClusterizer/test/
### raw (online)
cmsRun raw_RAW2DIGI_L1Reco_RECO.py

### rawprime (repack)
cmsRun repack_REPACK.py
cmsRun rawprime_RAW2DIGI_L1Reco_RECO.py
```

### [Temp] studying the un-associated cluster (July 18th)
[in DataFormats/SiStripCluster/src/SiStripCluster.cc](https://github.com/janice-cat/cmssw/commit/7502e043d8baa7c3d2817e29b734300df8bbdf17#diff-6d30f00290537b874138bf32e5d7123442b7cac0a3bb907fbcd84dc8a2a4e7aaR25-R37)

runing the rawprime repack can get the modified approx-cluster


## Run track analyzer
```bash
cd HITrackingStudies/HITrackingStudies/test/
cmsRun run_trkAna.py
```
- Note: parse the input file [here](https://github.com/CmsHI/rawprime/blob/main/HITrackingStudies/HITrackingStudies/run_trkAna.py#L26)


## [Ongoing] track-level checks: online RAW v.s. offline RAW' + [PR #42475](https://github.com/cms-sw/cmssw/pull/42475)
```bash
### get the new offline FEVT level file
cd RecoLocalTracker/SiStripClusterizer/test/
cmsRun repack_REPACK_study0809.py
##### I did a stupid event filtering, which could be made more general: https://github.com/janice-cat/cmssw/blob/d4165cb5f207ca0b7301d8b5e9f521b670c2c17b/RecoLocalTracker/SiStripClusterizer/test/repack_REPACK_study0809.py#L36-L153
##### Need to specify by hand: https://github.com/janice-cat/cmssw/blob/d4165cb5f207ca0b7301d8b5e9f521b670c2c17b/RecoLocalTracker/SiStripClusterizer/test/repack_REPACK_study0809.py#L31-L33
cmsRun rawprime_RAW2DIGI_L1Reco_RECO_study0809.py
##### Need to specify by hand: https://github.com/janice-cat/cmssw/blob/mydev-CMSSW_12_5_2/RecoLocalTracker/SiStripClusterizer/test/rawprime_RAW2DIGI_L1Reco_RECO_study0809.py#L31-L33

### get the new offline trackTree
##### I just added HITrackingStudies to THIS repo, which might make sharing codes easier 
cd HITrackingStudies/HITrackingStudies/test/
cmsRun run_trkAna.py
##### Need to specify by hand: https://github.com/janice-cat/cmssw/blob/6fc7bb0c635a06b7ce30995768a9efa95ad0b412/HITrackingStudies/HITrackingStudies/test/run_trkAna.py#L11-L15

### One can plot the track-level variables from trackTree outputs, e.g. trk_raw_15.root (online raw), trk_newPR.root (offline RAW' + PR #42475) 
```
