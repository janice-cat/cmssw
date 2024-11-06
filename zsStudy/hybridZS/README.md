- Production workflow
  - CMSSW version: `CMSSW_14_1_1`
  - Step1) HLT
    - Config srcipt ([hlt_cfg.py](hlt_cfg.py))  
      is based on `hltGetConfiguration /users/soohwan/HLT_141X/TrackerZS/HLT_ZBMBRawPrime/V1 --process MYHLT --full --offline --data --type HIon --unprescale --globaltag 141X_dataRun3_HLT_v1 --max-events 1000 --output all`.
    - Crab config script ([hltSubmitHITrackerNZS.py](hltSubmitHITrackerNZS.py))
      - `inputDataset` now is set to 2023 HITrackerNZS PD ([this line](hltSubmitHITrackerNZS.py#L23))
      - **One will need to manually modify the PD to run on the 2024 PbPb data**
      - **One might need to modify the storageSite to the one that you have the write permint** ([this line](hltSubmitHITrackerNZS.py#L36))

  - Step2) RECO
    - Config script ([recoPbPbprime2mini_RAW2DIGI_L1Reco_RECO.py](recoPbPbprime2mini_RAW2DIGI_L1Reco_RECO.py))  
      is based on `cmsDriver.py recoPbPbprime2mini --conditions 141X_dataRun3_Prompt_v3 -s RAW2DIGI,L1Reco,RECO --datatier AOD --eventcontent AOD --data  --process reRECO --scenario pp --customise Configuration/DataProcessing/RecoTLR.customisePostEra_Run3 --no_exec --era Run3_pp_on_PbPb_approxSiStripClusters_2024 --repacked`
    - Crab config script ([recoSubmitHITrackerNZS.py](recoSubmitHITrackerNZS.py))
      - **One will need to manually specify the `inputDataset` that the reco step would run on** ([this line](recoSubmitHITrackerNZS.py#L23)). This field will be the output dataset of the HLT step
      - **One might need to modify the storageSite to the one that you have the write permint** ([this line](recoSubmitHITrackerNZS.py#L34))
    
  - Step3) Forest/trackTree
    - Setup: https://github.com/RAGHUMATAPITA/2024HIRunNtupleTest/tree/14_1_3
    - One can follow the readme to build the tracking group repo. Please set up for the production with the version `CMSSW_14_1_1`
    - I will suggest to use my modified config script ([run_PbPb_cfg.py](run_PbPb_cfg.py)).
      Here is how I setup the forest in this directory
      ```bash
      cmsrel CMSSW_14_1_1
      cd CMSSW_14_1_1/src
      cmsenv

      ### under CMSSW_14_1_1/src/
      git clone -b 14_1_3 git@github.com:RAGHUMATAPITA/2024HIRunNtupleTest.git .
      mv 2024HIRunNtupleTest/HITrackingStudies ./
      scram b -j 8

      ### copy the essential scripts for the forest production under the zsStudy/hybridZS/ folder
      cp HITrackingStudies/HITrackingStudies/test/CentralityTable_HFtowers200_DataPbPb_periHYDJETshape_run3v1302x04_offline_Nominal.db zsStudy/hybridZS/ 
      cp HITrackingStudies/HITrackingStudies/test/pbpb.py zsStudy/hybridZS/

      cd zsStudy/hybridZS/
      cmsRun run_PbPb_cfg.py # run things locally
      crab submit -c forestSubmitHITrackerNZS.py
      ```  
      
      <details>
        <summary> I change the default option of 'sample' to be 'Data_Reco_AOD', and that of 'n' to be '-1. Because I don't know how to parse the optional arguments in the crab script 😅
      For the output name, I change it to be 'GeneralTracks.root'`. </summary>
        <img width="1020" alt="截圖 2024-11-06 12 42 16" src="https://github.com/user-attachments/assets/9e2efafa-5bed-45da-9140-6c62ace39472">
      </details>
      
      - **One will need to manually specify the `inputDataset` that the reco step would run on** ([this line](forestSubmitHITrackerNZS#L38)). This field will be the output dataset of the HLT step
      - **One will need to modify the `outLFNDirBase` on `eos`** ([this line](forestSubmitHITrackerNZS#L53))
