import os
import glob as glob


runsList = [
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374719/*/*/',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374728/*/*/',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374729/*/*/',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374730/*/*/',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374731/*/*/',
	'/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374751/*/*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	'/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374752/*/*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	'/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374753/*/*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	'/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374754/*/*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	'/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374763/*/*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	'/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374764/*/*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	'/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374765/*/*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	'/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374766/*/*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root'
]


for run in runsList:
	dataset = glob.glob(run)
	print('Totaling', len(dataset), 'files' )
	f = open("file_run{}.txt".format(run.split('crab_HIForwardStreamers_')[1].split('/')[0]), "w")
	f.write('\n'.join(dataset))
	f.close()
	os.system('sed -i -e "s#/eos/cms#root://eoscms.cern.ch/#" file_run{}.txt'.format(
		run.split('crab_HIForwardStreamers_')[1].split('/')[0],
		))
