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
    input = cms.untracked.int32(200),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# mode = 0 # 124X_dataRun3_Prompt_v10
# mode = 1 # 124X_dataRun3_Prompt_frozen_v5
mode = 2 # New PR

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('root://xrootd-cms.infn.it//store/hidata/HIRun2022A/HITestRaw6/RAW/v1/000/362/321/00000/76c3e7a8-896e-4671-9563-d6c596da5252.root'),
    secondaryFileNames = cms.untracked.vstring(),
    eventsToProcess = cms.untracked.VEventRange(
"362321:77471870-362321:77471870",
"362321:77614816-362321:77614816",
"362321:77612179-362321:77612179",
"362321:77869127-362321:77869127",
"362321:77866568-362321:77866568",
"362321:77525656-362321:77525656",
"362321:77503263-362321:77503263",
"362321:77584805-362321:77584805",
"362321:77451418-362321:77451418",
"362321:77463987-362321:77463987",
"362321:77445121-362321:77445121",
"362321:77915832-362321:77915832",
"362321:77698576-362321:77698576",
"362321:77498346-362321:77498346",
"362321:77666942-362321:77666942",
"362321:77473008-362321:77473008",
"362321:77518971-362321:77518971",
"362321:77789262-362321:77789262",
"362321:77903254-362321:77903254",
"362321:77769702-362321:77769702",
"362321:77798053-362321:77798053",
"362321:77798063-362321:77798063",
"362321:78203432-362321:78203432",
"362321:78030954-362321:78030954",
"362321:78116372-362321:78116372",
"362321:78264218-362321:78264218",
"362321:78202898-362321:78202898",
"362321:78129342-362321:78129342",
"362321:78217091-362321:78217091",
"362321:78413674-362321:78413674",
"362321:78022959-362321:78022959",
"362321:77936717-362321:77936717",
"362321:78314131-362321:78314131",
"362321:78190797-362321:78190797",
"362321:78370183-362321:78370183",
"362321:78341701-362321:78341701",
"362321:78017002-362321:78017002",
"362321:78082245-362321:78082245",
"362321:78036362-362321:78036362",
"362321:77990845-362321:77990845",
"362321:78352572-362321:78352572",
"362321:78351744-362321:78351744",
"362321:78185938-362321:78185938",
"362321:78241683-362321:78241683",
"362321:78552077-362321:78552077",
"362321:78785902-362321:78785902",
"362321:78608689-362321:78608689",
"362321:78784677-362321:78784677",
"362321:78466877-362321:78466877",
"362321:78762191-362321:78762191",
"362321:78829929-362321:78829929",
"362321:78749174-362321:78749174",
"362321:78818443-362321:78818443",
"362321:78755877-362321:78755877",
"362321:78645020-362321:78645020",
"362321:78915693-362321:78915693",
"362321:78878308-362321:78878308",
"362321:78444575-362321:78444575",
"362321:78658410-362321:78658410",
"362321:78681141-362321:78681141",
"362321:78843464-362321:78843464",
"362321:78660213-362321:78660213",
"362321:78676374-362321:78676374",
"362321:78852478-362321:78852478",
"362321:78673440-362321:78673440",
"362321:79655426-362321:79655426",
"362321:79898538-362321:79898538",
"362321:79712138-362321:79712138",
"362321:79853750-362321:79853750",
"362321:79769187-362321:79769187",
"362321:79564298-362321:79564298",
"362321:79620817-362321:79620817",
"362321:79754526-362321:79754526",
"362321:79854072-362321:79854072",
"362321:79418699-362321:79418699",
"362321:79606901-362321:79606901",
"362321:79493595-362321:79493595",
"362321:79472422-362321:79472422",
"362321:79640858-362321:79640858",
"362321:79463405-362321:79463405",
"362321:79637660-362321:79637660",
"362321:79426450-362321:79426450",
"362321:79708581-362321:79708581",
"362321:79553205-362321:79553205",
"362321:79670874-362321:79670874",
"362321:79852720-362321:79852720",
"362321:79687433-362321:79687433",
"362321:79602954-362321:79602954",
"362321:79731454-362321:79731454",
"362321:79708515-362321:79708515",
"362321:79323292-362321:79323292",
"362321:79175052-362321:79175052",
"362321:79366256-362321:79366256",
"362321:79279110-362321:79279110",
"362321:79191124-362321:79191124",
"362321:78920966-362321:78920966",
"362321:78920522-362321:78920522",
"362321:79031410-362321:79031410",
"362321:79345490-362321:79345490",
"362321:78988194-362321:78988194",
"362321:78932485-362321:78932485",
"362321:79154873-362321:79154873",
"362321:79236346-362321:79236346",
"362321:79099067-362321:79099067",
"362321:79111098-362321:79111098",
"362321:79003018-362321:79003018",
"362321:78991287-362321:78991287",
"362321:79084955-362321:79084955",
"362321:79015200-362321:79015200",
"362321:79025205-362321:79025205",
"362321:79062184-362321:79062184",
"362321:79313938-362321:79313938",
                        ),
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
                                           fileName = cms.untracked.string('repack_REPACK_prompt_v10.root' if mode==0 else
                                                                           'repack_REPACK_prompt_frozen_v5.root' if mode==1 else
                                                                           'repack_REPACK_newPR.root' if mode==2 else 
                                                                           'repack_REPACK.root'),
    outputCommands = process.REPACKRAWEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run3_data_prompt', '')
process.GlobalTag = GlobalTag(process.GlobalTag, '124X_dataRun3_Prompt_v10','') if mode == 0 else \
                    GlobalTag(process.GlobalTag, '124X_dataRun3_Prompt_frozen_v5','')
# process.GlobalTag = GlobalTag(process.GlobalTag, '124X_dataRun3_Prompt_v5','')
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

if mode==2:
    process.REPACKRAWoutput.outputCommands+=cms.untracked.vstring(
        'keep DetIdedmEDCollection_siStripDigisHLT_*_*'
    )

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
