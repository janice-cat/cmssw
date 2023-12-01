import os
job_list = [
	'promptReco_run375002_lowerDcut_v2/HIForward0',
	'promptReco_run375002_lowerDcut_v2/HIForward1',
	'promptReco_run375002_lowerDcut_v2/HIForward2',
	'promptReco_run375002_lowerDcut_v2/HIForward3',
	'promptReco_run375002_lowerDcut_v2/HIForward4',
	'promptReco_run375002_lowerDcut_v2/HIForward5',
	'promptReco_run375002_lowerDcut_v2/HIForward6',
	'promptReco_run375002_lowerDcut_v2/HIForward7',
	'promptReco_run375002_lowerDcut_v2/HIForward8',
	'promptReco_run375002_lowerDcut_v2/HIForward9',
	'promptReco_run375002_lowerDcut_v2/HIForward10',
	'promptReco_run375002_lowerDcut_v2/HIForward11',
	'promptReco_run375002_lowerDcut_v2/HIForward12',
	'promptReco_run375002_lowerDcut_v2/HIForward13',
	'promptReco_run375002_lowerDcut_v2/HIForward14',
	'promptReco_run375002_lowerDcut_v2/HIForward15',
	'promptReco_run375002_lowerDcut_v2/HIForward16',
	'promptReco_run375002_lowerDcut_v2/HIForward17',
	'promptReco_run375002_lowerDcut_v2/HIForward18',
	'promptReco_run375002_lowerDcut_v2/HIForward19',
	'promptReco_run375002_lowerDcut_v2',
]

for job in job_list:
	os.system('crab kill -d forestFowardPDs/crab_{}'.format(job.replace('/','_')))
	os.system('rm -rf forestFowardPDs/crab_{}'.format(job.replace('/','_')))
	os.system('rm -rf /eos/cms/store/group/phys_heavyions/yuchenc/run3RapidValidation/{}/'.format(job))
