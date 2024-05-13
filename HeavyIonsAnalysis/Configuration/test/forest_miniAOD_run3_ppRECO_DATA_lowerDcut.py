### HiForest Configuration
# Input: miniAOD
# Type: data

import FWCore.ParameterSet.Config as cms
#Switch the era to nbe Era_Run3_2023_cff - Run3_2023
from Configuration.Eras.Era_Run3_2023_cff import Run3_2023
import glob as glob
process = cms.Process('HiForest',Run3_2023)

###############################################################################

# HiForest info
process.load("HeavyIonsAnalysis.EventAnalysis.HiForestInfo_cfi")
process.HiForestInfo.info = cms.vstring("HiForest, miniAOD, 132X, data")

# import subprocess, os
# version = subprocess.check_output(
#     ['git', '-C', os.path.expandvars('$CMSSW_BASE/src'), 'describe', '--tags'])
# if version == '':
#     version = 'no git info'
# process.HiForestInfo.HiForestVersion = cms.string(version)

###############################################################################

# input files
process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    fileNames = cms.untracked.vstring(
        #File below is miniAOD from PbPb ZB
        # 'file:/afs/cern.ch/user/p/pchou/public/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_run37464X_calocut5.root'
        # 'file:/afs/cern.ch/user/p/pchou/public/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_run374719_ls0100.root'
        # [ 'file:'+f for f in glob.glob('/eos/cms/store/group/phys_heavyions/ginnocen/crabjobs_Run3_PbPbUPC/CRAB_UserFiles/crab_HIForwardStreamers/231003_225112/0000/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD*.root')]
        # [ 'file:'+f for f in glob.glob('/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374833/231007_144019/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root')]
        # [
        # '/store/hidata/HIRun2023A/HIForward0/MINIAOD/PromptReco-v2/000/375/002/00000/ca3d2434-b8ff-489e-8b87-18e0e5cde2ec.root',
        # '/store/hidata/HIRun2023A/HIForward0/MINIAOD/PromptReco-v2/000/375/002/00000/9d2bfdfd-683d-4e18-a488-b3915452737e.root',
        # '/store/hidata/HIRun2023A/HIForward0/MINIAOD/PromptReco-v2/000/375/002/00000/c1252302-f9c1-4183-bd26-b39bcb5b18d9.root',
        # '/store/hidata/HIRun2023A/HIForward0/MINIAOD/PromptReco-v2/000/375/002/00000/ca3d2434-b8ff-489e-8b87-18e0e5cde2ec.root',
        # ]
        # '/store/hidata/HIRun2023A/HIForward0/MINIAOD/PromptReco-v2/000/375/055/00000/4eacc5c8-5e8a-4fc1-80ee-0237cd27e364.root'
        # '/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_375252/231019_160125/0001/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_1461.root',
        'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/MINIAOD/16Jan2024-v1/2810000/0640e99d-84f5-49fd-a012-48be69252e99.root',
        # 'file:0640e99d-84f5-49fd-a012-48be69252e99.root',
        # '/store/hidata/HIRun2023A/HIForward1/MINIAOD/PromptReco-v2/000/375/002/00000/d9623a9c-74e7-41ae-9b6c-438a3bc2cb1f.root'
    ), 
    # eventsToProcess=cms.untracked.VEventRange("375252:660298351-375252:660298351"),
    # secondaryFileNames = cms.untracked.vstring(
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/0cc0b17b-193a-4efa-b4a8-ac8c601ef5f4.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/168ffff8-98c2-4637-bc52-8689c86703a4.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/1a5af614-2452-473e-8e9a-043afefc02de.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/239aad1c-e12b-421c-95db-529f797f174e.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/338cab5b-778f-4f58-92fe-42448738e68b.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/3fec0932-9f87-4bde-9832-b40b22068edc.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/4274515c-80e4-46ff-9223-e0a2767a0592.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/46f81b05-a091-4d99-9d79-136a8212291b.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/5e449762-34bb-440d-b56f-30e90ee7c745.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/6183b4ac-6df1-44ca-8fe3-7a2d5ec53649.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/61a38d70-0417-49f6-8605-873d06060a8a.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/6b6ae89d-8c01-4bbb-b67e-5eccb1fba426.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/763b007e-2bf4-402f-800c-446dea4dc63b.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/81f9d817-0bab-49bc-b0b7-3076abcd4851.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/9979d7e4-05aa-463b-a8e7-286e00ab8aba.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/abecace2-cdbf-4a88-8596-1451a02b029d.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/af8c63b9-ad12-470d-928b-3ccd1316ba67.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/b6939dac-d002-4ac3-bfd7-89610cfeb990.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/c2ed6c59-a5c6-4046-b423-f5abcd1da4d5.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/d4ec992d-d4ad-40ef-8a0c-b45e0501303b.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/e11e40fc-5622-497b-bccb-68b081b10038.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/e86f7113-5f6b-4354-b248-6762e2da72bb.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/e935cb80-e4ae-4173-97b4-24617f0e2ad3.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/f4dd702b-605b-407a-8f1d-dce34c45dc1d.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/f69b573d-6bdd-40db-98e5-29da0d559b0b.root',
    #     'root://cms-xrd-global.cern.ch//store/hidata/HIRun2023A/HIForward0/RAW/v1/000/375/754/00000/f84a149f-7ab2-4c07-bef7-5d8402072266.root',
    #     # '/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_375252/231019_160125/0001/reco_RAW2DIGI_L1Reco_RECO_PAT_1461.root'
    #     ),
)

import FWCore.PythonUtilities.LumiList as LumiList
process.source.lumisToProcess = LumiList.LumiList(filename = '/eos/user/c/cmsdqm/www/CAF/certification/Collisions23HI/Cert_Collisions2023HI_374288_375823_Golden.json').getVLuminosityBlockRange()

# number of events to process, set to -1 to process all events
process.maxEvents = cms.untracked.PSet(
   # input = cms.untracked.int32(150000)
    input = cms.untracked.int32(-1)
    # input = cms.untracked.int32(1000)
)

###############################################################################

# load Global Tag, geometry, etc.
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100


from Configuration.AlCa.GlobalTag import GlobalTag
#SWITCHING THE GT TO PROMPT RECO of PbPb
process.GlobalTag = GlobalTag(process.GlobalTag, '132X_dataRun3_Prompt_v3', '')

process.HiForestInfo.GlobalTagLabel = process.GlobalTag.globaltag

###############################################################################

# root output
process.TFileService = cms.Service("TFileService",
    fileName = cms.string("HiForestMiniAOD.root"))

# # edm output for debugging purposes
# process.output = cms.OutputModule(
#     "PoolOutputModule",
#     fileName = cms.untracked.string('HiForestEDM.root'),
#     outputCommands = cms.untracked.vstring(
#         'keep *',
#         )
#     )

# process.output_path = cms.EndPath(process.output)

###############################################################################

# event analysis
#CM TEMP EDIT
process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_data_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.skimanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hltobject_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.l1object_cfi')

process.hiEvtAnalyzer.doCentrality = cms.bool(False)
process.hiEvtAnalyzer.doHFfilters = cms.bool(False)

from HeavyIonsAnalysis.EventAnalysis.hltobject_cfi import trigger_list_data_2023_skimmed
process.hltobject.triggerNames = trigger_list_data_2023_skimmed

process.load('L1Trigger.L1TNtuples.l1MetFilterRecoTree_cfi')

process.load('HeavyIonsAnalysis.EventAnalysis.particleFlowAnalyser_cfi')
process.particleFlowAnalyser.ptMin = cms.double(0.0)
################################
# electrons, photons, muons
process.load('HeavyIonsAnalysis.EGMAnalysis.ggHiNtuplizer_cfi')
process.ggHiNtuplizer.doMuons = cms.bool(False)
process.ggHiNtuplizer.useValMapIso = cms.bool(False)
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
################################
# jet reco sequence
#CM Edit - switch to ak4PFJetSeequence
#process.load('HeavyIonsAnalysis.JetAnalysis.akCs4PFJetSequence_pponPbPb_data_cff')
process.load("HeavyIonsAnalysis.JetAnalysis.ak2PFJetSequence_ppref_data_cff")
process.load("HeavyIonsAnalysis.JetAnalysis.ak3PFJetSequence_ppref_data_cff")
process.load("HeavyIonsAnalysis.JetAnalysis.ak4PFJetSequence_ppref_data_cff")
process.load('HeavyIonsAnalysis.JetAnalysis.ak4CaloJetSequence_pp_data_cff')


#The following series of analyzers is to hack in a calorimeter jet correction
process.hltAK4CaloRelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
                                                     algorithm = cms.string('AK4Calo'),
                                                     level = cms.string('L2Relative')
)
process.hltAK4CaloAbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
                                                     algorithm = cms.string('AK4Calo'),
                                                     level = cms.string('L3Absolute')
                                                 )
process.hltAK4CaloCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
                                             correctors = cms.VInputTag("hltAK4CaloRelativeCorrector", "hltAK4CaloAbsoluteCorrector")
)
process.hltAK4CaloJetsCorrected = cms.EDProducer("CorrectedCaloJetProducer",
                                                 correctors = cms.VInputTag("hltAK4CaloCorrector"),
                                                 src = cms.InputTag("slimmedCaloJets")
)

process.ak4CaloJetAnalyzer.jetTag = cms.InputTag("hltAK4CaloJetsCorrected")
#End calorimeter jet correction hack


################################
# tracks
process.load("HeavyIonsAnalysis.TrackAnalysis.TrackAnalyzers_cff")
#process.load("HeavyIonsAnalysis.MuonAnalysis.unpackedMuons_cfi")
# muons
process.load("HeavyIonsAnalysis.MuonAnalysis.muonAnalyzer_cfi")
###############################################################################

# ZDC RecHit Producer
#CM Edit turn off the ZDC
process.load('HeavyIonsAnalysis.ZDCAnalysis.QWZDC2018Producer_cfi')
process.load('HeavyIonsAnalysis.ZDCAnalysis.QWZDC2018RecHit_cfi')
process.load('HeavyIonsAnalysis.ZDCAnalysis.zdcanalyzer_cfi')

process.zdcdigi.SOI = cms.untracked.int32(2)
process.zdcanalyzer.doZDCRecHit = False
process.zdcanalyzer.doZDCDigi = True
process.zdcanalyzer.zdcRecHitSrc = cms.InputTag("QWzdcreco")
process.zdcanalyzer.zdcDigiSrc = cms.InputTag("hcalDigis", "ZDC")
process.zdcanalyzer.calZDCDigi = False
process.zdcanalyzer.verbose = False
process.zdcanalyzer.nZdcTs = cms.int32(6)

from CondCore.CondDB.CondDB_cfi import *
process.es_pool = cms.ESSource("PoolDBESSource",
    timetype = cms.string('runnumber'),
    toGet = cms.VPSet(
        cms.PSet(
            record = cms.string("HcalElectronicsMapRcd"),
            tag = cms.string("HcalElectronicsMap_2021_v2.0_data")
        )
    ),
    connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
        authenticationMethod = cms.untracked.uint32(1)
    )

process.es_prefer = cms.ESPrefer('HcalTextCalibrations', 'es_ascii')
process.es_ascii = cms.ESSource(
    'HcalTextCalibrations',
    input = cms.VPSet(
        cms.PSet(

            object = cms.string('ElectronicsMap'),
            file = cms.FileInPath("emap_2023_newZDC_v3.txt")

             )
        )
    )
#CM Edit end turn off ZDC

###############################################################################
# main forest sequence
process.forest = cms.Path(
    process.HiForestInfo +
    process.hiEvtAnalyzer +
    process.hltanalysis +
    # process.hltobject +
    process.l1object +
    process.l1MetFilterRecoTree +
    process.trackSequencePP +
    process.hltAK4CaloRelativeCorrector + 
    process.hltAK4CaloAbsoluteCorrector +
    process.hltAK4CaloCorrector +
    process.hltAK4CaloJetsCorrected +
    process.ak4CaloJetAnalyzer +
    process.particleFlowAnalyser +
    process.ggHiNtuplizer +
    #process.zdcdigi +
    #process.QWzdcreco +
    process.zdcanalyzer +
    process.muonSequencePP
#    process.unpackedMuons +
#    process.muonAnalyzer
    )

#customisation
##########################
## Event Selection -> add the needed filters here
##########################
#
process.load('HeavyIonsAnalysis.EventAnalysis.collisionEventSelection_cff')
process.pclusterCompatibilityFilter = cms.Path(process.clusterCompatibilityFilter)
process.pprimaryVertexFilter = cms.Path(process.primaryVertexFilter)
#process.load('HeavyIonsAnalysis.EventAnalysis.hffilter_cfi')
#process.pphfCoincFilter4Th2 = cms.Path(process.phfCoincFilter4Th2)
#process.pphfCoincFilter1Th3 = cms.Path(process.phfCoincFilter1Th3)
#process.pphfCoincFilter2Th3 = cms.Path(process.phfCoincFilter2Th3)
#process.pphfCoincFilter3Th3 = cms.Path(process.phfCoincFilter3Th3)
#process.pphfCoincFilter4Th3 = cms.Path(process.phfCoincFilter4Th3)
#process.pphfCoincFilter5Th3 = cms.Path(process.phfCoincFilter5Th3)
#process.pphfCoincFilter1Th4 = cms.Path(process.phfCoincFilter1Th4)
#process.pphfCoincFilter2Th4 = cms.Path(process.phfCoincFilter2Th4)
#process.pphfCoincFilter3Th4 = cms.Path(process.phfCoincFilter3Th4)
#process.pphfCoincFilter4Th4 = cms.Path(process.phfCoincFilter4Th4)
#process.pphfCoincFilter5Th4 = cms.Path(process.phfCoincFilter5Th4)
#process.pphfCoincFilter1Th5 = cms.Path(process.phfCoincFilter1Th5)
#process.pphfCoincFilter2Th5 = cms.Path(process.phfCoincFilter2Th5)
#process.pphfCoincFilter3Th5 = cms.Path(process.phfCoincFilter3Th5)
#process.pphfCoincFilter4Th5 = cms.Path(process.phfCoincFilter4Th5)
#process.pphfCoincFilter5Th5 = cms.Path(process.phfCoincFilter5Th5)
#process.pphfCoincFilter1Th6 = cms.Path(process.phfCoincFilter1Th6)
#process.pphfCoincFilter2Th6 = cms.Path(process.phfCoincFilter2Th6)
#process.pphfCoincFilter3Th6 = cms.Path(process.phfCoincFilter3Th6)
#process.pphfCoincFilter4Th6 = cms.Path(process.phfCoincFilter4Th6)
#process.pphfCoincFilter5Th6 = cms.Path(process.phfCoincFilter5Th6)

#process.NoScraping = cms.EDFilter("FilterOutScraping",
# applyfilter = cms.untracked.bool(True),
# debugOn = cms.untracked.bool(False),
# numtrack = cms.untracked.uint32(10),
# thresh = cms.untracked.double(0.25)
#)
#process.pBeamScrapingFilter=cms.Path(process.NoScraping)

process.pAna = cms.EndPath(process.skimanalysis)




# Select the types of jets filled
addR2Jets = True

addR3Jets = True
addR3FlowJets = False
addR4Jets = True
addR4FlowJets = False
addUnsubtractedR4Jets = False

# Choose which additional information is added to jet trees
doHIJetID = True             # Fill jet ID and composition information branches
doWTARecluster = True        # Add jet phi and eta for WTA axis

# this is only for non-reclustered jets
addCandidateTagging = False

if addR4Jets :
    process.load("HeavyIonsAnalysis.JetAnalysis.extraJets_cff")
    from HeavyIonsAnalysis.JetAnalysis.clusterJetsFromMiniAOD_cff import setupPprefJets

    if addR2Jets :
        process.jetsR2 = cms.Sequence()
        setupPprefJets('ak2PF', process.jetsR2, process, isMC = 0, radius = 0.20, JECTag = '\
AK2PF')
        process.ak2PFpatJetCorrFactors.levels = ['L2Relative', 'L3Absolute']
        process.ak2PFpatJetCorrFactors.primaryVertices = "offlineSlimmedPrimaryVertices"
        process.load("HeavyIonsAnalysis.JetAnalysis.candidateBtaggingMiniAOD_cff")
        process.ak2PFJetAnalyzer.jetTag = 'ak2PFpatJets'
        process.ak2PFJetAnalyzer.jetName = 'ak2PF'
        process.ak2PFJetAnalyzer.doSubEvent = False # Need to disable this, since there is some issue with the gen jet constituents. More debugging needed is want to use constituents. 
        process.forest += process.extraJetsData * process.jetsR2 * process.ak2PFJetAnalyzer

    if addR3Jets :
        process.jetsR3 = cms.Sequence()
        setupPprefJets('ak3PF', process.jetsR3, process, isMC = 0, radius = 0.30, JECTag = '\
AK3PF')
        process.ak3PFpatJetCorrFactors.levels = ['L2Relative', 'L3Absolute']
        process.ak3PFpatJetCorrFactors.primaryVertices = "offlineSlimmedPrimaryVertices"
        process.load("HeavyIonsAnalysis.JetAnalysis.candidateBtaggingMiniAOD_cff")
        process.ak3PFJetAnalyzer.jetTag = 'ak3PFpatJets'
        process.ak3PFJetAnalyzer.jetName = 'ak3PF'
        process.ak3PFJetAnalyzer.doSubEvent = False # Need to disable this, since there is some issue with the gen jet constituents. More debugging needed is want to use constituents. 
        process.forest += process.extraJetsData * process.jetsR3 * process.ak3PFJetAnalyzer



    if addR4Jets :
        # Recluster using an alias "0" in order not to get mixed up with the default AK4 collections                                                                                    
        print("ADD R4 JETS")
        process.jetsR4 = cms.Sequence()
        setupPprefJets('ak04PF', process.jetsR4, process, isMC = 0, radius = 0.40, JECTag = 'AK4PF')
        process.ak04PFpatJetCorrFactors.levels = ['L2Relative', 'L3Absolute']
        process.ak04PFpatJetCorrFactors.primaryVertices = "offlineSlimmedPrimaryVertices"
        process.load("HeavyIonsAnalysis.JetAnalysis.candidateBtaggingMiniAOD_cff")
        process.ak4PFJetAnalyzer.jetTag = 'ak04PFpatJets'
        process.ak4PFJetAnalyzer.jetName = 'ak04PF'
        process.ak4PFJetAnalyzer.doSubEvent = False # Need to disable this, since there is some issue with the gen jet constituents. More debugging needed is want to use constituents. 
        process.forest += process.extraJetsData * process.jetsR4 * process.ak4PFJetAnalyzer

#Via Jing
#################### D finder #################
AddCaloMuon = False
runOnMC = False ## !!

HIFormat = False
UseGenPlusSim = False
# VtxLabel = "unpackedTracksAndVertices"
VtxLabel = "offlineSlimmedPrimaryVertices"
TrkLabel = "packedPFCandidates"
GenLabel = "prunedGenParticles"
TrkChi2Label = "packedPFCandidateTrackChi2"
useL1Stage2 = True
HLTProName = "HLT"
from Bfinder.finderMaker.finderMaker_75X_cff import finderMaker_75X
finderMaker_75X(process, AddCaloMuon, runOnMC, HIFormat, UseGenPlusSim, VtxLabel, TrkLabel, TrkChi2Label, GenLabel, useL1Stage2, HLTProName)
process.Dfinder.MVAMapLabel = cms.InputTag(TrkLabel, "MVAValues")
process.Dfinder.makeDntuple = cms.bool(True)
process.Dfinder.tkPtCut = cms.double(0.5) # before fit
process.Dfinder.tkEtaCut = cms.double(2.4) # before fit
process.Dfinder.dPtCut = cms.vdouble(1.0, 1.0, 1.5, 1.5, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.5, 1.5, 2.0, 2.0) # before fit
process.Dfinder.VtxChiProbCut = cms.vdouble(0.05, 0.05, 0.05, 0.05, 0.0, 0.0, 0.05, 0.05, 0.0, 0.0, 0.0, 0.0, 0.05, 0.05, 0.05, 0.05)
process.Dfinder.dCutSeparating_PtVal = cms.vdouble(5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5.)
process.Dfinder.tktkRes_svpvDistanceCut_lowptD = cms.vdouble(0., 0., 0., 0., 0., 0., 0., 0., 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 0., 0.)
process.Dfinder.tktkRes_svpvDistanceCut_highptD = cms.vdouble(0., 0., 0., 0., 0., 0., 0., 0., 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 0., 0.)
process.Dfinder.svpvDistanceCut_lowptD = cms.vdouble(1., 1., 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 0., 0., 0., 0., 0., 0., 2.5, 2.5)
process.Dfinder.svpvDistanceCut_highptD = cms.vdouble(2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 0., 0., 0., 0., 0., 0., 2.5, 2.5)

process.Dfinder.Dchannel = cms.vint32(1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
process.Dfinder.dropUnusedTracks = cms.bool(True)
process.Dfinder.detailMode = cms.bool(False)

process.Dfinder.printInfo = cms.bool(False)

process.dfinder = cms.Path(process.DfinderSequence)
###############################################################################

#################### B finder #################
AddCaloMuon = False
runOnMC = False ## !!
HIFormat = False
UseGenPlusSim = False
# VtxLabel = "unpackedTracksAndVertices"
VtxLabel = "offlineSlimmedPrimaryVertices"
TrkLabel = "packedPFCandidates"
TrkChi2Label = "packedPFCandidateTrackChi2"
GenLabel = "prunedGenParticles"
useL1Stage2 = True
HLTProName = "HLT"

process.Bfinder.MVAMapLabel = cms.InputTag(TrkLabel,"MVAValues")
process.Bfinder.makeBntuple = cms.bool(True)
process.Bfinder.tkPtCut = cms.double(0.8) # before fit
process.Bfinder.tkEtaCut = cms.double(2.4) # before fit
process.Bfinder.jpsiPtCut = cms.double(0.0) # before fit
process.Bfinder.bPtCut = cms.vdouble(1.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0) # before fit
process.Bfinder.Bchannel = cms.vint32(1, 0, 0, 1, 1, 1, 1)
process.Bfinder.VtxChiProbCut = cms.vdouble(0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.10)
process.Bfinder.svpvDistanceCut = cms.vdouble(2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.0)
process.Bfinder.doTkPreCut = cms.bool(True)
process.Bfinder.doMuPreCut = cms.bool(True)
process.Bfinder.MuonTriggerMatchingPath = cms.vstring(
    "HLT_HIL3Mu0NHitQ10_L2Mu0_MAXdR3p5_M1to5_v1")
process.Bfinder.MuonTriggerMatchingFilter = cms.vstring(
    "hltL3f0L3Mu0L2Mu0DR3p5FilteredNHitQ10M1to5")
process.BfinderSequence.insert(0, process.unpackedMuons)
process.BfinderSequence.insert(0, process.unpackedTracksAndVertices)
# process.unpackedMuons.muonSelectors = cms.vstring() # uncomment for pp
process.unpackedMuons.muonSelectors = cms.vstring() 

process.Bfinder.printInfo = cms.bool(False)

process.bfinder = cms.Path(process.BfinderSequence)


from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.hltfilter = hltHighLevel.clone(
   HLTPaths = [
        # Double muons
        'HLT_HIUPC_DoubleMuCosmic*_MaxPixelCluster1000_v*',
        'HLT_HIUPC_DoubleMuOpen*_NotMBHF*AND_v*',

        # Not MB
        'HLT_HIUPC_NotMBHF*_v*',

        # Jet triggers
        'HLT_HIUPC_SingleJet*_ZDC1n*XOR_*MaxPixelCluster*',
        'HLT_HIUPC_SingleJet*_NotMBHF2AND_*MaxPixelCluster*',

        # Single muon
        'HLT_HIUPC_SingleMu*_NotMBHF*_MaxPixelCluster*',

        # Single EG
        'HLT_HIUPC_SingleEG3_NotMBHF2AND_v*',
        'HLT_HIUPC_SingleEG5_NotMBHF2AND_v*',
        'HLT_HIUPC_SingleEG3_NotMBHF2AND_SinglePixelTrack_MaxPixelTrack_v*',
        'HLT_HIUPC_SingleEG5_NotMBHF2AND_SinglePixelTrack_MaxPixelTrack_v*',

        # ZDC 1n or, low pixel clusters
        'HLT_HIUPC_ZDC1nOR_SinglePixelTrackLowPt_MaxPixelCluster400_v*',
        'HLT_HIUPC_ZDC1nOR_MinPixelCluster400_MaxPixelCluster10000_v*',

        # ZB, single pixel track
        'HLT_HIUPC_ZeroBias_SinglePixelTrack_MaxPixelTrack_v*'
   ]
)
process.hltfilter.andOr = cms.bool(True)  # True = OR, False = AND between the HLT paths
process.hltfilter.throw = cms.bool(False) # throw exception on unknown path names

process.filterSequence = cms.Sequence(
    process.hltfilter *
    process.primaryVertexFilter
)

process.superFilterPath = cms.Path(process.filterSequence)
process.skimanalysis.superFilters = cms.vstring("superFilterPath")

for path in process.paths:
   getattr(process, path)._seq = process.filterSequence * getattr(process,path)._seq

from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)

process.options.wantSummary = cms.untracked.bool(True)