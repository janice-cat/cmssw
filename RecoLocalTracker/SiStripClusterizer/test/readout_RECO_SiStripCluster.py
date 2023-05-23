# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step2 --conditions 103X_dataRun2_Prompt_v2 -s RAW2DIGI,L1Reco,RECO --process reRECO -n 30 --data --era Run2_2018_pp_on_AA --eventcontent AOD --runUnscheduled --scenario pp --datatier AOD --repacked --filein file:out.root --fileout file:step2.root --no_exec
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
from Configuration.StandardSequences.Eras import eras

import os

process = cms.Process('reRECO3',eras.Run2_2018_pp_on_AA)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_DataMapper_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

options = VarParsing.VarParsing ('analysis')

# Input source
filename = "/afs/cern.ch/user/y/yuchenc/0518/CMSSW_13_0_6/src/RecoLocalTracker/SiStripClusterizer/data/Raw_53.root" if len(options.inputFiles)==0 else \
           options.inputFiles[0]
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:'+filename),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step2 nevts:30'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition
if (not os.path.exists('output/')): os.makedirs('output/')

process.outputClusters = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('ZLIB'),
    compressionLevel = cms.untracked.int32(7),
    eventAutoFlushCompressedSize = cms.untracked.int32(31457280),
    fileName = cms.untracked.string('file:output/{:s}_clusterTrimmed.root'.format( os.path.basename(filename).strip('.root')) ),
    outputCommands = cms.untracked.vstring(
    'drop *',   
	'keep *_*siStripClusters*_*_*'   
    )
)

process.TFileService = cms.Service("TFileService",
        fileName=cms.string("output/{:s}_clusterNtuple.root".format( os.path.basename(filename).strip('.root')) ))

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '103X_dataRun2_Prompt_v2', '')
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

process.SiStripClustersDump = cms.EDAnalyzer("SiStripClustersDump",
    SiStripClustersTag = cms.InputTag("siStripClusters")
)

# Path and EndPath definitions
process.analyzer_step = cms.Path(process.SiStripClustersDump) 
process.endjob_step = cms.EndPath(process.endOfProcess)
process.output_step = cms.EndPath(process.outputClusters)

process.load('EventFilter.SiStripRawToDigi.SiStripDigiToRaw_cfi')
process.rawStep = process.SiStripDigiToRaw.clone(
InputDigis=cms.InputTag('siStripDigis', 'ZeroSuppressed'),
RawDataTag = cms.InputTag('StripRawDataCollector')
 )

process.load('EventFilter.RawDataCollector.rawDataCollector_cfi')
process.StripRawDataCollector = process.rawDataCollector.clone(RawCollectionList = cms.VInputTag( cms.InputTag('rawStep')))

process.load('EventFilter.SiPixelRawToDigi.SiPixelDigiToRaw_cfi')
process.rawStepPix = process.siPixelRawData.clone(
InputLabel=cms.InputTag('siPixelDigis'),
 )
process.PixelRawDataCollector = process.rawDataCollector.clone(RawCollectionList = cms.VInputTag( cms.InputTag('rawStepPix')))

process.load('EventFilter.HcalRawToDigi.HcalDigiToRaw_cfi')
process.rawStepHCAL = process.hcalRawDataVME.clone(
    HBHE = cms.untracked.InputTag("hcalDigis"),
    HF = cms.untracked.InputTag("hcalDigis"),
    HO = cms.untracked.InputTag("hcalDigis"),
    ZDC = cms.untracked.InputTag("hcalDigis"),
    TRIG =  cms.untracked.InputTag("hcalDigis")
)
process.HCALRawDataCollector = process.rawDataCollector.clone(RawCollectionList = cms.VInputTag( cms.InputTag('rawStepHCAL')))

process.load('EventFilter.ESDigiToRaw.esDigiToRaw_cfi')
process.rawStepES = process.esDigiToRaw.clone(
Label = cms.string('ecalPreshowerDigis'),
)
process.ESRawDataCollector = process.rawDataCollector.clone(RawCollectionList = cms.VInputTag( cms.InputTag('rawStepES')))

process.rawPath = cms.Path(process.rawStep*process.rawStepPix*process.rawStepHCAL*process.rawStepES*process.StripRawDataCollector*process.PixelRawDataCollector*process.HCALRawDataCollector*process.ESRawDataCollector)


# Schedule definition
process.schedule = cms.Schedule(process.analyzer_step, process.rawPath, process.endjob_step,process.output_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

from Configuration.Applications.ConfigBuilder import MassReplaceInputTag
MassReplaceInputTag(process, new="rawDataMapperByLabel", old="rawDataCollector")

#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)


# Customisation from command line

#Have logErrorHarvester wait for the same EDProducers to finish as those providing data for the OutputModule
from FWCore.Modules.logErrorHarvester_cff import customiseLogErrorHarvesterUsingOutputCommands
process = customiseLogErrorHarvesterUsingOutputCommands(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion