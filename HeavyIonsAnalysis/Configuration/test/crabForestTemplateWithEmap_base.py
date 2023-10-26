import os, sys

run_list = [ 	'375202',
		'375245',
		'375252',
		'375256',
		'375259',
		'375300',
		'375317',
		]

for run in run_list:
	crab_script='''
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import getUsername

config = Configuration()

inputList = 'inputs/file_run{run:s}.txt'
jobTag = "run{run:s}_lowerDcut"
username = getUsername()

config.section_("General")
config.General.requestName = jobTag
config.General.workArea = 'forestFowardPDs'
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'forest_miniAOD_run3_ppRECO_DATA_lowerDcut.py'
config.JobType.maxMemoryMB = 5000
config.JobType.maxJobRuntimeMin = 500
config.JobType.scriptExe = 'submitScript.sh'
config.JobType.inputFiles = ['emap_2023_newZDC_v3.txt']
config.JobType.allowUndistributedCMSSW = True

config.section_("Data")
config.Data.userInputFiles = open(inputList).readlines()
config.Data.totalUnits = len(config.Data.userInputFiles)
#config.Data.inputDataset = '/Alternatively/DefineDataset/InsteadOf/InputFileList'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/group/phys_heavyions/' + username + '/run3RapidValidation/' + config.General.requestName
config.Data.publication = False

config.section_("Site")
config.Site.whitelist = ['T2_CH_CERN']
config.Site.storageSite = 'T2_CH_CERN'
'''.format(run=run)
	f = open('crabForestTemplateWithEmap.py', 'w')
	f.write(crab_script)
	os.system('cat crabForestTemplateWithEmap.py')
	os.system('crab submit -c crabForestTemplateWithEmap.py')



	crab_script='''
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import getUsername

config = Configuration()

inputList = 'inputs/file_run{run:s}.txt'
jobTag = "run{run:s}"
username = getUsername()

config.section_("General")
config.General.requestName = jobTag
config.General.workArea = 'forestFowardPDs'
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'forest_miniAOD_run3_ppRECO_DATA.py'
config.JobType.maxMemoryMB = 5000
config.JobType.maxJobRuntimeMin = 500
config.JobType.scriptExe = 'submitScript.sh'
config.JobType.inputFiles = ['emap_2023_newZDC_v3.txt']
config.JobType.allowUndistributedCMSSW = True

config.section_("Data")
config.Data.userInputFiles = open(inputList).readlines()
config.Data.totalUnits = len(config.Data.userInputFiles)
#config.Data.inputDataset = '/Alternatively/DefineDataset/InsteadOf/InputFileList'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/group/phys_heavyions/' + username + '/run3RapidValidation/' + config.General.requestName
config.Data.publication = False

config.section_("Site")
config.Site.whitelist = ['T2_CH_CERN']
config.Site.storageSite = 'T2_CH_CERN'
'''.format(run=run)
	f = open('crabForestTemplateWithEmap.py', 'w')
	f.write(crab_script)
	os.system('cat crabForestTemplateWithEmap.py')
	os.system('crab submit -c crabForestTemplateWithEmap.py')

