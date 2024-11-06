from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import getUsername
JOBTAG = 'HITrackerNZS'
USERNAME = getUsername()

config = Configuration()

config.section_("General")
config.General.requestName = JOBTAG
config.General.workArea = 'WorkArea_HITrackerNZS'
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_("JobType")
config.JobType.maxMemoryMB = 10000
config.JobType.maxJobRuntimeMin = 600
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'hlt_cfg.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.numCores=4

config.section_("Data")
config.Data.inputDataset = '/HITrackerNZS/HIRun2023A-v1/RAW'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 20
# config.Data.outLFNDirBase = '/store/group/phys_heavyions/'+USERNAME+'/HITrackerNZS_FEDlikeZS/hlt/'
config.Data.outLFNDirBase = '/store/user/'+USERNAME+'/HITrackerNZS_FEDlikeZS/hlt/'
config.Data.publication = True
# config.Data.outputPrimaryDataset = 'HITrackerNZS_FEDlikeZS_hlt'
config.Data.outputDatasetTag = 'HITrackerNZS_FEDlikeZS_hlt'
# config.Data.publishDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSWriter'

config.section_("Site")
config.Site.whitelist = ['T2_US_Vanderbilt', 'T2_US_Nebraska', 'T2_CH_CERN', 'T2_US_MIT']
config.Site.storageSite = 'T2_US_MIT'

config.section_("Debug")
config.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=True']
