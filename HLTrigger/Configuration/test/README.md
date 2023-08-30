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
- Output: `step2clusters.root`


