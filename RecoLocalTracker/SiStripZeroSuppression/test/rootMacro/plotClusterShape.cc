#include <string>
#include <vector>
#include <map>
#include <fstream>
#include <iostream>
#include <sstream>
#include <sys/stat.h>
#include <functional>
#include <cassert>

#include "TFile.h"
#include "TDirectoryFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TGraphErrors.h"
#include "TStopwatch.h"

#include "TCanvas.h"
#include "TStyle.h"
#include "TLegend.h"
#include "TLatex.h"
#include "TLine.h"
#include "TError.h"


using namespace std;

template<class T>
void PlotStyle(T* h)
{
	//fonts
    int defaultFont       = 43;
    float x_title_size    = 20;
    float y_title_size    = 20;

    float x_title_offset  = 1.5;
    float y_title_offset  = 2.1;

    float label_size      = 20;
    float label_offset    = 0.013;

	h->GetXaxis()->SetLabelFont(defaultFont);
	h->GetXaxis()->SetTitleFont(defaultFont);
	h->GetYaxis()->SetLabelFont(defaultFont);
	h->GetYaxis()->SetTitleFont(defaultFont);

	// gStyle->SetTitleFontSize(16);
	h->SetTitleOffset  (0);


	h->GetYaxis()->SetTitleOffset  (y_title_offset);
	h->GetYaxis()->CenterTitle();
	h->GetYaxis()->SetTitleSize    (x_title_size);
	h->GetYaxis()->SetLabelOffset  (label_offset);
	h->GetYaxis()->SetLabelSize    (label_size);
	h->GetYaxis()->SetNdivisions(508);

	h->GetXaxis()->SetTitleOffset  (x_title_offset);
	h->GetXaxis()->CenterTitle();
	h->GetXaxis()->SetTitleSize    (x_title_size);
	h->GetXaxis()->SetLabelOffset  (label_offset);
	h->GetXaxis()->SetLabelSize    (label_size);
	h->GetXaxis()->SetNdivisions(508);

	h->GetZaxis()->SetTitleOffset  (x_title_offset);
	h->GetZaxis()->CenterTitle();
	h->GetZaxis()->SetTitleSize    (x_title_size);
	h->GetZaxis()->SetLabelOffset  (label_offset);
	h->GetZaxis()->SetLabelSize    (label_size);

	h->SetLineWidth(2);
	// h->SetMinimum(-0.001);

}


void formatLegend(TLegend* leg, double textsize=17)
{
        leg->SetBorderSize(0);
        leg->SetTextFont(43);
        leg->SetTextSize(textsize);
        leg->SetFillStyle(0);
        leg->SetFillColor(0);
        leg->SetLineColor(0);
}

struct cluster{
	int idx;
	unsigned int event;
	int run;
	int lumi;

	// for approxCluster
	uint32_t    detId;
	uint16_t    firstStrip;
	uint16_t    endStrip;
	float       barycenter;
	uint16_t    size;
	int         charge;

	int      	matchLevel; // 1: exact 
							// 2: having overlap

	cluster(): idx(0), event(0), run(0), lumi(0), detId(0), 
		  firstStrip(0), endStrip(0), barycenter(0.), size(0), charge(0),
		  matchLevel(-1) {};
	cluster(int in_idx,
			unsigned int in_event,
			int in_run,
			int in_lumi,
			// for approxCluster
			uint32_t    in_detId,
			uint16_t    in_firstStrip,
			uint16_t    in_endStrip,
			float       in_barycenter,
			uint16_t    in_size,
			int in_charge) :
			idx(in_idx),
			event(in_event),
			run(in_run),
			lumi(in_lumi),
			  // for approxCluster
			detId(in_detId),
			firstStrip(in_firstStrip),
			endStrip(in_endStrip),
			barycenter(in_barycenter),
			size(in_size),
			charge(in_charge),
			matchLevel(-1) {};

	void print()
	{
		cout << "idx: " << idx <<
				", event: " << event <<
				", run: " << run <<
				", lumi: " << lumi <<

				", detId: " << detId <<
				", firstStrip: " << firstStrip <<
				", endStrip: " << endStrip <<
				", barycenter: " << barycenter <<
				", size: " << size <<
				", charge: " << charge << 
				", matchLevel: " << matchLevel << endl;
	}

};



int main(int argc, char const *argv[])
{
	string filename(argv[1]);
	string imgdir(argv[2]);
	bool plotApproximatedCluster = atoi(argv[3]);
	int chooseEventId = atoi(argv[4]);

	TFile* f2   		= TFile::Open(filename.c_str(), "read");
	TDirectoryFile* _2  	= (TDirectoryFile*) f2->Get("sep19_2_1_dump_rawprime");
	TTree* onlineClusterTree= (TTree*) _2->Get("onlineClusterTree");

	const static int nMax = 300000;


	////// for rawprime
	unsigned int r_event;
	int r_run;
	int r_lumi;

	// for converted stripCluster
	uint32_t    r_detId;
	uint16_t    r_firstStrip;
	uint16_t    r_endStrip;
	float       r_barycenter;
	uint16_t    r_size;
	int         r_charge;

	float       r_hitX[nMax];
	float       r_hitY[nMax];
	uint16_t    r_channel[nMax];
	uint16_t    r_adc[nMax];

	onlineClusterTree->SetBranchAddress("event", &r_event);
	onlineClusterTree->SetBranchAddress("run",   &r_run);
	onlineClusterTree->SetBranchAddress("lumi",  &r_lumi);

	onlineClusterTree->SetBranchAddress("detId", &r_detId);
	onlineClusterTree->SetBranchAddress((plotApproximatedCluster)? 	"firstStrip":
									"ref_firstStrip", &r_firstStrip);
	onlineClusterTree->SetBranchAddress((plotApproximatedCluster)? 	"endStrip":
									"ref_endStrip", &r_endStrip);
	onlineClusterTree->SetBranchAddress((plotApproximatedCluster)? 	"barycenter":
									"ref_barycenter", &r_barycenter);
	onlineClusterTree->SetBranchAddress((plotApproximatedCluster)? 	"size":
									"ref_size", &r_size);
	onlineClusterTree->SetBranchAddress((plotApproximatedCluster)? 	"charge":
									"ref_charge", &r_charge);

	onlineClusterTree->SetBranchAddress((plotApproximatedCluster)? 	"x":
									"ref_x", r_hitX);
	onlineClusterTree->SetBranchAddress((plotApproximatedCluster)? 	"y":
									"ref_y", r_hitY);
	onlineClusterTree->SetBranchAddress((plotApproximatedCluster)? 	"channel":
									"ref_channel", r_channel);
	onlineClusterTree->SetBranchAddress((plotApproximatedCluster)? 	"adc":
									"ref_adc", r_adc);


	map< int, map< int, map<int, cluster> > > r_dict; 	// event, detId, idx
	const Int_t r_nEntries = onlineClusterTree->GetEntries();
	for (int sc_idx = 0; sc_idx < r_nEntries; ++sc_idx)
	{
		if(sc_idx%1000000 == 0) std::cout << "Scanning rawprime clusters: " << sc_idx << "/" << r_nEntries << std::endl;
		onlineClusterTree->GetEntry(sc_idx);

		r_dict[ r_event ][ r_detId ][ sc_idx ] = cluster( sc_idx, r_event, r_run, r_lumi,
												r_detId, r_firstStrip, r_endStrip, r_barycenter,
												r_size, r_charge );
	}

	// for(auto& _scs_perEvt: r_dict) 
	// {

	system(("mkdir -p "+imgdir).c_str());

	for (auto& _scs_perEvt_perDetId: r_dict[chooseEventId]) 
	{
		TCanvas *canv2 = new TCanvas("canv2", "canv2", 600, 600);
		gStyle->SetOptStat(0);
		gStyle->SetOptTitle(0);

		int index = 0;
		for (auto& _sc: _scs_perEvt_perDetId.second) 
		{
			onlineClusterTree->GetEntry(_sc.first);

			cluster sc = _sc.second;
			// cluster( sc.idx, r_event, r_run, r_lumi,
			// 			r_detId, r_firstStrip, r_endStrip, r_barycenter,
			// 			r_size, r_charge );
			sc.print();

			TH1F * h_sc = new TH1F( Form("sc%d", sc.idx), Form("%s (strip:%d-%d); strip; ADC",
									   (plotApproximatedCluster)? "RAW\'": "RAW",
									   sc.firstStrip,sc.endStrip), 800,0,800 );

			for(uint16_t i=0; i < r_size; ++i) h_sc->Fill(r_channel[i], r_adc[i]);
			// PlotStyle(h_sc);  	
			h_sc->SetLineWidth(0);
			h_sc->SetFillColorAlpha(index+1, 0.7);
			h_sc->SetLineColorAlpha(index+1, 0.7);
			h_sc->GetYaxis()->SetRangeUser(0, h_sc->GetMaximum()*3);
			h_sc->DrawClone((index==0)? "hist": "hist same");

			index++;
			// TLatex latex;
			// latex.SetTextFont(42);
			// latex.SetTextSize(0.035);
			// latex.DrawLatexNDC(0.13,0.80,
			// 	Form("Event=%d DetId=%d (rootIdx=%d)",r_event,r_detId,sc.idx));

			delete h_sc;
		}

		TLegend* leg = canv2->BuildLegend(.3, .6, .85, .8);
		// formatLegend(leg);
		gPad->Modified();
		gPad->Update();

		canv2->SaveAs(Form("%s/Event%d_DetId%d_%sclustersShape.pdf",
			imgdir.c_str(), chooseEventId, _scs_perEvt_perDetId.first,
			(plotApproximatedCluster)? "approx": "closetSiStrip"));
		// system(Form("dropbox_uploader.sh upload %s/Event%d_DetId%d_%sclustersShape.pdf /tmp/",
		// 	imgdir.c_str(), chooseEventId, _scs_perEvt_perDetId.first,
		// 	(plotApproximatedCluster)? "approx": "closetSiStrip"));

	}

}

