import os, sys
import pandas as pd
import numpy as np
import ROOT
import uproot
sys.path.append('/afs/cern.ch/user/y/yuchenc/DataCompression/python/utils/')
import DfNtupleMgr as dnm
import PlotUtils as pu
import awkward as ak

def main():
	inFileName = sys.argv[1]
	prefix 	 = os.path.basename(inFileName).replace('.root','') if '.root' in inFileName else \
		   os.path.basename(inFileName).replace('.txt','')

	fileList = getFileList(inFileName)

	tSkimHLT, tHLT, tL1, tTrack, tZDC, tDfinder = [], [], [], [], [], []
	nEvtMax, nEvtMaxCounter = 50000, 50000

	for filepath in fileList:
		if nEvtMaxCounter <= 0: break
		print(filepath, nEvtMaxCounter)
		tSkimHLT.append(uproot.open(filepath).key('skimanalysis/HltTree').get(). \
			arrays(['pprimaryVertexFilter'], library='pd') )
		
		tHLT.append( 	uproot.open(filepath).key('hltanalysis/HltTree').get(). \
			arrays(['L1_MinimumBiasHF1_AND_BptxAND',
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
				'L1_SingleJet8_ZDC1n_XOR_BptxAND','L1_SingleJet12_ZDC1n_XOR_BptxAND','L1_SingleJet16_ZDC1n_XOR_BptxAND' 
				], library='pd') )

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

		nEvtMaxCounter -= tSkimHLT[-1].shape[0]

	print(tSkimHLT)
	print(tHLT)
	print(tL1)
	print(tTrack)
	print(tZDC)
	print(tDfinder)
	
	tSkimHLT 	= pd.concat(tSkimHLT)
	tHLT 		= pd.concat(tHLT)
	tL1 		= pd.concat(tL1)
	tTrack 		= pd.concat(tTrack)
	tZDC 		= pd.concat(tZDC)
	tDfinder 	= pd.concat(tDfinder)
	if nEvtMax > tSkimHLT.shape[0]: nEvtMax = tSkimHLT.shape[0]

	tSkimHLT	= tSkimHLT[:nEvtMax]
	tHLT		= tHLT[:nEvtMax]
	tL1		= tL1[:nEvtMax]
	tTrack		= tTrack[:nEvtMax]
	tZDC		= tZDC[:nEvtMax]
	tDfinder	= tDfinder[:nEvtMax]

	print(tSkimHLT)
	print(tHLT)
	print(tL1)
	print(tTrack)
	print(tZDC)
	print(tDfinder)

	df 	= pd.concat([tSkimHLT, tHLT, tL1, tTrack, tZDC, tDfinder], axis=1)

	print(df.shape)

	plotL1TriggerStatus(df, prefix)
	plotL1Obj(df, prefix)
	plotPV(df, prefix)
	plotNTrk(df, prefix)
	plotZDC(df, prefix)
	plotDCand(df, prefix)

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

def plotL1Obj(df, prefix):
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
		 [ 'jetEt', 'jetEt', (0, 100) ],
		 [ 'jetPUEt', 'jetPUEt', (0, 100) ]],
		 'img/'+prefix+'_UPCSpectra_l1jet.png', 100)


	_sumlist = ['sumType','sumEt','sumPhi','sumBx' ]
	df_flatSum = flatten_df(df, _sumlist)

	dnm.plotVarsState(
		[[ '', df_flatSum ]],
		[[ 'sumType', 'sumType', (0, 30) ],
		 [ 'sumEt', 'sumEt', (0, 100), 1 ],
		 [ 'sumPhi', 'sumPhi', (-np.pi, np.pi), 1 ]],
		 'img/'+prefix+'_UPCSpectra_l1sum.png', 100)

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
