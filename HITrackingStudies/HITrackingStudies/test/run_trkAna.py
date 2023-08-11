import FWCore.ParameterSet.Config as cms

process = cms.Process('TRACKANA')
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# mode = 0 # 124X_dataRun3_Prompt_v10
# mode = 1 # 124X_dataRun3_Prompt_frozen_v5
# mode = 2 # New PR
# mode = 3 # Raw_15
mode = 4 # RawPrime_15

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('trk_prompt_v10.root') if mode==0 else 
               cms.string('trk_prompt_frozen_v5.root') if mode==1 else 
               cms.string('trk_newPR.root') if mode==2 else
               cms.string('trk_raw_15.root') if mode==3 else
               cms.string('trk_rawprime_15.root')
)

# Input source
process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    # fileNames =  cms.untracked.vstring('file:/afs/cern.ch/work/m/mnguyen/public/prod/CMSSW_12_5_2/src/rawprime/raw_RAW2DIGI_L1Reco_RECO_run362321_evt79323292.root'),
    # fileNames =  cms.untracked.vstring('file:/afs/cern.ch/work/m/mnguyen/public/prod/CMSSW_12_5_2/src/rawprime/offlineRawprime_RAW2DIGI_L1Reco_RECO.root'),
    # fileNames =  cms.untracked.vstring('file:/afs/cern.ch/work/m/mnguyen/public/prod/CMSSW_12_5_2/src/rawprime/raw_RAW2DIGI_L1Reco_RECO.root'),
    # fileNames =  cms.untracked.vstring('file:/eos/user/y/yuchenc/rawprime/CMSSW_12_5_2/src/RecoLocalTracker/SiStripClusterizer/test/rawprime_RAW2DIGI_L1Reco_RECO_overwrite.root'),
    # fileNames =  cms.untracked.vstring('file:/eos/user/y/yuchenc/0518/CMSSW_12_5_2/src/RecoLocalTracker/SiStripClusterizer/test/rawprime_RAW2DIGI_L1Reco_RECO_overwrite.root'),
    # fileNames =  cms.untracked.vstring('file:/afs/cern.ch/work/m/mnguyen/public/prod/CMSSW_12_5_2/src/rawprime/repack_REPACK.root'),
    # fileNames =  cms.untracked.vstring('file:/afs/cern.ch/user/y/yuchenc/0518/CMSSW_13_0_6/src/RecoLocalTracker/SiStripClusterizer/data/Raw_53.root'),
    # fileNames =  cms.untracked.vstring('file:/afs/cern.ch/user/y/yuchenc/0518/CMSSW_13_0_6/src/RecoLocalTracker/SiStripClusterizer/data/RawPrime_53.root'),
    # fileNames =  cms.untracked.vstring('file:/eos/cms/store/group/phys_heavyions/mnguyen/rawprime/raw_RAW2DIGI_L1Reco_RECO.root')
    fileNames =  cms.untracked.vstring('file:/afs/cern.ch/user/y/yuchenc/rawprime_cmssw/CMSSW_12_5_2/src/RecoLocalTracker/SiStripClusterizer/test/rawprime_RAW2DIGI_L1Reco_RECO_prompt_v10.root') if mode==0 else 
                 cms.untracked.vstring('file:/afs/cern.ch/user/y/yuchenc/rawprime_cmssw/CMSSW_12_5_2/src/RecoLocalTracker/SiStripClusterizer/test/rawprime_RAW2DIGI_L1Reco_RECO_prompt_frozen_v5.root') if mode==1 else
                 cms.untracked.vstring('file:/afs/cern.ch/user/y/yuchenc/rawprime_cmssw/CMSSW_12_5_2/src/RecoLocalTracker/SiStripClusterizer/test/rawprime_RAW2DIGI_L1Reco_RECO_newPR.root') if mode==2 else
                 cms.untracked.vstring('file:/eos/user/y/yuchenc/0518/CMSSW_13_0_6/src/RecoLocalTracker/SiStripClusterizer/data/Raw_15.root') if mode==3 else
                 cms.untracked.vstring('file:/eos/user/y/yuchenc/0518/CMSSW_13_0_6/src/RecoLocalTracker/SiStripClusterizer/data/RawPrime_15.root')
    # eventsToProcess = cms.untracked.VEventRange("362321:160502249-362321:160502249"),
)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2022_realistic_hi', '')
###

#forest style analyzers (anaTrack module) (not affected by HITrackCorrections code)
process.load('HITrackingStudies.AnalyzerCode.trackAnalyzer_cff')
process.anaTrack.doSimVertex = False
process.anaTrack.doMVA = False
process.anaTrack.doSimTrack = False
# process.anaTrack.trackSrc = "hiConformalPixelTracks"
###

process.p = cms.Path(
                      process.anaTrack
)
