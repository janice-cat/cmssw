import os
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
	'run374754',
	# 'run374763',
	# 'run374764',
	# 'run374765',
	# 'run374766',
]


for job in jobsList[::-1]:
	os.system('crab status -d {}/crab_{}'.format(job, job))
	oldDirNames = glob.glob('/eos/cms/store/group/phys_heavyions/yuchenc/run3RapidValidation/'+job+'/CRAB_UserFiles/crab_'+job+'/*/*/')
	for oldDirName in oldDirNames:
		os.system('ls {} | grep -c ""'.format(oldDirName))
		newDirName = oldDirName.replace('/CRAB_UserFiles/crab_'+job+'/','/')
		print('This is old dir name:\t\t' , oldDirName)
		print('This will be new dir name:\t' , newDirName)
		answer = input('Want to rename?')
		if (answer):
			os.system('mkdir -p '+'/'.join(newDirName.split('/')[:-2]))
			os.system('eos file rename {} {}'.format(oldDirName, newDirName))
			os.system('ls {} | grep -c ""'.format(newDirName))
		print('-----'*20)

