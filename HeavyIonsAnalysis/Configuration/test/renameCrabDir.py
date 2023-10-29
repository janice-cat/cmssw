import os, sys
import glob as glob


jobsList = [
	# 'run374731_0000',
	# 'run374730_0003',
	# 'run374730_0002',
	# 'run374730_0001',
	# 'run374730_0000',
	# 'run374729_0000',
	# 'run374728_0000',
	# 'run374719_0008',
	# 'run374719_0007',
	# 'run374719_0006',
	# 'run374719_0005',
	# 'run374719_0004',
	# 'run374719_0003',
	# 'run374719_0002',
	# 'run374719_0001',
	# 'run374719_0000',
	# 'run374751',
	# 'run374752',
	# 'run374753',
	# 'run374754',
	# 'run374763',
	# 'run374764',
	# 'run374765',
	# 'run374766',
	# 'run374767',
	# 'run374768',
	# 'run374803',
	# 'run374803_lowerDcut',
	# 'run374810_1',
	# 'run374810_1_lowerDcut',
	# 'run374810_2',
	# 'run374810_2_lowerDcut',
	# 'run374834',
	# 'run374833',
	# 'run374828',
	# 'run374804',
	# 'run374778',
	# 'run374834_lowerDcut',
	# 'run374833_lowerDcut',
	# 'run374828_lowerDcut',
	# 'run374804_lowerDcut',
	# 'run374778_lowerDcut',
	# 'run374925',
	# 'run374925_lowerDcut',
	# 'run375002',
	# 'run375002_lowerDcut',
	# 'run374970',
	# 'run374970_lowerDcut',
	# 'run374997',
	# 'run374997_lowerDcut',
	# 'run375110',
	# 'run375110_lowerDcut',
	# 'run375007',
	# 'run375007_lowerDcut',
	# 'run375064',
	# 'run375064_lowerDcut',
	# 'run375060',
	# 'run375060_lowerDcut',
	# 'run375058',
	# 'run375058_lowerDcut',
	# 'run375013',
	# 'run375013_lowerDcut',
	# 'run375055',
	# 'run375055_lowerDcut',
	# 'run375145',
	# 'run375145_lowerDcut',
	# 'run375164',
	# 'run375164_lowerDcut',
	# 'run375195',
	# 'run375195_lowerDcut',
	'run375202_lowerDcut',
	# 'run375245_lowerDc0ut',
	'run375252_lowerDcut',
	# 'run375256_lowerDcut',
	'run375259_lowerDcut',
	'run375300_lowerDcut',
	'run375317_lowerDcut',
	# 'run375202', 
	# 'run375245',
	# 'run375252',
	# 'run375256',
	# 'run375259',
	# 'run375300',
	# 'run375317',
	# 'promptReco_run374804_lowerDcut/HIForward0',
	# 'promptReco_run374804_lowerDcut/HIForward1',
	# 'promptReco_run374804_lowerDcut/HIForward2',
	# 'promptReco_run374804_lowerDcut/HIForward3',
	# 'promptReco_run374804_lowerDcut/HIForward4',
	# 'promptReco_run374804_lowerDcut/HIForward5',
	# 'promptReco_run374804_lowerDcut/HIForward6',
	# 'promptReco_run374804_lowerDcut/HIForward7',
	# 'promptReco_run374804_lowerDcut/HIForward8',
	# 'promptReco_run374804_lowerDcut/HIForward9',
	# 'promptReco_run374804_lowerDcut/HIForward10',
	# 'promptReco_run374804_lowerDcut/HIForward11',
	# 'promptReco_run374804_lowerDcut/HIForward12',
	# 'promptReco_run374804_lowerDcut/HIForward13',
	# 'promptReco_run374804_lowerDcut/HIForward14',
	# 'promptReco_run374804_lowerDcut/HIForward15',
	# 'promptReco_run374804_lowerDcut/HIForward16',
	# 'promptReco_run374804_lowerDcut/HIForward17',
	# 'promptReco_run374804_lowerDcut/HIForward18',
	# 'promptReco_run374804_lowerDcut/HIForward19',
	# 'promptReco_run374804/HIForward0',
	# 'promptReco_run374804/HIForward1',
	# 'promptReco_run374804/HIForward2',
	# 'promptReco_run374804/HIForward3',
	# 'promptReco_run374804/HIForward4',
	# 'promptReco_run374804/HIForward5',
	# 'promptReco_run374804/HIForward6',
	# 'promptReco_run374804/HIForward7',
	# 'promptReco_run374804/HIForward8',
	# 'promptReco_run374804/HIForward9',
	# 'promptReco_run374804/HIForward10',
	# 'promptReco_run374804/HIForward11',
	# 'promptReco_run374804/HIForward12',
	# 'promptReco_run374804/HIForward13',
	# 'promptReco_run374804/HIForward14',
	# 'promptReco_run374804/HIForward15',
	# 'promptReco_run374804/HIForward16',
	# 'promptReco_run374804/HIForward17',
	# 'promptReco_run374804/HIForward18',
	# 'promptReco_run374804/HIForward19',
	'promptReco_run374997_lowerDcut/HIForward0',
	'promptReco_run374997_lowerDcut/HIForward1',
	'promptReco_run374997_lowerDcut/HIForward2',
	'promptReco_run374997_lowerDcut/HIForward3',
	'promptReco_run374997_lowerDcut/HIForward4',
	'promptReco_run374997_lowerDcut/HIForward5',
	'promptReco_run374997_lowerDcut/HIForward6',
	'promptReco_run374997_lowerDcut/HIForward7',
	'promptReco_run374997_lowerDcut/HIForward8',
	'promptReco_run374997_lowerDcut/HIForward9',
	'promptReco_run374997_lowerDcut/HIForward10',
	'promptReco_run374997_lowerDcut/HIForward11',
	'promptReco_run374997_lowerDcut/HIForward12',
	'promptReco_run374997_lowerDcut/HIForward13',
	'promptReco_run374997_lowerDcut/HIForward14',
	'promptReco_run374997_lowerDcut/HIForward15',
	'promptReco_run374997_lowerDcut/HIForward16',
	'promptReco_run374997_lowerDcut/HIForward17',
	'promptReco_run374997_lowerDcut/HIForward18',
	'promptReco_run374997_lowerDcut/HIForward19',
	# 'promptReco_run374997/HIForward0',
	# 'promptReco_run374997/HIForward1',
	# 'promptReco_run374997/HIForward2',
	# 'promptReco_run374997/HIForward3',
	# 'promptReco_run374997/HIForward4',
	# 'promptReco_run374997/HIForward5',
	# 'promptReco_run374997/HIForward6',
	# 'promptReco_run374997/HIForward7',
	# 'promptReco_run374997/HIForward8',
	# 'promptReco_run374997/HIForward9',
	# 'promptReco_run374997/HIForward10',
	# 'promptReco_run374997/HIForward11',
	# 'promptReco_run374997/HIForward12',
	# 'promptReco_run374997/HIForward13',
	# 'promptReco_run374997/HIForward14',
	# 'promptReco_run374997/HIForward15',
	# 'promptReco_run374997/HIForward16',
	# 'promptReco_run374997/HIForward17',
	# 'promptReco_run374997/HIForward18',
	# 'promptReco_run374997/HIForward19',
	'promptReco_run375013_lowerDcut/HIForward0',
	'promptReco_run375013_lowerDcut/HIForward1',
	'promptReco_run375013_lowerDcut/HIForward2',
	'promptReco_run375013_lowerDcut/HIForward3',
	# 'promptReco_run375013_lowerDcut/HIForward4',
	'promptReco_run375013_lowerDcut/HIForward5',
	'promptReco_run375013_lowerDcut/HIForward6',
	# 'promptReco_run375013_lowerDcut/HIForward7',
	# 'promptReco_run375013_lowerDcut/HIForward8',
	'promptReco_run375013_lowerDcut/HIForward9',
	'promptReco_run375013_lowerDcut/HIForward10',
	# 'promptReco_run375013_lowerDcut/HIForward11',
	'promptReco_run375013_lowerDcut/HIForward12',
	'promptReco_run375013_lowerDcut/HIForward13',
	'promptReco_run375013_lowerDcut/HIForward14',
	# 'promptReco_run375013_lowerDcut/HIForward15',
	'promptReco_run375013_lowerDcut/HIForward16',
	'promptReco_run375013_lowerDcut/HIForward17',
	# 'promptReco_run375013_lowerDcut/HIForward18',
	# 'promptReco_run375013_lowerDcut/HIForward19',
	# 'promptReco_run375013/HIForward0',
	'promptReco_run375013/HIForward1',
	# 'promptReco_run375013/HIForward2',
	# 'promptReco_run375013/HIForward3',
	# 'promptReco_run375013/HIForward4',
	# 'promptReco_run375013/HIForward5',
	# 'promptReco_run375013/HIForward6',
	# 'promptReco_run375013/HIForward7',
	# 'promptReco_run375013/HIForward8',
	'promptReco_run375013/HIForward9',
	'promptReco_run375013/HIForward10',
	# 'promptReco_run375013/HIForward11',
	# 'promptReco_run375013/HIForward12',
	'promptReco_run375013/HIForward13',
	# 'promptReco_run375013/HIForward14',
	# 'promptReco_run375013/HIForward15',
	'promptReco_run375013/HIForward16',
	# 'promptReco_run375013/HIForward17',
	# 'promptReco_run375013/HIForward18',
	'promptReco_run375013/HIForward19',
]


for job in jobsList[::-1]:
	os.system('crab status -d forestFowardPDs/crab_{}'.format(job.replace('/','_')))
	oldDirNames = 	glob.glob('/eos/cms/store/group/phys_heavyions/yuchenc/run3RapidValidation/'+job+'/CRAB_UserFiles/crab_'+job+'/*/*/') if 'promptReco' not in job else \
			glob.glob('/eos/cms/store/group/phys_heavyions/yuchenc/run3RapidValidation/'+job+'/crab_'+job.replace('/','_')+'/*/*/')
	answer = input('Mode: [s: successful -> rename; f: fail -> resubmit; n: not doing anything]')

	if answer == 's':
		for oldDirName in oldDirNames:
			os.system('ls {} | grep -c ""'.format(oldDirName))
			newDirName = 	oldDirName.replace('/CRAB_UserFiles/crab_'+job+'/','/') if 'promptReco' not in job else \
					oldDirName.replace('/crab_'+job.replace('/','_')+'/','/')
			print('This is old dir name:\t\t' , oldDirName)
			print('This will be new dir name:\t' , newDirName)
			answer2 = input('Want to rename?[0/1]')
			if (answer2=='1'):
				os.system('mkdir -p '+'/'.join(newDirName.split('/')[:-2]))
				os.system('eos file rename {} {}'.format(oldDirName, newDirName))
				os.system('ls {} | grep -c ""'.format(newDirName))
			elif (answer2=='0'):
				print('Skip renaming')
			else:
				print('Ambiguous input:', answer2, '. Should be [0/1]')
				sys.exit(0)
			print('-----'*20)

	elif answer == 'f':
		answer2 = input('Resubmit runtime, memory? [default=900, 5000]')
		runtime, memory = 900, 5000
		if (answer2!=''): runtime, memory = answer2.split(',')[0].strip(' '), answer2.split(',')[1].strip(' ')
		answer2 = input('crab resubmit -d forestFowardPDs/crab_{} --maxjobruntime={} --maxmemory={} [confirm 0/1?]'.format(
			job.replace('/','_'), runtime, memory
			))
		if (answer2=='1'):
			os.system('crab resubmit -d forestFowardPDs/crab_{} --maxjobruntime={} --maxmemory={}'.format(
				job.replace('/','_'), runtime, memory
				))
		else:
			print('Not doing anything')

		print('-----'*20)
	
	elif answer == 'n':
		print('Not doing anything')
		print('-----'*20)
	
	else:
		print('Ambiguous mode:', answer, '. Should be [s/f]')
		sys.exit(0)
