import os, sys
import glob as glob

jobTag 	= 'reReco_run{run:s}_v3/HIForward{PD:d}'
run 	= sys.argv[1]

jobsList= [ jobTag.format(run=run, PD=PD) for PD in range(20) ] 

for job in jobsList:
	os.system('crab status -d forestFowardPDs/crab_{}'.format(job.replace('/','_')))
	oldDirNames = 	glob.glob('/eos/cms/store/group/phys_heavyions/yuchenc/run3RapidValidation/'+job+'/CRAB_UserFiles/crab_'+job+'/*/*/') if '/' not in job else \
			glob.glob('/eos/cms/store/group/phys_heavyions/yuchenc/run3RapidValidation/'+job+'/crab_'+job.replace('/','_')+'/*/*/')
	answer = input('Mode: [s: successful -> rename; f: fail -> resubmit; n: not doing anything]')

	if answer == 's':
		for oldDirName in oldDirNames:
			os.system('ls {} | grep -c ""'.format(oldDirName))
			newDirName = 	oldDirName.replace('/CRAB_UserFiles/crab_'+job+'/','/') if '/' not in job else \
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
