# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: repack --scenario pp --conditions auto:run3_data_prompt -s REPACK:DigiToApproxClusterRaw --datatier GEN-SIM-DIGI-RAW-HLTDEBUG --eventcontent REPACKRAW --era Run3_pp_on_PbPb -n 10 --procModifiers approxSiStripClusters --repacked --process REHLT --filein /store/hidata/HIRun2022A/HITestRaw6/RAW/v1/000/362/321/00000/76c3e7a8-896e-4671-9563-d6c596da5252.root --customise_commands process.rawPrimeDataRepacker.inputTag='rawDataRepacker'
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_pp_on_PbPb_cff import Run3_pp_on_PbPb
from Configuration.ProcessModifiers.approxSiStripClusters_cff import approxSiStripClusters

process = cms.Process('REHLT',Run3_pp_on_PbPb,approxSiStripClusters)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.DigiToRaw_Repack_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.StandardSequences.RawToDigi_DataMapper_cff')  # for testing

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('root://xrootd-cms.infn.it//store/hidata/HIRun2022A/HITestRaw6/RAW/v1/000/362/321/00000/76c3e7a8-896e-4671-9563-d6c596da5252.root'),
    secondaryFileNames = cms.untracked.vstring(),
                            eventsToProcess = cms.untracked.VEventRange("362321:79323292-362321:79323292"),
)

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
    annotation = cms.untracked.string('repack nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.REPACKRAWoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RAW-HLTDEBUG'),
        filterName = cms.untracked.string('')
    ),
                                           #fileName = cms.untracked.string('repack_REPACK_hltGT.root'),
                                           fileName = cms.untracked.string('repack_REPACK.root'),
    outputCommands = process.REPACKRAWEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run3_data_prompt', '')
process.GlobalTag = GlobalTag(process.GlobalTag, '124X_dataRun3_Prompt_v10','')
#process.GlobalTag = GlobalTag(process.GlobalTag, '124X_dataRun3_HLT_v7','')
useHLTSiStripTags = False
if useHLTSiStripTags:
    print ('using siStrip HLT tags')
    process.GlobalTag.toGet.append(
        cms.PSet(
            record = cms.string("SiStripDetVOffRcd"),
            tag = cms.string('SiStripDetVOff_GR10_v1_hlt'),
        )
    )
    process.GlobalTag.toGet.append(
        cms.PSet(
            record = cms.string("SiStripBadFiberRcd"),
            tag = cms.string('SiStripBadChannel_FromOfflineCalibration_GR10_v1_hlt'),
        )
    )
    process.REPACKRAWoutput.fileName = 'repack_REPACK_modTag.root'

# Path and EndPath definitions
#process.load("RecoLocalTracker.SiStripClusterizer.SiStripApprox2Clusters_cfi")
#process.digi2repack_step = cms.Path(process.DigiToApproxClusterRaw*process.SiStripApprox2Clusters)
process.digi2repack_step = cms.Path(process.DigiToApproxClusterRaw)
process.raw2digi_step = cms.Path(process.RawToDigi)  #adding this for testing
process.endjob_step = cms.EndPath(process.endOfProcess)
process.REPACKRAWoutput_step = cms.EndPath(process.REPACKRAWoutput)

# Schedule definition
process.schedule = cms.Schedule(process.digi2repack_step,process.endjob_step,process.REPACKRAWoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

from Configuration.Applications.ConfigBuilder import MassReplaceInputTag
MassReplaceInputTag(process, new="rawDataMapperByLabel", old="rawDataCollector")



# Customisation from command line

process.rawPrimeDataRepacker.inputTag='rawDataRepacker'
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
