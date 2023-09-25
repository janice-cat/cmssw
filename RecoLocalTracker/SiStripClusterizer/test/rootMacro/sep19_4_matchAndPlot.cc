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

struct coordinateModulo{
	int part;
	int subpart;
	int layer;
	int ring;
	int nmod;
	double posx, posy, posz;
	double length,  width,  thickness, widthAtHalfLength;
	int detId;
	std::string nome; 
} mod[16588];

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
	string commonLumi(argv[1]);
	bool faster = (argc<=2)? true: atoi(argv[2]);

	/* *******************************
	 * 0.1 Loading tracker module
	 * *******************************/
	TFile* f_trk;
	TTree* tracker;

	struct stat sb;
	if (stat("../tracker.root", &sb)!=0) // file not exists
	{
		cout << "tracker.root not exists" << endl;
		f_trk 	= TFile::Open("../tracker.root", "RECREATE");
		tracker = new TTree("tracker", "tracker");

		int 	detId, part, subpart, layer, ring, nmod;
		float 	x, y, z;
		tracker->Branch("detId", 	&detId, 	"detId/I");
		tracker->Branch("part", 	&part, 		"part/I");
		tracker->Branch("subpart", 	&subpart, 	"subpart/I");
		tracker->Branch("layer", 	&layer, 	"layer/I");
		tracker->Branch("ring", 	&ring, 		"ring/I");
		tracker->Branch("nmod", 	&nmod, 		"nmod/I");
		tracker->Branch("x", 		&x, 		"x/F");
		tracker->Branch("y", 		&y, 		"y/F");
		tracker->Branch("z", 		&z, 		"z/F");

		ifstream* cfile = new ifstream("../tracker.dat",ios::in);
		int cont;
		string ciccio;
		map<int,int>indice_moduli;

		Int_t np = 0;
		//Store data about tracker modules
		while(!cfile->eof()) {
			*cfile  >> cont >> mod[np].part  >> mod[np].subpart 
			    >> mod[np].layer  >> mod[np].ring >> mod[np].nmod
			    >> mod[np].posx >> mod[np].posy >> mod[np].posz
			    >> mod[np].length >> mod[np].width >> mod[np].thickness
			    >> mod[np].widthAtHalfLength >> mod[np].detId; 
			getline(*cfile,ciccio);
			getline(*cfile,mod[np].nome);
			indice_moduli[mod[np].detId]=np;

			detId	= mod[np].detId;
			part	= mod[np].part;
			subpart	= mod[np].subpart;
			layer	= mod[np].layer;
			ring	= mod[np].ring;
			nmod	= mod[np].nmod;
			// meter -> centimeter
			x 	= mod[np].posx*100.;
			y 	= mod[np].posy*100.;
			z 	= mod[np].posz*100.;

			tracker->Fill();
			np++;
		}

		f_trk->Write();
		
		cout << "tracker.dat processed" << endl;
		cout << "tracker.root created" << endl;
		delete cfile;

	} else {
		cout << "read tracker.root" << endl;
		f_trk 	= TFile::Open("../tracker.root", "read");
		tracker = (TTree*) f_trk->Get("tracker");
	}

	/* *******************************
	 * 0.2 Loading clusters & dead strips
	 * *******************************/
	TFile* f1   		= TFile::Open(("../output/lumi_"+commonLumi+"_sep19_2_1_dump_rawprime.root").c_str(), "read");
	TDirectoryFile* _1  	= (TDirectoryFile*) f1->Get("sep19_2_1_dump_rawprime");
	TTree* onlineClusterTree= (TTree*) _1->Get("onlineClusterTree");

	TFile* f2   		= TFile::Open(("../output/lumi_"+commonLumi+"_sep19_2_2_dump_raw.root").c_str(), "read");
	TDirectoryFile* _2  	= (TDirectoryFile*) f2->Get("sep19_2_2_dump_raw");
	TTree* offlineClusterTree= (TTree*) _2->Get("offlineClusterTree");

	// TFile* f3   		= TFile::Open(("../output/lumi_"+commonLumi+"_sep19_3_1_dump_rawprime.root").c_str(), "read");
	// TDirectoryFile* _3  	= (TDirectoryFile*) f3->Get("sep19_3_dump_deadStrips");
	// TTree* onlineDeadStripTree= (TTree*) _3->Get("deadStripTree");

	TFile* f4   		= TFile::Open(("../output/lumi_"+commonLumi+"_sep19_3_2_dump_raw.root").c_str(), "read");
	TDirectoryFile* _4  	= (TDirectoryFile*) f4->Get("sep19_3_dump_deadStrips");
	TTree* offlineDeadStripTree= (TTree*) _4->Get("deadStripTree");

	const static int nMax = 30000;
	////// for rawprime
	unsigned int rp_event;
	int rp_run;
	int rp_lumi;

	// for approxCluster
	uint32_t    rp_detId;
	uint16_t    rp_firstStrip;
	uint16_t    rp_endStrip;
	float       rp_barycenter;
	uint16_t    rp_size;
	int         rp_charge;

	float       rp_hitX[nMax];
	float       rp_hitY[nMax];
	uint16_t    rp_channel[nMax];
	uint16_t    rp_adc[nMax];

	// // for reference of approxCluster
	// uint16_t    rp_ref_firstStrip;
	// uint16_t    rp_ref_endStrip;
	// float       rp_ref_barycenter;
	// uint16_t    rp_ref_size;
	// int         rp_ref_charge;

	// float       rp_ref_hitX[nMax];
	// float       rp_ref_hitY[nMax];
	// uint16_t    rp_ref_channel[nMax];
	// uint16_t    rp_ref_adc[nMax];

	// // for dead strip
  	// unsigned int rp_d_event;
	// int rp_d_run;
	// int rp_d_lumi;
	// int    		rp_d_detId;
	// uint16_t    rp_d_size;
	// uint16_t    rp_d_channel[800];


	////// for raw
	unsigned int r_event;
	int r_run;
	int r_lumi;

	// for stripCluster
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

	// for dead strip
  	unsigned int r_d_event;
	int r_d_run;
	int r_d_lumi;
	int    		r_d_detId;
	uint16_t    r_d_size;
	uint16_t    r_d_channel[800];

	onlineClusterTree->SetBranchAddress("event", &rp_event);
	onlineClusterTree->SetBranchAddress("run",   &rp_run);
	onlineClusterTree->SetBranchAddress("lumi",  &rp_lumi);

	onlineClusterTree->SetBranchAddress("detId", &rp_detId);
	onlineClusterTree->SetBranchAddress("firstStrip", &rp_firstStrip);
	onlineClusterTree->SetBranchAddress("endStrip", &rp_endStrip);
	onlineClusterTree->SetBranchAddress("barycenter", &rp_barycenter);
	onlineClusterTree->SetBranchAddress("size", &rp_size);
	onlineClusterTree->SetBranchAddress("charge", &rp_charge);

	onlineClusterTree->SetBranchAddress("x", rp_hitX);
	onlineClusterTree->SetBranchAddress("y", rp_hitY);
	onlineClusterTree->SetBranchAddress("channel", rp_channel);
	onlineClusterTree->SetBranchAddress("adc", rp_adc);

	// onlineClusterTree->SetBranchAddress("ref_firstStrip", &rp_ref_firstStrip);
	// onlineClusterTree->SetBranchAddress("ref_endStrip", &rp_ref_endStrip);
	// onlineClusterTree->SetBranchAddress("ref_barycenter", &rp_ref_barycenter);
	// onlineClusterTree->SetBranchAddress("ref_size", &rp_ref_size);
	// onlineClusterTree->SetBranchAddress("ref_charge", &rp_ref_charge);

	// onlineClusterTree->SetBranchAddress("ref_x", rp_ref_hitX);
	// onlineClusterTree->SetBranchAddress("ref_y", rp_ref_hitY);
	// onlineClusterTree->SetBranchAddress("ref_channel", rp_ref_channel);
	// onlineClusterTree->SetBranchAddress("ref_adc", rp_ref_adc);

	// onlineDeadStripTree->SetBranchAddress("event", &rp_d_event);
	// onlineDeadStripTree->SetBranchAddress("run",   &rp_d_run);
	// onlineDeadStripTree->SetBranchAddress("lumi",  &rp_d_lumi);
	// onlineDeadStripTree->SetBranchAddress("detId", &rp_d_detId);
	// onlineDeadStripTree->SetBranchAddress("size", &rp_d_size);
	// onlineDeadStripTree->SetBranchAddress("channel", rp_d_channel);

	offlineClusterTree->SetBranchAddress("event", &r_event);
	offlineClusterTree->SetBranchAddress("run",   &r_run);
	offlineClusterTree->SetBranchAddress("lumi",  &r_lumi);

	offlineClusterTree->SetBranchAddress("detId", &r_detId);
	offlineClusterTree->SetBranchAddress("firstStrip", &r_firstStrip);
	offlineClusterTree->SetBranchAddress("endStrip", &r_endStrip);
	offlineClusterTree->SetBranchAddress("barycenter", &r_barycenter);
	offlineClusterTree->SetBranchAddress("size", &r_size);
	offlineClusterTree->SetBranchAddress("charge", &r_charge);

	offlineClusterTree->SetBranchAddress("x", r_hitX);
	offlineClusterTree->SetBranchAddress("y", r_hitY);
	offlineClusterTree->SetBranchAddress("channel", r_channel);
	offlineClusterTree->SetBranchAddress("adc", r_adc);

	offlineDeadStripTree->SetBranchAddress("event", &r_d_event);
	offlineDeadStripTree->SetBranchAddress("run",   &r_d_run);
	offlineDeadStripTree->SetBranchAddress("lumi",  &r_d_lumi);
	offlineDeadStripTree->SetBranchAddress("detId", &r_d_detId);
	offlineDeadStripTree->SetBranchAddress("size", &r_d_size);
	offlineDeadStripTree->SetBranchAddress("channel", r_d_channel);


	map< int, map< int, map<int, cluster> > > r_dict; 	// event, detId, idx
	map< int, map< int, map<int, cluster> > > rp_dict; 	// event, detId, idx
	map< int, map< int, map<int, cluster> > > r_d_dict; 	// event, detId, idx
	// map< int, map< int, map<int, cluster> > > rp_d_dict; 	// event, detId, idx
	map<int, int> 	matched_sc2ac;
	vector<cluster>  	unmatched_scs;
	vector<cluster>  	unmatched_acs;


	TCanvas *canv0 = new TCanvas("canv0", "canv0", 600*3, 600*1);
	gStyle->SetOptTitle(0);
	gErrorIgnoreLevel = kWarning;
	canv0->Divide(3,1,0.001,0.001);

	TH1F * h_width_tot_sc      = new TH1F( "(offline) raw cluster", 
	                                    "; width; yield",  
	                                    50, 0., 50. );
	TH1F * h_charge_tot_sc     = new TH1F( "charge_tot_sc", 
	                                    "; charge; yield",  
	                                    100, 0., 700. );
	TH1F * h_barycenter_tot_sc = new TH1F( "barycenter_tot_sc", 
	                                    "; barycenter; yield",  
	                                    100, 0., 950. );

	TH1F * h_width_tot_ac      = new TH1F( "(online) raw' cluster", 
	                                    "; width; yield",  
	                                    50, 0., 50. );
	TH1F * h_charge_tot_ac     = new TH1F( "charge_tot_ac", 
	                                    "; charge; yield",  
	                                    100, 0., 700. );
	TH1F * h_barycenter_tot_ac = new TH1F( "barycenter_tot_ac", 
	                                    "; barycenter; yield",  
	                                    100, 0., 950. );




	const Int_t r_nEntries = offlineClusterTree->GetEntries();
	for (int sc_idx = 0; sc_idx < r_nEntries; ++sc_idx)
	{
		if(sc_idx%1000000 == 0) std::cout << "Scanning raw clusters: " << sc_idx << "/" << r_nEntries << std::endl;
		offlineClusterTree->GetEntry(sc_idx);

		r_dict[ r_event ][ r_detId ][ sc_idx ] = cluster( sc_idx, r_event, r_run, r_lumi,
												r_detId, r_firstStrip, r_endStrip, r_barycenter,
												r_size, r_charge );
	}


	const Int_t rp_nEntries = onlineClusterTree->GetEntries();
	for (int ac_idx = 0; ac_idx < rp_nEntries; ++ac_idx)
	{
		if(ac_idx%1000000 == 0) std::cout << "Scanning rawprime clusters: " << ac_idx << "/" << rp_nEntries << std::endl;
		onlineClusterTree->GetEntry(ac_idx);

		if (r_dict.find(rp_event)==r_dict.end()) continue;

		rp_dict[ rp_event ][ rp_detId ][ ac_idx ] = cluster( ac_idx, rp_event, rp_run, rp_lumi,
												rp_detId, rp_firstStrip, rp_endStrip, rp_barycenter,
												rp_size, rp_charge );
		h_width_tot_ac->Fill( rp_size );
		h_charge_tot_ac->Fill( rp_charge );
		h_barycenter_tot_ac->Fill( rp_barycenter );
	}

	const Int_t r_d_nEntries = offlineDeadStripTree->GetEntries();
	for (int idx = 0; idx < r_d_nEntries; ++idx)
	{
		if(idx%1000000 == 0) std::cout << "Scanning strip (for offline): " << idx << "/" << r_d_nEntries << std::endl;
		offlineDeadStripTree->GetEntry(idx);

		if (r_dict.find(r_d_event)==r_dict.end()) continue;

		if (r_d_size==0) continue;
		r_d_dict[ r_d_event ][ r_d_detId ][ idx ] = cluster( idx, r_d_event, r_d_run, r_d_lumi,
												r_d_detId, -1, -1, -1,
												r_d_size, -1 );
	}

	// const Int_t rp_d_nEntries = onlineDeadStripTree->GetEntries();
	// for (int idx = 0; idx < rp_d_nEntries; ++idx)
	// {
	// 	if(idx%1000000 == 0) std::cout << "Scanning strip (for online HLT): " << idx << "/" << rp_d_nEntries << std::endl;
	// 	onlineDeadStripTree->GetEntry(idx);

	// 	if (r_dict.find(rp_d_event)==r_dict.end()) continue;

	// 	if (rp_d_size==0) continue;
	// 	rp_d_dict[ rp_d_event ][ rp_d_detId ][ idx ] = cluster( idx, rp_d_event, rp_d_run, rp_d_lumi,
	// 											rp_d_detId, -1, -1, -1,
	// 											rp_d_size, -1 );
	// }

	for (auto it = r_dict.cbegin(); it != r_dict.cend() /* not hoisted */; /* no increment */)
	{
		if (rp_dict.find(it->first)==rp_dict.end())
		{
			printf("[Error] Unexpected, found unmatched event in raw!\n"); // temp, only for 09/21
			r_dict.erase(it++);    // or "it = m.erase(it)" since C++11
		}
		else
		{
			for (auto& _scs_perEvt_perDetId: it->second) 
			{
				for (auto& _sc: _scs_perEvt_perDetId.second) 
				{
					cluster sc(_sc.second);
					h_width_tot_sc->Fill( sc.size );
					h_charge_tot_sc->Fill( sc.charge );
					h_barycenter_tot_sc->Fill( sc.barycenter);
				}
			}
			++it;
		}
	}
	/* *******************************
	 * 1.0 Plotting total cluster distributions
	 * *******************************/
	canv0->cd(1);	
	canv0->GetPad(1)->SetMargin (0.18, 0.05, 0.15, 0.05);
	PlotStyle(h_width_tot_ac); h_width_tot_ac->SetLineColor(kBlue); 	h_width_tot_ac->Draw("");
	PlotStyle(h_width_tot_sc); h_width_tot_sc->SetLineWidth(0); h_width_tot_sc->SetFillColorAlpha(kBlack, 0.7); h_width_tot_sc->SetLineColorAlpha(kBlack, 0.7);  	h_width_tot_sc->Draw("same");
	TLegend* leg0 = canv0->GetPad(1)->BuildLegend(.4, .6, .85, .8);
	formatLegend(leg0);
	canv0->cd(2);	
	canv0->GetPad(2)->SetMargin (0.18, 0.05, 0.15, 0.05);
	PlotStyle(h_charge_tot_ac); h_charge_tot_ac->SetLineColor(kBlue); 	h_charge_tot_ac->Draw("");
	PlotStyle(h_charge_tot_sc); h_charge_tot_sc->SetLineWidth(0); h_charge_tot_sc->SetFillColorAlpha(kBlack, 0.7); h_charge_tot_sc->SetLineColorAlpha(kBlack, 0.7); 	h_charge_tot_sc->Draw("same");
	canv0->cd(3);	
	canv0->GetPad(3)->SetMargin (0.18, 0.05, 0.15, 0.05);
	PlotStyle(h_barycenter_tot_ac); h_barycenter_tot_ac->SetLineColor(kBlue); 	h_barycenter_tot_ac->Draw("");
	PlotStyle(h_barycenter_tot_sc); h_barycenter_tot_sc->SetLineWidth(0); h_barycenter_tot_sc->SetFillColorAlpha(kBlack, 0.7); h_barycenter_tot_sc->SetLineColorAlpha(kBlack, 0.7); 	h_barycenter_tot_sc->Draw("same");
	
	canv0->SaveAs(("../img/lumi_"+commonLumi+"_TotalClusters.pdf").c_str());
	system(("dropbox_uploader.sh upload ../img/lumi_"+commonLumi+"_TotalClusters.pdf /tmp/").c_str());

	delete canv0;
	/*
	cout << "map of raw clusters: " << endl;
	for(auto& _cs_perEvt: r_dict) 
	{
		cout << "event: " << _cs_perEvt.first << endl;
		for (auto& _cs_perEvt_perDetId: _cs_perEvt.second) 
		{
			cout << "detId: " << _cs_perEvt_perDetId.first << endl;
			for (auto& _c: _cs_perEvt_perDetId.second) 
			{
				cout << "idx: " << _c.first << endl;
				_c.second.print();
			}
		}
	}
	cout << "map of rawprime clusters: " << endl;
	for(auto& _cs_perEvt: rp_dict) 
	{
		cout << "event: " << _cs_perEvt.first << endl;
		for (auto& _cs_perEvt_perDetId: _cs_perEvt.second) 
		{
			cout << "detId: " << _cs_perEvt_perDetId.first << endl;
			for (auto& _c: _cs_perEvt_perDetId.second) 
			{
				cout << "idx: " << _c.first << endl;
				_c.second.print();
			}
		}
	}
	*/

	/* *******************************
	 * 2. matching
	 * *******************************/
	for(auto& _acs_perEvt: rp_dict) 
	{
		unsigned int this_event = _acs_perEvt.first;
		for (auto& _acs_perEvt_perDetId: _acs_perEvt.second) 
		{
			int this_detId = _acs_perEvt_perDetId.first;
			for (auto& _ac: _acs_perEvt_perDetId.second) 
			{
				// int this_idx = _ac.first;

				cluster ac(_ac.second);
				float distance(9999.);
				cluster closet_sc; closet_sc.idx = -999;

				for (auto& _sc: r_dict[this_event][this_detId]) 
				{
					cluster sc(_sc.second);
					// cluster matching: exact
					if (ac.size == sc.size &&
						std::max( ac.firstStrip, sc.firstStrip ) <= \
						std::min( ac.endStrip,   sc.endStrip ) ) 
					{
						if (std::abs(ac.barycenter - sc.barycenter) < distance) 
						{
							closet_sc 	= sc;
							distance 	= std::abs(ac.barycenter - sc.barycenter);
						}
					} // end exact matching scan
				} // end strip cluster loop

				if (closet_sc.idx!=-999) 
				{
					if ( matched_sc2ac.count( closet_sc.idx ) == 0 )
					{
						if (ac.firstStrip == closet_sc.firstStrip) {
							closet_sc.matchLevel = 1;
							ac.matchLevel = 1;
						} else {
							closet_sc.matchLevel = 2;
							ac.matchLevel = 2;
						}
						matched_sc2ac[ closet_sc.idx ] = ac.idx;
					} 
					else 
					{
						cluster prev_ac = rp_dict[this_event][this_detId] \
												 [	matched_sc2ac[ closet_sc.idx ] ]; // extract previous ac that matches to sc, get its idx

						if (std::abs( ac.barycenter - closet_sc.barycenter ) < \
							std::abs( prev_ac.barycenter - closet_sc.barycenter ) ) {
							unmatched_acs.push_back(prev_ac);
							matched_sc2ac[ closet_sc.idx ] = ac.idx;
						}
					}
				}
				else 
				{
					unmatched_acs.push_back(ac);
				} 
			}
		}
	}


	for(auto& _scs_perEvt: r_dict) 
	{
		for (auto& _scs_perEvt_perDetId: _scs_perEvt.second) 
		{
			for (auto& _sc: _scs_perEvt_perDetId.second) 
			{
				cluster sc(_sc.second);
				if ( matched_sc2ac.count(sc.idx)==0 ) unmatched_scs.push_back(sc);
			}
		}
	}

	printf("[Summary] matched_sc2ac.size(): %ld, unmatched_acs.size(): %ld, unmatched_scs.size(): %ld\n", 
	                matched_sc2ac.size(), unmatched_acs.size(), unmatched_scs.size());


	/* *******************************
	 * 3.1 plotting matched cluster pairs
	 * *******************************/
	TH2F * h_width      = new TH2F( "width", 
	                                    "; RAW SiStripCluster width; RAW' ApproxCluster width",  
	                                    50, 0., 50.,
	                                    50, 0., 50. );
	TH2F * h_charge     = new TH2F( "charge", 
	                                    "; RAW SiStripCluster charge; RAW' ApproxCluster charge",  
	                                    100, 0., 700.,
	                                    100, 0., 700. );
	TH2F * h_barycenter = new TH2F( "barycenter", 
	                                    "; RAW SiStripCluster barycenter; RAW' ApproxCluster barycenter",  
	                                    100, 0., 950.,
	                                    100, 0., 950. );

	TH1F * h_width_res      = new TH1F( "width_res", 
	                                    "; width (RAW'-RAW)/RAW; yield",
	                                    50, -1., 1.);
	TH1F * h_charge_res     = new TH1F( "chagre_res", 
	                                    "; charge (RAW'-RAW)/RAW; yield",
	                                    50, -1., 1.);
	TH1F * h_barycenter_res = new TH1F( "barycenter_res", 
	                                    "; barycenter RAW'-RAW; yield",
	                                    50, -2., 2.);

	ofstream matched_sc2ac_txt;
	matched_sc2ac_txt.open(Form("log/lumi_%s_matched_sc2ac.txt", commonLumi.c_str()));
	matched_sc2ac_txt << "event detId sc_idx barycenter width charge firstStrip endStrip ac_idx barycenter width charge firstStrip endStrip\n";
	for (auto& idx_pair: matched_sc2ac) 
	{
		// printf("[Debug] approxCluster %p, SiStripCluster %p\n", ac_ptr, sc_ptr);
		offlineClusterTree->GetEntry(idx_pair.first);
		onlineClusterTree->GetEntry( idx_pair.second);


		h_width     ->Fill( r_size, rp_size );
		h_charge    ->Fill( r_charge, rp_charge );
		h_barycenter->Fill( r_barycenter, rp_barycenter ); 

		h_width_res     ->Fill( ( rp_size - r_size )/((float) r_size) );
		h_charge_res    ->Fill( ( rp_charge - r_charge )/((float) r_charge) );
		h_barycenter_res->Fill( rp_barycenter - r_barycenter );

		matched_sc2ac_txt << r_event << " " << r_detId << " " 
						  << idx_pair.first << " " << r_barycenter << " " << r_size << " " << r_charge << " " << r_firstStrip << " " << r_endStrip << " "
						  << idx_pair.second << " " << rp_barycenter << " " << rp_size << " " << rp_charge << " " << rp_firstStrip << " " << rp_endStrip << "\n";
	}
	matched_sc2ac_txt.close();


	TCanvas *canv = new TCanvas("canv", "canv", 600*3, 600*2);


	canv->Divide(3,2,0.001,0.001);

	canv->cd(1); canv->GetPad(1)->SetMargin (0.18, 0.05, 0.15, 0.05);
	PlotStyle(h_width);  	h_width->Draw("COLZ");
	canv->cd(2); canv->GetPad(2)->SetMargin (0.18, 0.05, 0.15, 0.05);
	PlotStyle(h_charge);  	h_charge->Draw("COLZ");
	canv->cd(3); canv->GetPad(3)->SetMargin (0.18, 0.05, 0.15, 0.05);
	PlotStyle(h_barycenter);  	h_barycenter->Draw("COLZ");
	
	canv->cd(4); canv->GetPad(4)->SetLogy(); canv->GetPad(4)->SetMargin (0.18, 0.05, 0.15, 0.05);
	PlotStyle(h_width_res);  		h_width_res->Draw("");
	canv->cd(5); canv->GetPad(5)->SetLogy(); canv->GetPad(5)->SetMargin (0.18, 0.05, 0.15, 0.05);
	PlotStyle(h_charge_res);  		h_charge_res->Draw("");
	canv->cd(6); canv->GetPad(6)->SetLogy(); canv->GetPad(6)->SetMargin (0.18, 0.05, 0.15, 0.05);
	PlotStyle(h_barycenter_res);  	h_barycenter_res->Draw("");


	canv->SaveAs(("../img/lumi_"+commonLumi+"_MatchedClusters.pdf").c_str());
	system(("dropbox_uploader.sh upload ../img/lumi_"+commonLumi+"_MatchedClusters.pdf /tmp/").c_str());

	delete canv;

	ofstream unmatched_scs_txt;
	unmatched_scs_txt.open(Form("log/lumi_%s_unmatched_scs.txt",commonLumi.c_str()));
	unmatched_scs_txt << "event detId sc_idx barycenter width charge firstStrip endStrip\n";
	for(auto& sc: unmatched_scs)
	{
		unmatched_scs_txt << sc.event << " " << sc.detId << " " 
						  << sc.idx << " " << sc.barycenter << " " << sc.size << " " << sc.charge << " "
						  << sc.firstStrip << " " << sc.endStrip << "\n";
	}
	unmatched_scs_txt.close();


	ofstream unmatched_acs_txt;
	unmatched_acs_txt.open(Form("log/lumi_%s_unmatched_acs.txt",commonLumi.c_str()));
	unmatched_acs_txt << "event detId ac_idx barycenter width charge firstStrip endStrip\n";
	for(auto& ac: unmatched_acs)
	{
		unmatched_acs_txt << ac.event << " " << ac.detId << " " 
						  << ac.idx << " " << ac.barycenter << " " << ac.size << " " << ac.charge << " "
						  << ac.firstStrip << " " << ac.endStrip << "\n";
	}
	unmatched_acs_txt.close();

	/* *******************************
	 * 3.2 Plotting unmatched raw SiStripCluster
	 * *******************************/
	for(auto& sc: unmatched_scs)
	{
		offlineClusterTree->GetEntry(sc.idx);
		if (!faster) sc.print();

		// find ac
		if( rp_dict.find( sc.event ) == rp_dict.end() ) continue;
		if( rp_dict[ sc.event ].find( sc.detId ) == rp_dict[ sc.event ].end() ) {
			printf("[Warning:1] no matched ac detId %d in event %d for sc\n", sc.detId, sc.event);
			cout << "sc: " << endl;
			sc.print();
			cout << "offline dead strip (sc) " << endl;
			for (auto& r_ds: r_d_dict[ sc.event ][ sc.detId ]) r_ds.second.print();
			// cout << "online dead strip (sc) " << endl;
			// for (auto& rp_ds: rp_d_dict[ sc.event ][ sc.detId ]) rp_ds.second.print();
			continue;
		}

		TCanvas *canv2 = new TCanvas("canv2", "canv2", 600, 600);
		gStyle->SetOptStat(0);

		TH1F * h_sc = new TH1F( Form("sc%d", sc.idx), Form("RAW (%d-%d); strip; ADC",sc.firstStrip,sc.endStrip), 800,0,800 );

		for(uint16_t i=0; i < r_size; ++i) h_sc->Fill(r_channel[i], r_adc[i]);
		// PlotStyle(h_sc);  	
		h_sc->SetLineWidth(0);
		h_sc->SetFillColorAlpha(kBlack, 0.7);
		h_sc->SetLineColorAlpha(kBlack, 0.7);
		h_sc->GetYaxis()->SetRangeUser(0, h_sc->GetMaximum()*3);
		h_sc->DrawClone("hist");

		/* *******************************
		 * 3.2.1 plot ac on the same detId
		 * *******************************/
		map<int, cluster> ac_map = rp_dict[sc.event][sc.detId];
		if (!faster) printf("found %ld ac in same event and same detId\n", ac_map.size());

		bool foundOverlap(false);
		// bool foundOverlap_ref(false);
		for (auto& ac: ac_map) 
		{

			onlineClusterTree->GetEntry(ac.first);
			if (!faster) ac.second.print();

			if (!foundOverlap) {
				foundOverlap =  std::max( ac.second.firstStrip, sc.firstStrip ) <= \
				                std::min( ac.second.endStrip,   sc.endStrip );
			}

			// if (!foundOverlap_ref) {
			// 	foundOverlap_ref =  std::max( rp_ref_firstStrip, sc.firstStrip ) <= \
			// 	                std::min( rp_ref_endStrip,   sc.endStrip );
			// }

			TH1F * h_ac = new TH1F(Form("ac_%d_%d", sc.idx, ac.first), Form("RAW' (%d-%d); strip; ADC",rp_firstStrip,rp_endStrip), 800,0,800 );
			for(uint16_t i=0; i < rp_size; ++i) h_ac->Fill(rp_channel[i], rp_adc[i]);
			// PlotStyle(h_ac);
			h_ac->SetLineColor(kBlue);

			// TH1F * h_ac_ref = new TH1F(Form("ac_ref_%d_%d", sc.idx, ac.first), Form("RAW' ref (%d); strip; ADC",ac.first), 800,0,800 );
			// for(uint16_t i=0; i < rp_ref_size; ++i) h_ac_ref->Fill(rp_ref_channel[i], rp_ref_adc[i]);
			// // PlotStyle(h_ac_ref);
			// h_ac_ref->SetLineColor(kRed);

			h_ac->DrawClone("hist same");
			// h_ac_ref->DrawClone("hist same");
			
			delete h_ac; 
			// delete h_ac_ref; 
		}
		
		string prefix("");
		if (!foundOverlap)
		{
			printf("[Warning:2] no matched ac in event %d detId %d for sc\n", sc.event, sc.detId);
			prefix = "Warning2_";
			cout << "sc: " << endl;
			sc.print();
			cout << "ac: " << endl;
			for (auto& ac: ac_map) {
				cout << "approx: "; ac.second.print();
				// onlineClusterTree->GetEntry(ac.first);
				// cluster ac_ref = cluster( ac.first, rp_event, rp_run, rp_lumi,
				// 						  rp_detId, rp_ref_firstStrip, rp_ref_endStrip, rp_ref_barycenter,
				// 						  rp_ref_size, rp_ref_charge );
				// cout << "ref    : "; ac_ref.print();
			}
		}

		// if (!foundOverlap_ref)
		// {
		// 	printf("[Warning:3] no matched ac ref in event %d detId %d for sc\n", sc.event, sc.detId);
		// 	prefix = "Warning3_";
		// 	cout << "sc: " << endl;
		// 	sc.print();
		// 	cout << "ac: " << endl;
		// 	for (auto& ac: ac_map) {
		// 		cout << "approx: "; ac.second.print();
		// 		onlineClusterTree->GetEntry(ac.first);
		// 		cluster ac_ref = cluster( ac.first, rp_event, rp_run, rp_lumi,
		// 								  rp_detId, rp_ref_firstStrip, rp_ref_endStrip, rp_ref_barycenter,
		// 								  rp_ref_size, rp_ref_charge );
		// 		cout << "ref    : "; ac_ref.print();
		// 	}
		// }

		/* *******************************
		 * 3.2.2 plot ds of raw on the same detId
		 * *******************************/
		map<int, cluster> r_ds_map = r_d_dict[sc.event][sc.detId]; 
		if (!faster) printf("found %ld online (raw') ds in same event and same detId\n", r_ds_map.size());

		if (r_ds_map.size()==1)
		{
			cluster& r_ds = r_ds_map.begin()->second;
			offlineDeadStripTree->GetEntry(r_ds.idx);

			TH1F * h_r_ds = new TH1F(Form("r_ds_%d_%d", sc.idx, r_ds.idx), Form("RAW dead (%d-%d); strip; ADC",r_ds.firstStrip, r_ds.endStrip), 800,0,800 );
			int r_d_channel_min = 1000;
			int r_d_channel_max = -1;
			for(uint16_t i=0; i < r_d_size; ++i) 
			{
				h_r_ds->Fill(r_d_channel[i], h_sc->GetMaximum());
				if (r_d_channel[i] < r_d_channel_min) r_d_channel_min = r_d_channel[i];
				if (r_d_channel[i] > r_d_channel_max) r_d_channel_max = r_d_channel[i];
			}
			h_r_ds->SetTitle(Form("RAW dead (%d-%d);",r_d_channel_min,r_d_channel_max));
			// PlotStyle(h_r_ds);
			h_r_ds->SetFillColorAlpha(kYellow+1, 0.2);
			h_r_ds->SetLineColorAlpha(kYellow+1, 0.2);
			h_r_ds->DrawClone("hist same");
			delete h_r_ds; 
		} else if (r_ds_map.size()==0) {}
		else {
			printf("[Error] Don't expect\n");
			exit(0);
		}


		/* *******************************
		 * 3.2.3 plot ds of rawprime on the same detId
		 * *******************************/
		// map<int, cluster> rp_ds_map = rp_d_dict[sc.event][sc.detId];
		// // if (!faster) printf("found %ld online (raw') ds in same event and same detId\n", rp_ds_map.size());

		// if (rp_ds_map.size()==1)
		// {
		// 	cluster& rp_ds = rp_ds_map.begin()->second;
		// 	onlineDeadStripTree->GetEntry(rp_ds.idx);

		// 	TH1F * h_rp_ds = new TH1F(Form("rp_ds_%d_%d", sc.idx, rp_ds.idx), Form("RAW' dead (%d); strip; ADC",rp_ds.idx), 800,0,800 );
		// 	int rp_d_channel_min = 1000;
		// 	int rp_d_channel_max = -1;
		// 	for(uint16_t i=0; i < rp_d_size; ++i) 
		// 	{
		// 		h_rp_ds->Fill(rp_d_channel[i], h_sc->GetMaximum());
		// 		if (rp_d_channel[i] < rp_d_channel_min) rp_d_channel_min = rp_d_channel[i];
		// 		if (rp_d_channel[i] > rp_d_channel_max) rp_d_channel_max = rp_d_channel[i];

		// 	}
		// 	h_rp_ds->SetTitle(Form("RAW' dead (%d-%d);",rp_d_channel_min,rp_d_channel_max));
		// 	// PlotStyle(h_rp_ds);
		// 	h_rp_ds->SetFillColorAlpha(kMagenta, 0.3);
		// 	h_rp_ds->SetLineColorAlpha(kMagenta, 0.3);
		// 	h_rp_ds->DrawClone("hist same");
		// 	delete h_rp_ds; 
		// } else if (rp_ds_map.size()==0) {}
		// else {
		// 	printf("[Error] Don't expect\n");
		// 	exit(0);
		// }

		TLegend* leg = canv2->BuildLegend(.5, .6, .85, .8);
		// formatLegend(leg);
		gPad->Modified();
		gPad->Update();
		delete h_sc;

		
		canv2->SaveAs(Form("../img/lumi_%s_%sUnmatchedStripClusters_idx%d.pdf",commonLumi.c_str(),prefix.c_str(),sc.idx));
		if (!faster || prefix=="Warning2_") system(Form("dropbox_uploader.sh upload ../img/lumi_%s_%sUnmatchedStripClusters_idx%d.pdf /tmp/",commonLumi.c_str(),prefix.c_str(),sc.idx));

		delete canv2;
		if (!faster || prefix=="Warning2_") printf("===========================================\n");

	}

	return 0;
}

