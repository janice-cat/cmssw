import os
import glob as glob


runsList = [
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374719/*/*/',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374728/*/*/',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374729/*/*/',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374730/*/*/',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374730/231004_121156/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374731/*/*/',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374751/*/*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374752/*/*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374753/*/*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374754/*/*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374763/*/*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374764/*/*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374765/*/*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374766/*/*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root'
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374767/231005_134903/0000/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root'
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374768/231005_134939/0000/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root'
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374803/231006_100504/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root'
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374810_1/231006_102702/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374810_2/231006_102810/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374778/231007_144102/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374804/231007_144401/0000/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374828/231007_144218/0000/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374833/231007_144019/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374834/231007_144448/0000/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374925/231010_094326/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_375002/231011_190013/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374970/231011_121811/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_374997/231011_185830/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_375007/231012_083828/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_375058/231013_065604/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_375060/231013_065734/0000/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_375064/231013_135433/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	# '/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_375110/231013_220544/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	'/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_375013/231012_213248/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	'/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_375055/231012_225551/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	'/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_375145/231015_085115/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	'/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_375164/231015_085155/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
	'/eos/cms/store/group/phys_heavyions/pchou/RAW2DIGI/CRAB_UserFiles/crab_HIForwardStreamers_375195/231015_120728/000*/reco_RAW2DIGI_L1Reco_RECO_PAT_inMINIAOD_*.root',
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
