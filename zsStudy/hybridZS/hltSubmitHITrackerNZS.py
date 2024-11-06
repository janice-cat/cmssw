from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import getUsername
import glob as glob
USERNAME = getUsername()
RUN    = '387867'
JOBTAG = 'HITrackerNZS_2024Data_'+RUN

config = Configuration()

config.section_("General")
config.General.requestName = JOBTAG
config.General.workArea = 'WorkArea_'+JOBTAG
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
config.Data.userInputFiles = [ 'file:'+filename for filename in glob.glob('/eos/cms/store/t0streamer/Data/PhysicsHITrackerNZS/000/'+RUN[:3]+'/'+RUN[3:]+'/*dat') ]
config.Data.totalUnits = len(config.Data.userInputFiles)
# config.Data.inputDataset = '/HITrackerNZS/HIRun2023A-v1/RAW'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
# config.Data.outLFNDirBasqe = '/store/group/phys_heavyions/'+USERNAME+'/'+JOBTAG+'_hybridZS/hlt/'
config.Data.outLFNDirBase = '/store/user/'+USERNAME+'/'+JOBTAG+'_hybridZS/hlt/'
config.Data.publication = True
config.Data.outputPrimaryDataset = JOBTAG+'_hybridZS'
config.Data.outputDatasetTag = JOBTAG+'_hybridZS_hlt'
# config.Data.publishDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSWriter'

config.section_("Site")
config.Site.whitelist = ['T2_US_Vanderbilt', 'T2_US_Nebraska', 'T2_CH_CERN', 'T2_US_MIT']
config.Site.storageSite = 'T2_US_MIT'

config.section_("Debug")
config.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=True']