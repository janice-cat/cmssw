import os, sys

run=sys.argv[1]

for PD in range(0,32,1):
	crab_script='''
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import getUsername

config = Configuration()

jobTag = "promptReco_run{run:s}_HIPhysicsRawPrime{PD:d}"
username = getUsername()

config.section_("General")
config.General.requestName = jobTag
config.General.workArea = 'X3872'
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'forest_miniAOD_run3_DATA_wBfinder.py'
config.JobType.maxMemoryMB = 3000
config.JobType.maxJobRuntimeMin = 150
config.JobType.scriptExe = 'submitScript.sh'
config.JobType.inputFiles = ['emap_2023_newZDC_v3.txt','CentralityTable_HFtowers200_DataPbPb_periHYDJETshape_run3v1302x04_offline_374289.db']
config.JobType.allowUndistributedCMSSW = True

config.section_("Data")
config.Data.inputDataset = '/HIPhysicsRawPrime{PD:d}/HIRun2023A-PromptReco-v2/MINIAOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 1
config.Data.runRange = '{run:s}-{run:s}'
config.Data.outLFNDirBase = '/store/group/phys_heavyions/' + username + '/X3872/promptReco_run{run:s}/'
config.Data.publication = False

config.section_("Site")
config.Site.whitelist = ['T2_US_Vanderbilt', 'T2_US_Nebraska']
config.Site.storageSite = 'T2_CH_CERN'
'''.format(run=run, PD=PD)
	f = open('crabForestTemplateWithEmap.py', 'w')
	f.write(crab_script)
	f.close()
	os.system('cat crabForestTemplateWithEmap.py')
	os.system('crab submit -c crabForestTemplateWithEmap.py')
