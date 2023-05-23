### Reading out cluster info from Raw RECO file
- Steering file: [readout_RECO_SiStripCluster.py](readout_RECO_SiStripCluster.py)
	- Input: `/HITestRaw6/phys_heavyions_ops-crab_Raw_Filtered_FEVT_March20_v2-791d174b6f0532ee9d9680f5a2c2df80/USER` [edmEventSize](../data/Raw_edmEventSize.txt)  
		> I downloaded one of the file (/afs/cern.ch/user/y/yuchenc/0518/CMSSW_13_0_6/src/RecoLocalTracker/SiStripClusterizer/data/Raw_53.root) from DAS for now, just for the convenience of developing the code. I'll change it to the xrootd afterwards so as to read the whole dataset.
	- Output: `output/*_clusterTrimmed.root`, `output/*_clusterNtuple.root`
- Analyzer: [SiStripClustersDump.cc](SiStripClustersDump.cc)
	- InputTag: siStripClusters
	- Output: `clusters` calculated by [SiStripCluster.h](https://github.com/janice-cat/cmssw/blob/master/DataFormats/SiStripCluster/interface/SiStripCluster.h) with branches `event`, `detId`, `barycenter`, `charge`

### Reading out cluster info from Raw' RECO file
- Steering file: [readout_RECO_SiStripApproxCluster.py](readout_RECO_SiStripApproxCluster.py)
	- Output: `output/*_approxClusterTrimmed.root`, `output/*_approxClusterNtuple.root`
- Analyzer: [SiStripApproximatedClustersDump.cc](SiStripApproximatedClustersDump.cc)
	- InputTag: siStripClusters
	- Output: `clusters` calculated by [SiStripApproximateCluster.h](https://github.com/janice-cat/cmssw/blob/master/DataFormats/SiStripCluster/interface/SiStripApproximateCluster.h) with branches `event`, `detId`, `barycenter`, `width`, `charge`

### Commands:
```bash
scram b -j8
cmsRun readout_RECO_SiStripCluster.py
cmsRun readout_RECO_SiStripApproxCluster.py
root -l Raw_53_clusterNtuple.root
root [1] SiStripClustersDump->cd()
root [2] clusters->Draw("barycenter")               
root [3] clusters->Draw("charge")
```
