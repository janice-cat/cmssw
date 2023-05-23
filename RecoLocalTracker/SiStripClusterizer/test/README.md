### Reading out cluster info from Raw RECO file
- Steering file: [readout_RECO_Raw.py](readout_RECO_Raw.py)
	- Input: `/HITestRaw6/phys_heavyions_ops-crab_Raw_Filtered_FEVT_March20_v2-791d174b6f0532ee9d9680f5a2c2df80/USER` [edmEventSize](../data/Raw_edmEventSize.txt)  
		> I downloaded one of the [file](../data/Raw_53.root) from DAS for now, just for the convenience of developing the code. I'll change it to the xrootd afterwards so as to read the whole dataset.
	- Output: `Raw_53_trimmed.root`, `Raw_53_clusterNtuple.root`
- Analyzer: [SiStripClustersDump.cc](SiStripClustersDump.cc)
	- InputTag: siStripClusters
	- Output: `clusters` calculated by [SiStripCluster.h](https://github.com/janice-cat/cmssw/blob/master/DataFormats/SiStripCluster/interface/SiStripCluster.h) with branches `event`, `detId`, `barycenter`, `charge`
- Commands:
```bash
scram b -j8
cmsRun readout_RECO_Raw.py
root -l Raw_53_clusterNtuple.root
root [1] SiStripClustersDump->cd()
root [2] clusters->Draw("barycenter")               
root [3] clusters->Draw("charge")
```