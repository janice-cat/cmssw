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
	'run375013',
	'run375013_lowerDcut',
	'run375055',
	'run375055_lowerDcut',
	'run375145',
	'run375145_lowerDcut',
	'run375164',
	'run375164_lowerDcut',
	'run375195',
	'run375195_lowerDcut',
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

