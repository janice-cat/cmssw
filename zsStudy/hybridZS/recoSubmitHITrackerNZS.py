from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import getUsername
JOBTAG = 'HITrackerNZS_reco'
USERNAME = getUsername()

config = Configuration()

config.section_("General")
config.General.requestName = JOBTAG
config.General.workArea = 'WorkArea_HITrackerNZS'
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_("JobType")
config.JobType.maxMemoryMB = 10000
config.JobType.maxJobRuntimeMin = 330
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'recoPbPbprime2mini_RAW2DIGI_L1Reco_RECO.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.numCores=4

config.section_("Data")
config.Data.inputDataset = '/HITrackerNZS/yuchenc-HITrackerNZS_hybridZS_hlt-570ecf6398dfa9c1e4eef03b8cd09c36/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/'+USERNAME+'/HITrackerNZS_hybridZS/reco/'
config.Data.publication = True
config.Data.outputDatasetTag = 'HITrackerNZS_hybridZS_reco'
# config.Data.publishDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSWriter'

config.section_("Site")
config.Site.whitelist = ['T2_US_Vanderbilt', 'T2_US_Nebraska', 'T2_CH_CERN', 'T2_US_MIT']
config.Site.storageSite = 'T2_US_MIT'

config.section_("Debug")
config.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=True']
