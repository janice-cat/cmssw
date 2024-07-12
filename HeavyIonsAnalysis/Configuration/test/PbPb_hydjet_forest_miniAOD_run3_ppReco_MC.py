### HiForest Configuration
# Collisions: pp
# Type: MC
# Input: miniAOD

import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
from Configuration.Eras.Era_Run3_cff import Run3
process = cms.Process('HiForest', Run3)
process.options = cms.untracked.PSet()


# import of standard configurations
options = VarParsing ('analysis')
options.register ('subfile',
              0,
              VarParsing.multiplicity.singleton,
              VarParsing.varType.int,
              "[0 .. 24], we batch 10 DIGI files into a job")
options.parseArguments()
print('subfile:\t', options.subfile)

#####################################################################################
# HiForest labelling info
#####################################################################################

process.load("HeavyIonsAnalysis.EventAnalysis.HiForestInfo_cfi")
process.HiForestInfo.info = cms.vstring("HiForest, miniAOD, 132X, mc")

#####################################################################################
# Input source
#####################################################################################

process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    fileNames = cms.untracked.vstring(
        'file:/eos/cms//store/group/phys_heavyions/yuchenc/localProduction/stepAODMINIAOD_bMin15.root'
        # 'file:../../../../../CMSSW_13_2_10/src/HeavyIonsAnalysis/Configuration/test/stepAODMINIAOD.root'
        # 'file:/eos/cms/store/group/phys_heavyions/yuchenc/localProduction/stepAODMINIAOD_numFile10_subFile'+str(options.subfile)+'.root'
        # 'file:/afs/cern.ch/user/y/yuchenc/forestFowardPDs/CMSSW_13_2_10/src/HeavyIonsAnalysis/Configuration/test/test.root'
        # '/store/mc/HINPbPbSpring23MiniAOD/MinBias_Drum5F_5p36TeV_hydjet/MINIAODSIM/NoPU_132X_mcRun3_2023_realistic_HI_v9-v2/2820000/02288831-b588-4380-bac8-9910f24691bd.root'
    )
)

# Number of events we want to process, -1 = all events
process.maxEvents = cms.untracked.PSet(
    # input = cms.untracked.int32(40)
    input = cms.untracked.int32(-1)
)

#####################################################################################
# Load Global Tag, Geometry, etc.
#####################################################################################

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100

# TODO: Global tag complete guess from the list. Probably wrong. But does not crash
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '132X_mcRun3_2023_realistic_HI_v9', '')
process.HiForestInfo.GlobalTagLabel = process.GlobalTag.globaltag

# TODO: Old calibration here, might need to update
process.GlobalTag.toGet.extend([
    cms.PSet(record = cms.string("BTagTrackProbability3DRcd"),
             tag = cms.string("JPcalib_MC94X_2017pp_v2"),
             connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")

         )
      ])

#####################################################################################
# Define tree output
#####################################################################################

process.TFileService = cms.Service("TFileService",
    # fileName = cms.string("/eos/cms/store/group/phys_heavyions/yuchenc/localProduction/PbPb_hydjet_MC_subFile"+str(options.subfile)+".root"))
    fileName = cms.string("file:/eos/cms//store/group/phys_heavyions/yuchenc/localProduction/test_bMin15.root"))
    # fileName = cms.string("test.root"))

#####################################################################################
# Additional Reconstruction and Analysis: Main Body
#####################################################################################

#############################
# Jets
#############################
process.load("HeavyIonsAnalysis.JetAnalysis.ak4PFJetSequence_ppref_mc_cff")
#####################################################################################

############################
# Event Analysis
############################
# use data version to avoid PbPb MC
process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_data_cfi')
process.hiEvtAnalyzer.Vertex = cms.InputTag("offlineSlimmedPrimaryVertices")
process.hiEvtAnalyzer.doCentrality = cms.bool(True)
process.hiEvtAnalyzer.doEvtPlane = cms.bool(False)
process.hiEvtAnalyzer.doEvtPlaneFlat = cms.bool(False)
process.hiEvtAnalyzer.doMC = cms.bool(True) # general MC info
process.hiEvtAnalyzer.doHiMC = cms.bool(True) # HI specific MC info
process.hiEvtAnalyzer.doHFfilters = cms.bool(False) # Disable HF filters for ppRef

process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hltobject_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.l1object_cfi')

# TODO: Many of these triggers are not available in the test file
from HeavyIonsAnalysis.EventAnalysis.hltobject_cfi import trigger_list_mc
process.hltobject.triggerNames = trigger_list_mc

process.load('L1Trigger.L1TNtuples.l1MetFilterRecoTree_cfi')

# PF analyzer
process.load('HeavyIonsAnalysis.EventAnalysis.particleFlowAnalyser_cfi')
# 1/27/2024: lower the pT min cut from default (5) to 0.01 - important for the rapidity gap analysis
process.particleFlowAnalyser.ptMin = cms.double(0.01)

# Gen particles
process.load('HeavyIonsAnalysis.EventAnalysis.HiGenAnalyzer_cfi')
# 1/27/2024 lower the pT min cut from default (5) to 0.01 - important for the rapidity gap analysis
process.HiGenParticleAna.ptMin = cms.untracked.double(0.01)

#####################################################################################

#########################
# Track Analyzer
#########################
process.load('HeavyIonsAnalysis.TrackAnalysis.TrackAnalyzers_cff')

#####################################################################################

#####################
# photons
######################
process.load('HeavyIonsAnalysis.EGMAnalysis.ggHiNtuplizer_cfi')
process.ggHiNtuplizer.doGenParticles = cms.bool(True)
process.ggHiNtuplizer.doMuons = cms.bool(False) # unpackedMuons collection not found from file
process.ggHiNtuplizer.useValMapIso = cms.bool(False) # True here causes seg fault
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

# jet reco sequence
#CM Edit - switch to ak4PFJetSeequence
#process.load('HeavyIonsAnalysis.JetAnalysis.akCs4PFJetSequence_pponPbPb_data_cff')
process.load("HeavyIonsAnalysis.JetAnalysis.ak4PFJetSequence_ppref_mc_cff")
process.load('HeavyIonsAnalysis.JetAnalysis.ak4CaloJetSequence_pp_data_cff')

####################################################################################
process.ak4CaloJetAnalyzer.jetTag = cms.InputTag("slimmedCaloJets")

#########################
# Main analysis list
#########################

process.forest = cms.Path(
    process.HiForestInfo +
    process.hltanalysis *
    process.hiEvtAnalyzer *
    process.hltobject +
    process.l1object +
    process.l1MetFilterRecoTree +
    process.HiGenParticleAna +
    process.ggHiNtuplizer +
    process.trackSequencePP +
    process.particleFlowAnalyser +
    process.ak4CaloJetAnalyzer
)

#####################################################################################

addR3Jets = False
addR4Jets = True

if addR3Jets or addR4Jets :
    process.load("HeavyIonsAnalysis.JetAnalysis.extraJets_cff")
    from HeavyIonsAnalysis.JetAnalysis.clusterJetsFromMiniAOD_cff import setupPprefJets

    if addR3Jets :
        process.jetsR3 = cms.Sequence()
        setupPprefJets('ak3PF', process.jetsR3, process, isMC = 1, radius = 0.30, JECTag = 'AK3PF')
        process.ak3PFpatJetCorrFactors.levels = ['L2Relative', 'L3Absolute']
        process.load("HeavyIonsAnalysis.JetAnalysis.candidateBtaggingMiniAOD_cff")
        process.ak3PFJetAnalyzer = process.ak4PFJetAnalyzer.clone(jetTag = "ak3PFpatJets", jetName = 'ak3PF', genjetTag = "ak3GenJetsNoNu")
        process.forest += process.extraJetsMC * process.jetsR3 * process.ak3PFJetAnalyzer

    if addR4Jets :
        # Recluster using an alias "0" in order not to get mixed up with the default AK4 collections
        process.jetsR4 = cms.Sequence()
        setupPprefJets('ak04PF', process.jetsR4, process, isMC = 1, radius = 0.40, JECTag = 'AK4PF')
        process.ak04PFpatJetCorrFactors.levels = ['L2Relative', 'L3Absolute']
        process.ak04PFpatJetCorrFactors.primaryVertices = "offlineSlimmedPrimaryVertices"
        process.load("HeavyIonsAnalysis.JetAnalysis.candidateBtaggingMiniAOD_cff")
        process.ak4PFJetAnalyzer.jetTag = 'ak04PFpatJets'
        process.ak4PFJetAnalyzer.jetName = 'ak04PF'
        process.ak4PFJetAnalyzer.doSubEvent = False # Need to disable this, since there is some issue with the gen jet constituents. More debugging needed is want to use constituents.
        process.forest += process.extraJetsMC * process.jetsR4 * process.ak4PFJetAnalyzer

#################### D/B finder #################
AddCaloMuon = False
runOnMC = True ## !!
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
process.Dfinder.tkPtCut = cms.double(0.0) # before fit
process.Dfinder.tkEtaCut = cms.double(2.4) # before fit
process.Dfinder.dPtCut = cms.vdouble(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) # before fit
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

process.load('HeavyIonsAnalysis.EventAnalysis.skimanalysis_cfi')
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
