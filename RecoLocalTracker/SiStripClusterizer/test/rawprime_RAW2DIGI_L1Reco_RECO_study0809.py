# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step3 --conditions auto:run3_data_prompt -s RAW2DIGI,L1Reco,RECO --datatier FEVTDEBUGHLT --eventcontent FEVTDEBUGHLT --data --process reRECO --scenario pp -n 1 --repacked --era Run3_pp_on_PbPb_approxSiStripClusters --no_exec --filein /store/hidata/HIRun2022A/HITestRawPrime6/RAW/v1/000/362/321/00000/0586f6b3-0298-4f2b-a159-de91e51004d0.root
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_pp_on_PbPb_approxSiStripClusters_cff import Run3_pp_on_PbPb_approxSiStripClusters

process = cms.Process('reRECO',Run3_pp_on_PbPb_approxSiStripClusters)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_DataMapper_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(50),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

useHLTSiStripTags = False
# mode = 0 # 124X_dataRun3_Prompt_v10
# mode = 1 # 124X_dataRun3_Prompt_frozen_v5
mode = 2 # New PR


# Input source
process.source = cms.Source("PoolSource",
                            # fileNames = cms.untracked.vstring('root://xrootd-cms.infn.it//store/hidata/HIRun2022A/HITestRawPrime6/RAW/v1/000/362/321/00000/0586f6b3-0298-4f2b-a159-de91e51004d0.root'),
                            fileNames = cms.untracked.vstring('file:./repack_REPACK_prompt_v10.root' if mode==0 else 
                                                              'file:./repack_REPACK_prompt_frozen_v5.root' if mode==1 else 
                                                              'file:./repack_REPACK_newPR.root' if mode==2 else 
                                                              'file:./repack_REPACK.root'),
                            secondaryFileNames = cms.untracked.vstring(),
                            # eventsToProcess = cms.untracked.VEventRange("362321:79323292-362321:79323292"),
)

if useHLTSiStripTags:
    process.source.fileNames = cms.untracked.vstring('file:./repack_REPACK_modTag.root')


process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    makeTriggerResults = cms.obsolete.untracked.bool,
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step3 nevts:1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('FEVTDEBUGHLT'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('rawprime_RAW2DIGI_L1Reco_RECO_prompt_v10.root' if mode==0 else 
                                    'rawprime_RAW2DIGI_L1Reco_RECO_prompt_frozen_v5.root' if mode==1 else
                                    'rawprime_RAW2DIGI_L1Reco_RECO_newPR.root' if mode==2 else
                                    'rawprime_RAW2DIGI_L1Reco_RECO.root'),
    outputCommands = process.FEVTDEBUGHLTEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)
if useHLTSiStripTags:
    process.FEVTDEBUGHLToutput.fileName = cms.untracked.string('rawprime_RAW2DIGI_L1Reco_RECO_modTag.root')

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
# process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run3_data_prompt', '')
process.GlobalTag = GlobalTag(process.GlobalTag, '124X_dataRun3_Prompt_v10','') if mode == 0 else \
                    GlobalTag(process.GlobalTag, '124X_dataRun3_Prompt_frozen_v5','')
# process.GlobalTag = GlobalTag(process.GlobalTag, '124X_dataRun3_Prompt_v10','')
# process.GlobalTag = GlobalTag(process.GlobalTag, '124X_dataRun3_Prompt_v5','')

# Path and EndPath definitions
if mode==2: 
    process.RawToDigiTask.remove(process.siStripDigis)
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
if mode==2:
    process.MeasurementTrackerEvent.inactiveStripDetectorLabels = cms.VInputTag("siStripDigisHLT") 
    process.MeasurementTrackerEventPreSplitting.inactiveStripDetectorLabels = cms.VInputTag("siStripDigisHLT")
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.endjob_step,process.FEVTDEBUGHLToutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

from Configuration.Applications.ConfigBuilder import MassReplaceInputTag
MassReplaceInputTag(process, new="rawDataMapperByLabel", old="rawDataCollector")

#Setup FWK for multithreaded                                                                                                                                                                               
  
process.options.numberOfThreads = 8
process.options.numberOfStreams = 0

# Customisation from command line
process.FEVTDEBUGHLToutput.outputCommands.extend(['keep recoTracks_*_*_*'])
process.FEVTDEBUGHLToutput.outputCommands.extend(['keep recoVertexs_*_*_*'])
process.FEVTDEBUGHLToutput.outputCommands.extend(['keep *_pixelPair*_*_*'])
if mode==2:
    process.FEVTDEBUGHLToutput.outputCommands.extend(['keep TrackCandidate_*_*_*'])
    process.FEVTDEBUGHLToutput.outputCommands.extend(['keep *TrackCandidate_*_*_*'])
#process.pixelPairStep.qualityCuts = (-1.,0.0,0.98)
#process.pixelPairStepTrackCandidates.useHitsSplitting = False
#process.pixelPairStepClusters.maxChi2 = 0.
#Have logErrorHarvester wait for the same EDProducers to finish as those providing data for the OutputModule
from FWCore.Modules.logErrorHarvester_cff import customiseLogErrorHarvesterUsingOutputCommands
process = customiseLogErrorHarvesterUsingOutputCommands(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
