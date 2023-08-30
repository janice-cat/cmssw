## Generating RAW' approximated clusters with HLT menu:
- Command:
```bash
cmsRun ZDCTestRawPrime.py
```
- Output: `outputDQM.root`
## Generating RAW clusters with RECO:
- Command:
```bash
cmsRun step2_RAW2DIGI_L1Reco_RECO.py
```
> `step2_RAW2DIGI_L1Reco_RECO.py` is obtained based on `runTheMatrix.py -l 140.56 -n -e`
- Taking `outputDQM.root` and producing `step2clusters.root`, which will contain branches: `hltSiStripClusterizerForRawPrime`, `hltSiStripClusters2ApproxClusters`, `siStripClusters`.

