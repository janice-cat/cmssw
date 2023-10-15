import os, sys
import pandas as pd
import numpy as np
import ROOT
import uproot
sys.path.append('/afs/cern.ch/user/y/yuchenc/DataCompression/python/utils/')
import DfNtupleMgr as dnm
import PlotUtils as pu
import awkward as ak
import json
import gc

def main():
	lumiMask = json.load(open('/eos/cms/store/group/phys_heavyions/sayan/HIN_run3_pseudo_JSON/HIPhysicsRawPrime/Golden_Online_live.json'))

	inFileName = sys.argv[1]
	prefix 	 = os.path.basename(inFileName).replace('.root','') if '.root' in inFileName else \
		   os.path.basename(inFileName).replace('.txt','')

	runIdx 	 = prefix.replace('run','')
	runIdx 	 = '374681'
	lumiMask_forThisRun = np.array(lumiMask[runIdx])
	print('lumiMask_forThisRun', lumiMask_forThisRun)

	fileList = getFileList(inFileName)

	tSkimHLT, tHLT, tL1, tTrack, tZDC, tDfinder, tEvt, tAk4PFJet, tAk4CaloJet = [], [], [], [], [], [], [], [], []
	nEvtMax, nEvtMaxCounter = 50000, 50000

	for filepath in fileList:
		if nEvtMaxCounter <= 0: break
		print(filepath, nEvtMaxCounter)
		evtDf 	= uproot.open(filepath).key('hiEvtAnalyzer/HiTree').get(). \
			arrays(['lumi'], library='pd')
		lumiSet = set(evtDf['lumi'])
		# print('evtDf', evtDf)
		print('lumiSet', lumiSet)

		if (not all( any((x >= lumiMask_forThisRun[:,0]) * \
		                 (x <= lumiMask_forThisRun[:,1])) for x in lumiSet ) ): continue

		tSkimHLT.append(uproot.open(filepath).key('skimanalysis/HltTree').get(). \
			arrays(['pprimaryVertexFilter'], library='pd') )
		
		tHLT.append( 	uproot.open(filepath).key('hltanalysis/HltTree').get(). \
			arrays(filter_name=['L1_MinimumBiasHF1_AND_BptxAND',
				'L1_MinimumBiasHF2_AND_BptxAND','L1_NotMinimumBiasHF2_AND_BptxAND',
				'L1_ZDC22_OR_BptxAND','L1_ZDC80_OR_BptxAND','L1_ZDC133_OR_BptxAND',
				'L1_ZDCP22_BptxAND','L1_ZDCM22_BptxAND','L1_ZDC22_AND_BptxAND',
				'L1_ZDCP80_BptxAND','L1_ZDCM80_BptxAND','L1_ZDC80_AND_BptxAND',
				'L1_ZDCP133_BptxAND','L1_ZDCM133_BptxAND','L1_ZDC133_AND_BptxAND',
				'L1_ZDC1n_OR_BptxAND','L1_ZDC1n_OR_MinimumBiasHF1_AND_BptxAND','L1_ZDC1n_OR_MinimumBiasHF2_AND_BptxAND',
				'L1_ZDC1n_XOR_MinimumBiasHF1_AND_BptxAND','L1_ZDC1n_XOR_MinimumBiasHF2_AND_BptxAND','L1_ZDC1n_AND_MinimumBiasHF2_AND_BptxAND',
				'L1_ZDC2n_OR_MinimumBiasHF1_AND_BptxAND','L1_ZDC2n_OR_MinimumBiasHF2_AND_BptxAND',
				'L1_ZDC3n_OR_MinimumBiasHF1_AND_BptxAND','L1_ZDC3n_OR_MinimumBiasHF2_AND_BptxAND',
				'L1_ZDC22_OR','L1_ZDC80_OR','L1_ZDC133_OR',
				'L1_ZDCP22','L1_ZDCM22','L1_ZDC22_AND',
				'L1_ZDCP80','L1_ZDCM80','L1_ZDC80_AND',
				'L1_ZDCP133','L1_ZDCM133','L1_ZDC133_AND',
				'L1_SingleJet8_NotMinimumBiasHF2_AND_BptxAND','L1_SingleJet12_NotMinimumBiasHF2_AND_BptxAND','L1_SingleJet16_NotMinimumBiasHF2_AND_BptxAND',
				'L1_SingleJet8_ZDC1n_XOR_BptxAND','L1_SingleJet12_ZDC1n_XOR_BptxAND','L1_SingleJet16_ZDC1n_XOR_BptxAND',
				'HLT_HIMinimumBiasHF1AND_*v[0-9]', 
				'HLT_HIUPC_SingleJet8_ZDC1nXOR_MaxPixelCluster50000_v2',
				'HLT_HIUPC_SingleJet8_NotMBHF2AND_MaxPixelCluster50000_v2'],
				library='pd') )

		tL1.append( 	uproot.open(filepath).key('l1object/L1UpgradeFlatTree').get(). \
			arrays([ 'nJets','jetEt','jetEta','jetPUEt','jetBx',
				 'nSums','sumType','sumEt','sumPhi','sumBx'], library='pd') )

		tTrack.append( 	uproot.open(filepath).key('ppTracks/trackTree').get(). \
			arrays(['nTrk', 'nVtx',
				'xVtx', 'yVtx', 'zVtx',
				'xErrVtx', 'yErrVtx', 'zErrVtx',
				'chi2Vtx', 'ndofVtx', 'isFakeVtx', 
				'nTracksVtx', 'ptSumVtx'], library='pd') )

		tZDC.append( 	uproot.open(filepath).key('zdcanalyzer/zdcdigi').get(). \
			arrays(['sumPlus', 'sumMinus'], library='pd') )

		tDfinder.append(uproot.open(filepath).key('Dfinder/ntDkpi').get(). \
			arrays(['Dsize', 
				'Dmass', 'D_unfitted_mass', 'DsvpvDistance',
				'Dpt', 'D_unfitted_pt',
				'Deta','Dphi',
				'DvtxX', 'DvtxY', 'DvtxZ',
				'Dd0', 'Dd0Err', 'Ddca',
				'Dchi2ndf', 'Dchi2cl', 'Dalpha'], library='pd') )

		tEvt.append( evtDf )

		tAk4PFJet.append(uproot.open(filepath).key('ak4PFJetAnalyzer/t').get(). \
			arrays(['jteta', 'jtpt', 'nref',
				'jtPfNHF', 'jtPfNEF', 'jtPfMUF', 'jtPfCHF', 'jtPfCEF',
				'jtPfNHM', 'jtPfCHM'], library='pd'))

		tAk4CaloJet.append(uproot.open(filepath).key('ak4CaloJetAnalyzer/caloJetTree').get(). \
			arrays(['jteta', 'jtpt'], library='pd'). \
			rename(columns={'jteta': 'calo_jteta', 'jtpt': 'calo_jtpt'}))

		nEvtMaxCounter -= tSkimHLT[-1].shape[0]

	# print(tSkimHLT)
	# print(tHLT)
	# print(tL1)
	# print(tTrack)
	# print(tZDC)
	# print(tDfinder)
	# print(tEvt)
	# print(tAk4PFJet)
	HLTMBPaths = tHLT[0].filter(regex=('HLT_HIMinimumBiasHF1AND.*'))
	print('HLT MB paths:', HLTMBPaths)

	tSkimHLT 	= pd.concat(tSkimHLT)
	tHLT 		= pd.concat(tHLT)
	tL1 		= pd.concat(tL1)
	tTrack 		= pd.concat(tTrack)
	tZDC 		= pd.concat(tZDC)
	tDfinder 	= pd.concat(tDfinder)
	tEvt 		= pd.concat(tEvt)
	tAk4PFJet 	= pd.concat(tAk4PFJet)
	tAk4CaloJet 	= pd.concat(tAk4CaloJet)
	if nEvtMax > tSkimHLT.shape[0]: nEvtMax = tSkimHLT.shape[0]

	tSkimHLT	= tSkimHLT[:nEvtMax]
	tHLT		= tHLT[:nEvtMax]
	tL1		= tL1[:nEvtMax]
	tTrack		= tTrack[:nEvtMax]
	tZDC		= tZDC[:nEvtMax]
	tDfinder	= tDfinder[:nEvtMax]
	tEvt		= tEvt[:nEvtMax]
	tAk4PFJet	= tAk4PFJet[:nEvtMax]
	tAk4CaloJet	= tAk4CaloJet[:nEvtMax]

	print(tSkimHLT)
	print(tHLT)
	print(tL1)
	print(tTrack)
	print(tZDC)
	print(tDfinder)
	print(tEvt)
	print(tAk4PFJet)
	print(tAk4CaloJet)

	df 	= pd.concat([tSkimHLT, tHLT, tL1, tTrack, tZDC, tDfinder, tEvt, tAk4PFJet, tAk4CaloJet], axis=1)

	del tSkimHLT, tHLT, tL1, tTrack, tZDC, tDfinder, tEvt, tAk4PFJet, tAk4CaloJet
	gc.collect()
	print(gc.garbage)

	print(df.shape)


	plotAK4PFJet(df, prefix)
	plotAK4CaloJet(df, prefix)
	plotHLTTriggerStatus(df, prefix, HLTMBPaths)
	plotL1TriggerStatus(df, prefix)
	plotL1Obj(df, prefix, 
		doJetEtTrigSelStudy=False, HLTMBPaths=HLTMBPaths,
		doLeadingJet=True)
	plotPV(df, prefix)
	plotNTrk(df, prefix)
	plotZDC(df, prefix)
	plotDCand(df, prefix)


def plotAK4PFJet(df, prefix):
	_jetlist = ['jteta','jtpt',
		    'jtPfNHF', 'jtPfNEF', 'jtPfMUF', 'jtPfCHF', 'jtPfCEF',
		    'jtPfNHM', 'jtPfCHM']
	df_flatJet = flatten_df(df, _jetlist)

	print(1/df_flatJet.index.shape[0])
	dnm.plotVarsState(
		[[ 'no cut', df_flatJet ],
		 [ 'pass PV', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1') ] ],
		 [ 'fail PV', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==0') ] ]],
		[[ 'jteta', 'AK4PF jteta', (-5, 5) ],
		 [ 'jtpt', 'AK4PF jtpt', (0, 70) ]],
		 'img/'+prefix+'_UPCSpectra_AK4PFJet_PV_normalized.png', 100,
		 # density=2)
		 in_weights=1/df_flatJet.shape[0])

	dnm.plotVarsState(
		[[ '', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0') ] ]],
		[[ 'jteta', 'AK4PF jteta', (-5, 5) ],
		 [ 'jtpt', 'AK4PF jtpt', (0, 70) ]],
		 'img/'+prefix+'_UPCSpectra_AK4PFJet_cleanedUp_nonMB_normalized.png', 100,
		 density=2)

	dnm.plotVarsState(
		[[ 'PV+~MB', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0') ] ],
		 [ 'PV+~MB+emu(ZDC1n_XOR)', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
		 						       '((sumPlus>1100 & sumMinus<1100) | (sumPlus<1100 & sumMinus>1100))') ] ]],
		[[ 'jteta', 'AK4PF jteta', (-5, 5) ],
		 [ 'jtpt', 'AK4PF jtpt', (0, 70) ]],
		 'img/'+prefix+'_UPCSpectra_AK4PFJet_cleanedUp_emuzdcxor_normalized.png', 100,
		 # density=2)
		 in_weights=1/df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0') ].shape[0])

	dnm.plotVarsState(
		[[ '(1)ZDCXOR+Jet8', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & HLT_HIUPC_SingleJet8_ZDC1nXOR_MaxPixelCluster50000_v2==1') ] ],
		 [ '(2)NotHFAND+Jet8', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & HLT_HIUPC_SingleJet8_NotMBHF2AND_MaxPixelCluster50000_v2==1') ] ],
		 [ '(1)+(2)', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & HLT_HIUPC_SingleJet8_ZDC1nXOR_MaxPixelCluster50000_v2==1 & HLT_HIUPC_SingleJet8_NotMBHF2AND_MaxPixelCluster50000_v2==1') ] ],
		],
		[[ 'jteta', 'AK4PF jteta', (-5, 5) ],
		 [ 'jtpt', 'AK4PF jtpt', (0, 70) ]],
		 'img/'+prefix+'_UPCSpectra_AK4PFJet_cleanedUp_lowptJetTriggered_normalized.png', 100,
		 density=2)

	dnm.plotVarsState(
		[[ '', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & (' \
						   '(abs(jteta)<=2.6 & jtPfNHF<0.90 & jtPfNEF<0.90 & nref>1 & jtPfMUF<0.80 & jtPfCHF>0.01 & jtPfCHM>0 & jtPfCEF<0.80) | ' \
				 '(abs(jteta)> 2.6 & abs(jteta)<=2.7 & jtPfNHF<0.90 & jtPfNEF<0.99 &          jtPfMUF<0.80 &                jtPfCHM>0 & jtPfCEF<0.80) | ' \
				 '(abs(jteta)> 2.7 & abs(jteta)<=3.0 &                jtPfNEF<0.99 &                                                                   jtPfNHM>1) | ' \
				 '(abs(jteta)> 3.0 & abs(jteta)<=5.0 & jtPfNHF>0.2  & jtPfNEF<0.9  &                                                                   jtPfNHM>10) )' ) ] ]],
		[[ 'jteta', 'AK4PF jteta', (-5, 5) ],
		 [ 'jtpt', 'AK4PF jtpt', (0, 70) ]],
		 'img/'+prefix+'_UPCSpectra_AK4PFJet_cleanedUp_nonMB_jetid_normalized.png', 100,
		 density=2)

def plotAK4CaloJet(df, prefix):
	_jetlist = ['calo_jteta','calo_jtpt']
	df_flatJet = flatten_df(df, _jetlist)

	dnm.plotVarsState(
		[[ 'no cut', df_flatJet ],
		 [ 'pass PV', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1') ] ],
		 [ 'fail PV', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==0') ] ]],
		[[ 'calo_jteta', 'AK4Calo jteta', (-5, 5) ],
		 [ 'calo_jtpt', 'AK4Calo jtpt', (0, 70) ]],
		 'img/'+prefix+'_UPCSpectra_AK4CaloJet_PV_normalized.png', 100,
		 # density=2)
		 in_weights=1/df_flatJet.shape[0])

	dnm.plotVarsState(
		[[ '', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0') ] ]],
		[[ 'calo_jteta', 'AK4Calo jteta', (-5, 5) ],
		 [ 'calo_jtpt', 'AK4Calo jtpt', (0, 70) ]],
		 'img/'+prefix+'_UPCSpectra_AK4CaloJet_cleanedUp_nonMB_normalized.png', 100,
		 density=2)

	dnm.plotVarsState(
		[[ 'PV+~MB', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0') ] ],
		 [ 'PV+~MB+emu(ZDC1n_XOR)', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
		 						       '((sumPlus>1100 & sumMinus<1100) | (sumPlus<1100 & sumMinus>1100))') ] ]],
		[[ 'calo_jteta', 'AK4Calo jteta', (-5, 5) ],
		 [ 'calo_jtpt', 'AK4Calo jtpt', (0, 70) ]],
		 'img/'+prefix+'_UPCSpectra_AK4CaloJet_cleanedUp_emuzdcxor_normalized.png', 100,
		 # density=2)
		 in_weights=1/df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0') ].shape[0])

	dnm.plotVarsState(
		[[ '(1)ZDCXOR+Jet8', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & HLT_HIUPC_SingleJet8_ZDC1nXOR_MaxPixelCluster50000_v2==1') ] ],
		 [ '(2)NotHFAND+Jet8', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & HLT_HIUPC_SingleJet8_NotMBHF2AND_MaxPixelCluster50000_v2==1') ] ],
		 [ '(1)+(2)', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & HLT_HIUPC_SingleJet8_ZDC1nXOR_MaxPixelCluster50000_v2==1 & HLT_HIUPC_SingleJet8_NotMBHF2AND_MaxPixelCluster50000_v2==1') ] ],
		],
		[[ 'calo_jteta', 'AK4Calo jteta', (-5, 5) ],
		 [ 'calo_jtpt', 'AK4Calo jtpt', (0, 70) ]],
		 'img/'+prefix+'_UPCSpectra_AK4CaloJet_cleanedUp_lowptJetTriggered_normalized.png', 100,
		 density=2)

def plotL1TriggerStatus(df, prefix):
	dnm.plotVarsState(
		[[ '', df ]],
		[[ 'L1_MinimumBiasHF1_AND_BptxAND', 'L1_MinimumBiasHF1_AND_BptxAND', (-1, 2), 1 ],
		 [ 'L1_MinimumBiasHF2_AND_BptxAND', 'L1_MinimumBiasHF2_AND_BptxAND', (-1, 2), 1 ],
		 [ 'L1_NotMinimumBiasHF2_AND_BptxAND', 'L1_NotMinimumBiasHF2_AND_BptxAND', (-1, 2), 1 ],

		 [ 'L1_ZDC22_OR_BptxAND', 'L1_ZDC22_OR_BptxAND', (-1, 2), 1 ],
		 [ 'L1_ZDC80_OR_BptxAND', 'L1_ZDC80_OR_BptxAND', (-1, 2), 1 ],
		 [ 'L1_ZDC133_OR_BptxAND', 'L1_ZDC133_OR_BptxAND', (-1, 2), 1 ],

		 [ 'L1_ZDCP22_BptxAND', 'L1_ZDCP22_BptxAND', (-1, 2), 1 ],
		 [ 'L1_ZDCM22_BptxAND', 'L1_ZDCM22_BptxAND', (-1, 2), 1 ],
		 [ 'L1_ZDC22_AND_BptxAND', 'L1_ZDC22_AND_BptxAND', (-1, 2), 1 ],

		 [ 'L1_ZDCP80_BptxAND', 'L1_ZDCP80_BptxAND', (-1, 2), 1 ],
		 [ 'L1_ZDCM80_BptxAND', 'L1_ZDCM80_BptxAND', (-1, 2), 1 ],
		 [ 'L1_ZDC80_AND_BptxAND', 'L1_ZDC80_AND_BptxAND', (-1, 2), 1 ],

		 [ 'L1_ZDCP133_BptxAND', 'L1_ZDCP133_BptxAND', (-1, 2), 1 ],
		 [ 'L1_ZDCM133_BptxAND', 'L1_ZDCM133_BptxAND', (-1, 2), 1 ],
		 [ 'L1_ZDC133_AND_BptxAND', 'L1_ZDC133_AND_BptxAND', (-1, 2), 1 ],

		 [ 'L1_ZDC1n_OR_BptxAND', 'L1_ZDC1n_OR_BptxAND', (-1, 2), 1 ],
		 [ 'L1_ZDC1n_OR_MinimumBiasHF1_AND_BptxAND', 'L1_ZDC1n_OR_MinimumBiasHF1_AND_BptxAND', (-1, 2), 1 ],
		 [ 'L1_ZDC1n_OR_MinimumBiasHF2_AND_BptxAND', 'L1_ZDC1n_OR_MinimumBiasHF2_AND_BptxAND', (-1, 2), 1 ],

		 [ 'L1_ZDC1n_XOR_MinimumBiasHF1_AND_BptxAND', 'L1_ZDC1n_XOR_MinimumBiasHF1_AND_BptxAND', (-1, 2), 1 ],
		 [ 'L1_ZDC1n_XOR_MinimumBiasHF2_AND_BptxAND', 'L1_ZDC1n_XOR_MinimumBiasHF2_AND_BptxAND', (-1, 2), 1 ],
		 [ 'L1_ZDC1n_AND_MinimumBiasHF2_AND_BptxAND', 'L1_ZDC1n_AND_MinimumBiasHF2_AND_BptxAND', (-1, 2), 1 ],

		 [ 'L1_ZDC2n_OR_MinimumBiasHF1_AND_BptxAND', 'L1_ZDC2n_OR_MinimumBiasHF1_AND_BptxAND', (-1, 2), 1 ],
		 [ 'L1_ZDC3n_OR_MinimumBiasHF1_AND_BptxAND', 'L1_ZDC3n_OR_MinimumBiasHF1_AND_BptxAND', (-1, 2), 1 ],
		 
		 [ 'L1_ZDC2n_OR_MinimumBiasHF2_AND_BptxAND', 'L1_ZDC2n_OR_MinimumBiasHF2_AND_BptxAND', (-1, 2), 1 ],
		 [ 'L1_ZDC3n_OR_MinimumBiasHF2_AND_BptxAND', 'L1_ZDC3n_OR_MinimumBiasHF2_AND_BptxAND', (-1, 2), 1 ] ],
		 'img/'+prefix+'_UPCSpectra_MBtrig_normalized.png', 10,
		 density=2)

	dnm.plotVarsState(
		[[ '', df ]],
		[[ 'L1_ZDC22_OR', 'L1_ZDC22_OR', (-1, 2), 1 ],
		 [ 'L1_ZDC80_OR', 'L1_ZDC80_OR', (-1, 2), 1 ],
		 [ 'L1_ZDC133_OR', 'L1_ZDC133_OR', (-1, 2), 1 ],

		 [ 'L1_ZDCP22', 'L1_ZDCP22', (-1, 2), 1 ],
		 [ 'L1_ZDCM22', 'L1_ZDCM22', (-1, 2), 1 ],
		 [ 'L1_ZDC22_AND', 'L1_ZDC22_AND', (-1, 2), 1 ],

		 [ 'L1_ZDCP80', 'L1_ZDCP80', (-1, 2), 1 ],
		 [ 'L1_ZDCM80', 'L1_ZDCM80', (-1, 2), 1 ],
		 [ 'L1_ZDC80_AND', 'L1_ZDC80_AND', (-1, 2), 1 ],

		 [ 'L1_ZDCP133', 'L1_ZDCP133', (-1, 2), 1 ],
		 [ 'L1_ZDCM133', 'L1_ZDCM133', (-1, 2), 1 ],
		 [ 'L1_ZDC133_AND', 'L1_ZDC133_AND', (-1, 2), 1 ] ],
		 'img/'+prefix+'_UPCSpectra_MBtrig_noBptxGate_normalized.png', 10,
		 density=2)


	dnm.plotVarsState(
		[[ '', df ]],
		[[ 'L1_SingleJet8_NotMinimumBiasHF2_AND_BptxAND', 'L1_SingleJet8_NotMinimumBiasHF2_AND_BptxAND', (-1, 2), 1 ],
		 [ 'L1_SingleJet12_NotMinimumBiasHF2_AND_BptxAND', 'L1_SingleJet12_NotMinimumBiasHF2_AND_BptxAND', (-1, 2), 1 ],
		 [ 'L1_SingleJet16_NotMinimumBiasHF2_AND_BptxAND', 'L1_SingleJet16_NotMinimumBiasHF2_AND_BptxAND', (-1, 2), 1 ],
		 
		 [ 'L1_SingleJet8_ZDC1n_XOR_BptxAND', 'L1_SingleJet8_ZDC1n_XOR_BptxAND', (-1, 2), 1 ],
		 [ 'L1_SingleJet12_ZDC1n_XOR_BptxAND', 'L1_SingleJet12_ZDC1n_XOR_BptxAND', (-1, 2), 1 ],
		 [ 'L1_SingleJet16_ZDC1n_XOR_BptxAND', 'L1_SingleJet16_ZDC1n_XOR_BptxAND', (-1, 2), 1 ] ],
		 'img/'+prefix+'_UPCSpectra_UPCJet_normalized.png', 10,
		 density=2)

def plotHLTTriggerStatus(df, prefix, HLTMBPaths):
	dnm.plotVarsState(
		[[ '', df ]],
		[ [ path, path, (-1, 2), 1 ] for path in HLTMBPaths ],
		 'img/'+prefix+'_UPCSpectra_HLT_MBtrig_normalized.png', 10,
		 density=2)

def plotL1Obj(df, prefix, doJetEtTrigSelStudy=False, HLTMBPaths=[], doLeadingJet=False):
	dnm.plotVarsState(
		[[ '', df ]],
		[[ 'nJets', 'nJets', (0, 16), 1 ],
		 [ 'nSums', 'nSums', (0, 70), 1 ]],
		 'img/'+prefix+'_UPCSpectra_l1.png', 16)

	_jetlist = ['jetEt','jetEta','jetPUEt','jetBx' ]
	df_flatJet = flatten_df(df, _jetlist)

	dnm.plotVarsState(
		[[ '', df_flatJet ]],
		[[ 'jetEta', 'jetEta', (-5, 5) ],
		 [ 'jetEt', 'jetEt', (0, 70) ],
		 [ 'jetPUEt', 'jetPUEt', (0, 100) ]],
		 'img/'+prefix+'_UPCSpectra_l1jet.png', 100)

	dnm.plotVarsState(
		[[ 'no cut', df_flatJet ],
		 [ 'pass PV', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1') ] ],
		 [ 'fail PV', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==0') ] ]],
		[[ 'jetEta', 'jetEta', (-5, 5) ],
		 [ 'jetEt', 'jetEt', (0, 70) ]],
		 'img/'+prefix+'_UPCSpectra_l1jet_PV_normalized.png', 100,
		 # density=2)
		 in_weights=1/df_flatJet.shape[0])

	dnm.plotVarsState(
		[[ '', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0') ] ]],
		[[ 'jetEta', 'jetEta', (-5, 5) ],
		 [ 'jetEt', 'jetEt', (0, 70) ]],
		 'img/'+prefix+'_UPCSpectra_l1jet_cleanedUp_nonMB_normalized.png', 100,
		 density=2)

	dnm.plotVarsState(
		[[ 'PV+~MB', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0') ] ],
		 [ 'PV+~MB+emu(ZDC1n_XOR)', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
		 						       '((sumPlus>1100 & sumMinus<1100) | (sumPlus<1100 & sumMinus>1100))') ] ]],
		[[ 'jetEta', 'jetEta', (-5, 5) ],
		 [ 'jetEt', 'jetEt', (0, 70) ]],
		 'img/'+prefix+'_UPCSpectra_l1jet_cleanedUp_emuzdcxor_normalized.png', 100,
		 # density=2)
		 in_weights=1/df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0') ].shape[0])

	dnm.plotVarsState(
		[[ '(1)ZDCXOR+Jet8', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & HLT_HIUPC_SingleJet8_ZDC1nXOR_MaxPixelCluster50000_v2==1') ] ],
		 [ '(2)NotHFAND+Jet8', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & HLT_HIUPC_SingleJet8_NotMBHF2AND_MaxPixelCluster50000_v2==1') ] ],
		 [ '(1)+(2)', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & HLT_HIUPC_SingleJet8_ZDC1nXOR_MaxPixelCluster50000_v2==1 & HLT_HIUPC_SingleJet8_NotMBHF2AND_MaxPixelCluster50000_v2==1') ] ],
		],
		[[ 'jetEta', 'jetEta', (-5, 5) ],
		 [ 'jetEt', 'jetEt', (0, 70) ]],
		 'img/'+prefix+'_UPCSpectra_l1jet_cleanedUp_lowptJetTriggered_normalized.png', 100,
		 density=2)

	_sumlist = ['sumType','sumEt','sumPhi','sumBx' ]
	df_flatSum = flatten_df(df, _sumlist)

	dnm.plotVarsState(
		[[ '', df_flatSum ]],
		[[ 'sumType', 'sumType', (0, 30) ],
		 [ 'sumEt', 'sumEt', (0, 100), 1 ],
		 [ 'sumPhi', 'sumPhi', (-np.pi, np.pi), 1 ]],
		 'img/'+prefix+'_UPCSpectra_l1sum.png', 100)

	if (doJetEtTrigSelStudy):
		dnm.plotVarsState(
			[[ 'PV+~L1_HF1', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0') ] ],
			 [ 'PV+~L1_HF2', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF2_AND_BptxAND==0') ] ],
			 [ 'PV+~L1_ZDC1n_OR', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_ZDC1n_OR_BptxAND==0') ] ],
			 [ 'PV+~L1_ZDC1n_OR_HF1', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_ZDC1n_OR_MinimumBiasHF1_AND_BptxAND==0') ] ],
			 [ 'PV+~L1_ZDC1n_OR_HF2', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_ZDC1n_OR_MinimumBiasHF2_AND_BptxAND==0') ] ],
			 ],
			[[ 'jetEta', 'jetEta', (-5, 5) ],
			 [ 'jetEt', 'jetEt', (0, 70) ]],
			 'img/'+prefix+'_UPCSpectra_l1jet_PV_L1_NMB1_normalized.png', 100,
			 density=2)

		dnm.plotVarsState(
			[[ 'PV+~L1_ZDC1n_XOR_HF1', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_ZDC1n_XOR_MinimumBiasHF1_AND_BptxAND==0') ] ],
			 [ 'PV+~L1_ZDC1n_XOR_HF2', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_ZDC1n_XOR_MinimumBiasHF2_AND_BptxAND==0') ] ],
			 [ 'PV+~L1_ZDC2n_OR_HF1', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_ZDC2n_OR_MinimumBiasHF1_AND_BptxAND==0') ] ],
			 [ 'PV+~L1_ZDC2n_OR_HF2', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_ZDC2n_OR_MinimumBiasHF2_AND_BptxAND==0') ] ],
			 [ 'PV+~L1_ZDC3n_OR_HF1', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_ZDC3n_OR_MinimumBiasHF1_AND_BptxAND==0') ] ],
			 [ 'PV+~L1_ZDC3n_OR_HF2', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_ZDC3n_OR_MinimumBiasHF2_AND_BptxAND==0') ] ]
			 ],
			[[ 'jetEta', 'jetEta', (-5, 5) ],
			 [ 'jetEt', 'jetEt', (0, 70) ]],
			 'img/'+prefix+'_UPCSpectra_l1jet_PV_L1_NMB2_normalized.png', 100,
			 density=2)

		dnm.plotVarsState(
			[[ 'PV+L1_HF1', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==1') ] ],
			 [ 'PV+L1_HF2', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF2_AND_BptxAND==1') ] ],
			 [ 'PV+L1_ZDC1n_OR', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_ZDC1n_OR_BptxAND==1') ] ],
			 [ 'PV+L1_ZDC1n_OR_HF1', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_ZDC1n_OR_MinimumBiasHF1_AND_BptxAND==1') ] ],
			 [ 'PV+L1_ZDC1n_OR_HF2', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_ZDC1n_OR_MinimumBiasHF2_AND_BptxAND==1') ] ],
			 ],
			[[ 'jetEta', 'jetEta', (-5, 5) ],
			 [ 'jetEt', 'jetEt', (0, 70) ]],
			 'img/'+prefix+'_UPCSpectra_l1jet_PV_L1_MB1_normalized.png', 100,
			 density=2)

		dnm.plotVarsState(
			[[ 'PV+L1_ZDC1n_XOR_HF1', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_ZDC1n_XOR_MinimumBiasHF1_AND_BptxAND==1') ] ],
			 [ 'PV+L1_ZDC1n_XOR_HF2', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_ZDC1n_XOR_MinimumBiasHF2_AND_BptxAND==1') ] ],
			 [ 'PV+L1_ZDC2n_OR_HF1', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_ZDC2n_OR_MinimumBiasHF1_AND_BptxAND==1') ] ],
			 [ 'PV+L1_ZDC2n_OR_HF2', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_ZDC2n_OR_MinimumBiasHF2_AND_BptxAND==1') ] ],
			 [ 'PV+L1_ZDC3n_OR_HF1', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_ZDC3n_OR_MinimumBiasHF1_AND_BptxAND==1') ] ],
			 [ 'PV+L1_ZDC3n_OR_HF2', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & L1_ZDC3n_OR_MinimumBiasHF2_AND_BptxAND==1') ] ]
			 ],
			[[ 'jetEta', 'jetEta', (-5, 5) ],
			 [ 'jetEt', 'jetEt', (0, 70) ]],
			 'img/'+prefix+'_UPCSpectra_l1jet_PV_L1_MB2_normalized.png', 100,
			 density=2)

		legendArr 	= [ name.replace('HLT_HIMinimumBiasHF1AND','HLT_HF1') for name in HLTMBPaths ]
		cutArr 		= [ 'pprimaryVertexFilter==1 & ' + name + ' == ' for name in HLTMBPaths ]

		dnm.plotVarsState(
			[[ 'PV+~'+leg, df_flatJet[ df_flatJet.eval(cut+'0') ] ] for (leg, cut) in zip(legendArr, cutArr) ],
			[[ 'jetEta', 'jetEta', (-5, 5) ],
			 [ 'jetEt', 'jetEt', (0, 70) ]],
			 'img/'+prefix+'_UPCSpectra_l1jet_PV_HLT_NMB_normalized.png', 100,
			 density=2)

		dnm.plotVarsState(
			[[ 'PV+'+leg, df_flatJet[ df_flatJet.eval(cut+'1') ] ] for (leg, cut) in zip(legendArr, cutArr) ],
			[[ 'jetEta', 'jetEta', (-5, 5) ],
			 [ 'jetEt', 'jetEt', (0, 70) ]],
			 'img/'+prefix+'_UPCSpectra_l1jet_PV_HLT_MB_normalized.png', 100,
			 density=2)


		dnm.plotVarsState(
			[[ '(1) PV', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1') ] ],
			 [ '(1)+0<jetEt<8', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & jetEt < 8') ] ],
			 [ '(1)+8<jetEt<12', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & jetEt >= 8 & jetEt < 12') ] ],
			 [ '(1)+12<jetEt<16', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & jetEt >= 12 & jetEt < 16') ] ],
			 [ '(1)+16<jetEt<20', df_flatJet[ df_flatJet.eval('pprimaryVertexFilter==1 & jetEt >= 16 & jetEt < 20') ] ]],
			[[ 'jetEta', 'jetEta', (-5, 5) ],
			 [ 'jetEt', 'jetEt', (0, 70) ]],
			 'img/'+prefix+'_UPCSpectra_l1jetEtDep.png', 100)

	del df_flatJet
	del df_flatSum
	gc.collect()
	print(gc.garbage)

	if (doLeadingJet):
		df_sub = df[ df.eval('nJets!=0') ].copy(deep=True)
		df_sub['jetEtMax'] 	= df_sub['jetEt'].apply(max)
		df_sub['jetEta_EtMax'] 	= df_sub[['jetEt','jetEta']].apply(lambda x: x.jetEta[np.argmax(x.jetEt)], axis=1)

		dnm.plotVarsState(
			[[ 'no cut', df_sub ],
			 [ 'pass PV', df_sub[ df_sub.eval('pprimaryVertexFilter==1') ] ],
			 [ 'fail PV', df_sub[ df_sub.eval('pprimaryVertexFilter==0') ] ]],
			[[ 'jetEta_EtMax', 'leading jetEta', (-5, 5) ],
			 [ 'jetEtMax', 'leading jetEt', (0, 70) ]],
			 'img/'+prefix+'_UPCSpectra_l1Leadingjet_PV_normalized.png', 100,
			 # density=2)
			 in_weights=1/df_sub.shape[0])

		dnm.plotVarsState(
			[[ '', df_sub[ df_sub.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0') ] ]],
			[[ 'jetEta_EtMax', 'leading jetEta', (-5, 5) ],
			 [ 'jetEtMax', 'leading jetEt', (0, 70) ]],
			 'img/'+prefix+'_UPCSpectra_l1Leadingjet_cleanedUp_nonMB_normalized.png', 100,
			 density=2)

		dnm.plotVarsState(
			[[ 'PV+~MB', df_sub[ df_sub.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0') ] ],
			 [ 'PV+~MB+emu(ZDC1n_XOR)', df_sub[ df_sub.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
			 						       '((sumPlus>1100 & sumMinus<1100) | (sumPlus<1100 & sumMinus>1100))') ] ]],
			[[ 'jetEta_EtMax', 'leading jetEta', (-5, 5) ],
			 [ 'jetEtMax', 'leading jetEt', (0, 70) ]],
			 'img/'+prefix+'_UPCSpectra_l1Leadingjet_cleanedUp_emuzdcxor_normalized.png', 100,
			 # density=2)
			 in_weights=1/df_sub[ df_sub.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0') ].shape[0])

		dnm.plotVarsState(
			[[ '(1)ZDCXOR+Jet8', df_sub[ df_sub.eval('pprimaryVertexFilter==1 & HLT_HIUPC_SingleJet8_ZDC1nXOR_MaxPixelCluster50000_v2==1') ] ],
			 [ '(2)NotHFAND+Jet8', df_sub[ df_sub.eval('pprimaryVertexFilter==1 & HLT_HIUPC_SingleJet8_NotMBHF2AND_MaxPixelCluster50000_v2==1') ] ],
			 [ '(1)+(2)', df_sub[ df_sub.eval('pprimaryVertexFilter==1 & HLT_HIUPC_SingleJet8_ZDC1nXOR_MaxPixelCluster50000_v2==1 & HLT_HIUPC_SingleJet8_NotMBHF2AND_MaxPixelCluster50000_v2==1') ] ],
			],
			[[ 'jetEta_EtMax', 'leading jetEta', (-5, 5) ],
			 [ 'jetEtMax', 'leading jetEt', (0, 70) ]],
			 'img/'+prefix+'_UPCSpectra_l1Leadingjet_cleanedUp_lowptJetTriggered_normalized.png', 100,
			 density=2)
	del df_sub
	gc.collect()
	print(gc.garbage)

def plotPV(df, prefix):
	dnm.plotVarsState(
		[[ 'pass PV', df[ df.eval('pprimaryVertexFilter==1') ] ],
		 [ 'fail PV', df[ df.eval('pprimaryVertexFilter==0') ] ] ],
		[[ 'nVtx', 'nVtx', (0, 10), 1 ]],
		 'img/'+prefix+'_UPCSpectra_PV.png', 10)

	_vtxlist = [ 'xVtx', 'yVtx', 'zVtx',
		  'xErrVtx', 'yErrVtx', 'zErrVtx',
		  'chi2Vtx', 'ndofVtx', 'isFakeVtx', 
		  'nTracksVtx', 'ptSumVtx' ]
	df_flatVtx = flatten_df(df, _vtxlist)

	dnm.plotVarsState(
		[[ 'pass PV', df_flatVtx[ df_flatVtx.eval('pprimaryVertexFilter==1') ] ],
		 [ 'fail PV', df_flatVtx[ df_flatVtx.eval('pprimaryVertexFilter==0') ] ] ],
		[[ 'xVtx', 'xVtx', (-0.5, 0.5), 1 ],
		 [ 'yVtx', 'yVtx', (-0.5, 0.5), 1 ],
		 [ 'zVtx', 'zVtx', (-0.5, 0.5), 1 ],

		 [ 'xErrVtx', 'xErrVtx', (0, 0.5), 1 ],
		 [ 'yErrVtx', 'yErrVtx', (0, 0.5), 1 ],
		 [ 'zErrVtx', 'zErrVtx', (0, 0.5), 1 ],

		 [ 'chi2Vtx', 'chi2Vtx', (0, 5), 1 ],
		 [ 'ndofVtx', 'ndofVtx', (0, 15) ],
		 [ 'isFakeVtx', 'isFakeVtx', (-1, 2) ],
		 
		 [ 'nTracksVtx', 'nTracksVtx', (0, 10) ],
		 [ 'ptSumVtx', 'ptSumVtx', (0, 300), 1 ]],
		 'img/'+prefix+'_UPCSpectra_vtx.png', 100)

def plotNTrk(df, prefix):
	dnm.plotVarsState(
		[[ '(1)PV', df[ df.eval('pprimaryVertexFilter==1') ] ],
		 [ '(2)PV+~MB', df[ df.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0') ] ],
		 [ '(2)+ZDCB(th=1100)', df[ df.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
		 					   'sumPlus>1100 & sumMinus>1100') ] ] ,
		 [ '(2)+ZDCP(th=1100)', df[ df.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
		 					   'sumPlus>1100 & sumMinus<1100') ] ] ,
		 [ '(2)+ZDCM(th=1100)', df[ df.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
		 					   'sumPlus<1100 & sumMinus>1100') ] ] ],
		[[ 'nTrk', 'nTrk', (0, 6500)   ],
		 [ 'nTrk', 'nTrk', (0, 6500), 1],
		 [ 'nTrk', 'nTrk', (0, 1500), 1] ],
		 'img/'+prefix+'_UPCSpectra.png', 100)

	dnm.plotVarsState(
		[[ '(2)PV+~MB', df[ df.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0') ] ],
		 [ '(2)+ZDCB(th=1100)', df[ df.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
		 					   'sumPlus>1100 & sumMinus>1100') ] ] ,
		 [ '(2)+ZDCB(th=1500)', df[ df.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
		 					   'sumPlus>1500 & sumMinus>1500') ] ] ,
		 [ '(2)+ZDCB(th=2000)', df[ df.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
		 					   'sumPlus>2000 & sumMinus>2000') ] ] ,
		 [ '(2)+ZDCB(th=2500)', df[ df.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
		 					   'sumPlus>2500 & sumMinus>2500') ] ] ],
		[[ 'nTrk', 'nTrk', (0, 6500)   ],
		 [ 'nTrk', 'nTrk', (0, 6500), 1],
		 [ 'nTrk', 'nTrk', (0, 1500), 1]  ],
		 'img/'+prefix+'_UPCSpectra_ZDCB.png', 100)

	dnm.plotVarsState(
		[[ '(2)PV+~MB', df[ df.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0') ] ],
		 [ '(2)+ZDCP(th=1100)', df[ df.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
		 					   'sumPlus>1100 & sumMinus<1100') ] ] ,
		 [ '(2)+ZDCP(th=1500)', df[ df.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
		 					   'sumPlus>1500 & sumMinus<1500') ] ] ,
		 [ '(2)+ZDCP(th=2000)', df[ df.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
		 					   'sumPlus>2000 & sumMinus<2000') ] ] ,
		 [ '(2)+ZDCP(th=2500)', df[ df.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
		 					   'sumPlus>2500 & sumMinus<2500') ] ] ],
		[[ 'nTrk', 'nTrk', (0, 6500)   ],
		 [ 'nTrk', 'nTrk', (0, 6500), 1],
		 [ 'nTrk', 'nTrk', (0, 1500), 1]  ],
		 'img/'+prefix+'_UPCSpectra_ZDCP.png', 100)

	dnm.plotVarsState(
		[[ '(2)PV+~MB', df[ df.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0') ] ],
		 [ '(2)+ZDCM(th=1100)', df[ df.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
		 					   'sumPlus<1100 & sumMinus>1100') ] ] ,
		 [ '(2)+ZDCM(th=1500)', df[ df.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
		 					   'sumPlus<1500 & sumMinus>1500') ] ] ,
		 [ '(2)+ZDCM(th=2000)', df[ df.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
		 					   'sumPlus<2000 & sumMinus>2000') ] ] ,
		 [ '(2)+ZDCM(th=2500)', df[ df.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
		 					   'sumPlus<2500 & sumMinus>2500') ] ] ],
		[[ 'nTrk', 'nTrk', (0, 6500)   ],
		 [ 'nTrk', 'nTrk', (0, 6500), 1],
		 [ 'nTrk', 'nTrk', (0, 1500), 1] ],
		 'img/'+prefix+'_UPCSpectra_ZDCM.png', 100)

def plotZDC(df, prefix):
	dnm.plotVarsState(
		[[ '', df ]],
		[[ 'sumPlus', 'sumPlus', (-30e3, 200e3) ],
		 [ 'sumPlus', 'sumPlus', (-30e3, 200e3), 1 ],
		 [ 'sumPlus', 'sumPlus', (-3e3, 3e3), 1 ],

		 [ 'sumMinus', 'sumMinus', (-30e3, 200e3) ],
		 [ 'sumMinus', 'sumMinus', (-30e3, 200e3), 1 ],
		 [ 'sumMinus', 'sumMinus', (-3e3, 3e3), 1 ]],
		 'img/'+prefix+'_UPCSpectra_zdc.png', 100)

def plotDCand(df, prefix):
	_dcandlist = [  'Dmass', 'D_unfitted_mass', 'DsvpvDistance',
			'Dpt', 'D_unfitted_pt',
			'Deta','Dphi',
			'DvtxX', 'DvtxY', 'DvtxZ',
			'Dd0', 'Dd0Err', 'Ddca',
			'Dchi2ndf', 'Dchi2cl', 'Dalpha']
	df_flatDcand = flatten_df(df, _dcandlist)

		
	dnm.plotVarsState(
		[[ 'no cut', df_flatDcand ],
		 [ 'PV+~MB', df_flatDcand[ df_flatDcand.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0') ] ],
		 [ 'PV+~MB+ZDCP(th=1100)', df_flatDcand[ df_flatDcand.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
				 					   'sumPlus>1100 & sumMinus<1100') ] ] ],
		[[ 'Dmass', 'Dmass', (1.7, 2.05) ],
		 [ 'D_unfitted_mass', 'D_unfitted_mass', (1.7, 2.05) ],
		 [ 'DsvpvDistance', 'DsvpvDistance', (0, 15), 1 ],

		 [ 'Dpt', 'Dpt', (0, 10) ],
		 [ 'Deta', 'Deta', (-3.5, 3.5) ],
		 [ 'Dphi', 'Dphi', (-np.pi, np.pi) ],

		 [ 'D_unfitted_pt', 'D_unfitted_pt', (0, 10) ]],
		 'img/'+prefix+'_UPCSpectra_Dcand_kin.png', 100)

	dnm.plotVarsState(
		[[ 'no cut', df_flatDcand ],
		 [ 'PV+~MB', df_flatDcand[ df_flatDcand.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0') ] ],
		 [ 'PV+~MB+ZDCP(th=1100)', df_flatDcand[ df_flatDcand.eval('pprimaryVertexFilter==1 & L1_MinimumBiasHF1_AND_BptxAND==0 & '
				 					   'sumPlus>1100 & sumMinus<1100') ] ] ],
		[[ 'DvtxX', 'DvtxX', (-3, 3), 1 ],
		 [ 'DvtxY', 'DvtxY', (-3, 3), 1 ],
		 [ 'DvtxZ', 'DvtxZ', (-3, 3), 1 ],

		 [ 'Dd0', 'Dd0', (0, 10), 1 ],
		 [ 'Dd0Err', 'Dd0Err', (0, 10), 1 ],
		 [ 'Ddca', 'Ddca', (0, 5), 1 ],
		 
		 [ 'Dchi2ndf', 'Dchi2ndf', (0, 4), 1 ],
		 [ 'Dchi2cl', 'Dchi2cl', (0, 1) ],
		 [ 'Dalpha', 'Dalpha', (0, np.pi), 1 ]],
		 'img/'+prefix+'_UPCSpectra_Dcand_fit.png', 100)

def getFileList(inFileName):
	fileList = []
	if len(inFileName) < 5:
		print("[Error] Given inFileName \'", inFileName, "\' is invalid, exit 1." )
		sys.exit(1)
	elif ".txt" in inFileName:
		if (np.genfromtxt(inFileName, dtype=str).ndim==0):
			fileList.append(str(np.genfromtxt(inFileName, dtype=str)))
		else:
			fileList = list(np.genfromtxt(inFileName, dtype=str))
	elif ".root" in inFileName:
	        fileList.append(inFileName)
	else:
		print("[Error] Given inFileName \'", inFileName, "\' is invalid, exit 1." )
		sys.exit(1)
	return(fileList)

def flatten_df(df, flatten_arr):
	df_flatVtx 		= df.copy(deep=True)
	df_flatVtx[flatten_arr] = df_flatVtx[flatten_arr].apply(lambda x: x.tolist())
	df_flatVtx 		= df_flatVtx.explode( flatten_arr )
	df_flatVtx[flatten_arr] = df_flatVtx[flatten_arr].astype(float)
	return df_flatVtx

if __name__ == '__main__':
	main()
