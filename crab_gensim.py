from WMCore.Configuration import Configuration

config = Configuration()

config.section_("General")
config.General.requestName = "HINPbPbSpring23GS_bMin15"
config.General.transferLogs = False

config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = "HIN-HINPbPbSpring23GS-00015_bMin15_cfg.py"
#config.JobType.pyCfgParams=["maxEventsOutput=350"]
config.JobType.maxMemoryMB = 10000    # request high memory machines.
# config.JobType.maxJobRuntimeMin = 2750    # request longer runtime, ~48 hours.
config.JobType.numCores = 4

config.section_("Data")
config.Data.inputDBS = "global" #"phys03"
config.Data.splitting = "EventBased"
config.Data.unitsPerJob = 200 ## Number of *input* event per job !
NJOBS = 10000 ## Total number of jobs !
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.outputPrimaryDataset = 'HINPbPbSpring23GS_bMin15_GENSIM'
config.Data.outLFNDirBase = "/store/group/phys_heavyions/yuchenc/HINPbPbSpring23GS/"
config.Data.publication = False

config.section_("Site")
config.Site.storageSite = "T2_CH_CERN"
