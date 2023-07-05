#! /usr/bin/env python3
import numpy as np
# from root_pandas import read_root
import pandas as pd
import argparse
from glob import glob

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import os, sys
import uproot
sys.path.append('/afs/cern.ch/user/y/yuchenc/DataCompression/python/utils/')
import DfNtupleMgr as dnm
import PlotUtils as pu

from  itertools import chain


def main():
	parser = argparse.ArgumentParser(prog='nClusters.py')
	parser.add_argument('f1', 	help='***.root (RAW root path)')
	parser.add_argument('f2', 	help='***.root (RAWPrime root path)')
	args = parser.parse_args()

	f1 = args.f1
	f2 = args.f2

	branchlist 	= [ 'event', 'detId', 'barycenter', 'width', 'charge' ]

	df1, df2 = 0, 0
	for key in uproot.open(f1).keys():
		if ('SiStripClustersDump/clusters' in key):
			df1 = uproot.open(f1)[key].arrays(branchlist, library='pd')
			break
	for key in uproot.open(f2).keys():
		if ('clusterNtuple.root' in f2):
			if ('SiStripClustersDump/clusters' in key):
				df2 = uproot.open(f2)[key].arrays(branchlist, library='pd')
				break
		if ('approxClusterNtuple.root' in f2):
			if ('SiStripApproximatedClustersDump/ApproxClusters' in key):
				df2 = uproot.open(f2)[key].arrays(branchlist, library='pd')
				break

	##### nClusters
	df1_common = df1
	df2_common = df2
	df1_common = df1_common[ df1_common.event.isin(df2_common.event) ]
	df2_common = df2_common[ df2_common.event.isin(df1_common.event) ]
	df1_common = df1_common.value_counts('event',sort=False,dropna=False).reset_index(name='count')
	df2_common = df2_common.value_counts('event',sort=False,dropna=False).reset_index(name='count')
	print(df1_common)
	print(df2_common)

	plt.figure(figsize=(8,8))
	grid_space = plt.GridSpec(3,1, wspace=0.4, hspace=0.)
	ax = plt.subplot(grid_space[:2])
	ax.xaxis.set_ticklabels([])
	plt.grid(1)

	plt.errorbar(df1_common['event'], df1_common['count'],
					yerr=np.sqrt(df1_common['count']),
					marker='.', ls='none', 
					drawstyle='steps-mid', fmt='o',
					ecolor='lightgray', elinewidth=3, capsize=0)
	plt.errorbar(df2_common['event'], df2_common['count'],
					yerr=np.sqrt(df2_common['count']),
					marker='.', ls='none', 
					drawstyle='steps-mid', fmt='o',
					ecolor='lightgray', elinewidth=3, capsize=0)
	plt.ylabel('#(clusters)')
	plt.legend(['Raw','Raw\''],frameon=False)
	# plt.yscale('log')


	ax2 = plt.subplot(grid_space[2])
	plt.errorbar(df2_common['event'], df2_common['count']/df1_common['count'],
					yerr=df2_common['count']/df1_common['count'] * np.sqrt( (np.sqrt(df1_common['count'])/df1_common['count'])**2 +\
												(np.sqrt(df2_common['count'])/df2_common['count'])**2 ),
					marker='.', ls='none', 
					drawstyle='steps-mid', fmt='o', color=(1.0, 0.4980392156862745, 0.054901960784313725),
					ecolor='lightgray', elinewidth=3, capsize=0)
	plt.ylabel('ratio (Raw\'/Raw)')
	plt.xlabel('event index')
	plt.ylim([0.95, 1.15])
	# plt.yscale('log')
	plt.grid(1)
	plt.savefig('../img/nClusters.pdf')
	pu.Send2Dropbox('../img/nClusters.pdf')

	##### diff nClusters v.s. detId

	df1_common = df1
	df2_common = df2
	df1_common = df1_common[ df1_common.event.isin(df2_common.event) ]
	df2_common = df2_common[ df2_common.event.isin(df1_common.event) ]
	print(df1_common)
	print(df2_common)
	df1_common[ df1_common.event==160683550 ].sort_values(by=['detId','barycenter','width','charge']).to_csv('out_raw_160683550.txt',index=False)
	df2_common[ df2_common.event==160683550 ].sort_values(by=['detId','barycenter','width','charge']).to_csv('out_rawprime_160683550.txt',index=False)

	# df1_common = df1_common[ df1_common.event==160523183 ]
	# df2_common = df2_common[ df2_common.event==160523183 ]

	nbins = 100
	plt.figure(figsize=(8,8))
	plt.suptitle(r'Events $\in [{}, {}]$'.format(np.min(df1_common.event),
						     np.max(df1_common.event)))
	grid_space = plt.GridSpec(7,2, wspace=0.30, hspace=0)

	for i, [rangeCongig, title, grid_space_mo_idx, grid_space_dau_idx] in \
	   enumerate([[ (369.1e6, 369.2e6), r'detId $< 3.8 \times 10^8$', grid_space[:2,0], grid_space[2,0] ],
		      [ (402.65e6, 402.7e6), r'$3.9 \times 10^8 <$ detId $< 4.1 \times 10^8$', grid_space[:2,1], grid_space[2,1] ],
		      [ (436.2e6, 436.4e6), r'$4.3 \times 10^8 <$ detId $< 4.5 \times 10^8$', grid_space[4:6,0], grid_space[6,0] ],
		      [ (470.0e6, 470.5e6), r'detId $> 4.6 \times 10^8$', grid_space[4:6,1], grid_space[6,1] ]]):

		ax = plt.subplot(grid_space_mo_idx)
		ax.xaxis.set_ticklabels([])

		plt.grid(1)
		plt.title(title)

		y1, bin_edges = np.histogram(df1_common.detId, bins=nbins, range=rangeCongig)
		bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
		yerr1 	= np.sqrt(y1)

		y2, bin_edges = np.histogram(df2_common.detId, bins=nbins, range=rangeCongig)
		bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
		yerr2 	= np.sqrt(y2)

		plt.errorbar(bin_centers[y1!=0], y1[y1!=0],
					yerr=yerr1[y1!=0],
					marker='.', ls='none', 
					drawstyle='steps-mid', fmt='o',
					ecolor='lightgray', elinewidth=3, capsize=0)
		plt.errorbar(bin_centers[y2!=0], y2[y2!=0],
					yerr=yerr2[y2!=0],
					marker='.', ls='none', 
					drawstyle='steps-mid', fmt='o',
					ecolor='lightgray', elinewidth=3, capsize=0)
		plt.xlim(rangeCongig)
		plt.ylabel('count')
		if (i==0): plt.legend(['Raw','Raw\''],frameon=False)

		ax = plt.subplot(grid_space_dau_idx)
		plt.grid(1)
		plt.errorbar(bin_centers[np.logical_or(y1!=0, y2!=0)], (y2-y1)[np.logical_or(y1!=0, y2!=0)],
					yerr=np.sqrt(yerr1*yerr1 + yerr2*yerr2)[np.logical_or(y1!=0, y2!=0)],
					marker='.', ls='none', 
					drawstyle='steps-mid', fmt='o', color=(1.0, 0.4980392156862745, 0.054901960784313725),
					ecolor='lightgray', elinewidth=3, capsize=0)
		plt.xlim(rangeCongig)
		plt.ylabel('RAW\'-RAW')
		plt.xlabel('detId')

	plt.savefig('../img/diff_detId_{}_{}.pdf'.format(np.min(df1_common.event), np.max(df1_common.event)))
	pu.Send2Dropbox('../img/diff_detId_{}_{}.pdf'.format(np.min(df1_common.event), np.max(df1_common.event)))

if __name__ == '__main__':
	main()
