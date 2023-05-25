import uproot
import pandas as pd

import sys
sys.path.append('/afs/cern.ch/user/y/yuchenc/DataCompression/python/utils/') 
import DfNtupleMgr as dnm 
import PlotUtils as pu

file_r_c = uproot.open('../output/raw_RAW2DIGI_L1Reco_RECO_run362321_evt79323292_clusterNtuple.root')
tree_r_c = file_r_c['SiStripClustersDump/clusters']
df_r_c   = tree_r_c.arrays(library="pd")

file_rp_c = uproot.open('../output/step3_RAW2DIGI_L1Reco_RECO_rawprime_run362321_evt79323292_clusterNtuple.root')
tree_rp_c = file_rp_c['SiStripClustersDump/clusters']
df_rp_c   = tree_rp_c.arrays(library="pd")

detId_in_r_c_and_rp_c 	= df_r_c[ df_r_c.detId.isin(df_rp_c.detId) ]
detId_in_r_c_notIn_rp_c = df_r_c[ ~(df_r_c.detId.isin(df_rp_c.detId)) ]
detId_in_rp_c_and_r_c 	= df_rp_c[ df_rp_c.detId.isin(df_r_c.detId) ]
detId_in_rp_c_notIn_r_c = df_rp_c[ ~(df_rp_c.detId.isin(df_r_c.detId)) ]

dnm.plotVarsState( [['common (RAW)', detId_in_r_c_and_rp_c],
		    ['common (RAW\')', detId_in_rp_c_and_r_c],
		    ['only in RAW', detId_in_r_c_notIn_rp_c],
		    ['only in RAW\'', detId_in_rp_c_notIn_r_c]],
		   [[ 'detId', 'detId',  (360e6, 480e6)],
		    [ 'barycenter', 'barycenter',  (0, 950)],
		    [ 'charge', 'charge',  (0, 700)]],
		    '../img/checkDetId.pdf',
		    col_arr=[(0.17254901960784313, 0.6274509803921569, 0.17254901960784313), 
		    	     (0.17254901960784313, 0.6274509803921569, 0.17254901960784313, 0.5), 
		    	     (0.12156862745098039, 0.4666666666666667, 0.7058823529411765),
		    	     (1.0, 0.4980392156862745, 0.054901960784313725)])

pu.Send2Dropbox('../img/checkDetId.pdf')