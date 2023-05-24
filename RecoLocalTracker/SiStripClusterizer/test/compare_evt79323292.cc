#include "TFile.h"
#include "TDirectoryFile.h"
#include "TTree.h"
#include "TH1D.h"

#include "TCanvas.h"
#include "TStyle.h"
#include "TLegend.h"


template<class T>
void PlotStyle(T* h1)
{
        gStyle->SetTitleFontSize(0.08);

        Float_t x_title_size    = 0.07;
        Float_t y_title_size    = 0.06;

        Float_t x_title_offset  = 0.95;
        Float_t y_title_offset  = 1.25;

        Float_t label_size      = 0.05;
        Float_t label_offset    = 0.013;

        h1->GetYaxis()->SetTitleOffset  (y_title_offset);
        h1->GetYaxis()->SetTitleSize    (y_title_size);
        h1->GetYaxis()->SetLabelOffset  (label_offset);
        h1->GetYaxis()->SetLabelSize    (label_size);
        h1->GetYaxis()->SetNdivisions(508);

        h1->GetXaxis()->SetTitleOffset  (x_title_offset);
        h1->GetXaxis()->CenterTitle();
        h1->GetXaxis()->SetTitleSize    (x_title_size);
        h1->GetXaxis()->SetLabelOffset  (label_offset);
        h1->GetXaxis()->SetLabelSize    (label_size);
        h1->GetXaxis()->SetNdivisions(508);

        h1->SetLineWidth(2);
}


void formatLegend(TLegend* leg, double textsize=0.055)
{
        leg->SetBorderSize(0);
        leg->SetTextFont(42);
        leg->SetTextSize(textsize);
        leg->SetFillStyle(0);
        leg->SetFillColor(0);
        leg->SetLineColor(0);
}

void compare_evt79323292()
{
	TDirectoryFile* _;
	TFile* raw_c   = TFile::Open("output/raw_RAW2DIGI_L1Reco_RECO_run362321_evt79323292_clusterNtuple.root", "read");
	_  = (TDirectoryFile*) raw_c->Get("SiStripClustersDump");
	TTree* t_r_c   = (TTree*) _->Get("clusters");
	
	TFile* rawp_c  = TFile::Open("output/step3_RAW2DIGI_L1Reco_RECO_rawprime_run362321_evt79323292_clusterNtuple.root", "read");
	_  = (TDirectoryFile*) rawp_c->Get("SiStripClustersDump");
	TTree* t_rp_c  = (TTree*) _->Get("clusters");
	
	TFile* rawp_ac = TFile::Open("output/repack_REPACK_approxClusterNtuple.root", "read");
	_  = (TDirectoryFile*) rawp_ac->Get("SiStripApproximatedClustersDump");
	TTree* t_rp_ac = (TTree*) _->Get("ApproxClusters");

	float barycenter_r_c;
	uint16_t  width_r_c;
	int   charge_r_c;
	float barycenter_rp_c;
	uint16_t  width_rp_c;
	int   charge_rp_c;
	uint16_t barycenter_rp_ac;
	uint8_t  width_rp_ac;
	uint8_t  charge_rp_ac;

	t_r_c->SetBranchAddress("barycenter", &barycenter_r_c);
	t_r_c->SetBranchAddress("width", &width_r_c);
	t_r_c->SetBranchAddress("charge", &charge_r_c);

	t_rp_c->SetBranchAddress("barycenter", &barycenter_rp_c);
	t_rp_c->SetBranchAddress("width", &width_rp_c);
	t_rp_c->SetBranchAddress("charge", &charge_rp_c);
	
	t_rp_ac->SetBranchAddress("barycenter", &barycenter_rp_ac);
	t_rp_ac->SetBranchAddress("width", &width_rp_ac);
	t_rp_ac->SetBranchAddress("charge", &charge_rp_ac);
	
	TH1D* h_barycenter_r_c = new TH1D( "h_barycenter_r_c", "RAW; barycenter; count", 40, 0, 950);
	TH1D* h_charge_r_c = new TH1D( "h_charge_r_c", "RAW; charge; count", 40, 0, 700);
	TH1D* h_width_r_c = new TH1D( "h_width_r_c", "RAW; width; count", 40, 0, 20);

	TH1D* h_barycenter_rp_c = new TH1D( "h_barycenter_rp_c", "RAW'; barycenter; count", 40, 0, 950);
	TH1D* h_charge_rp_c = new TH1D( "h_charge_rp_c", "RAW'; charge; count", 40, 0, 700);
	TH1D* h_width_rp_c = new TH1D( "h_width_rp_c", "RAW'; width; count", 40, 0, 20);

	TH1D* h_barycenter_rp_ac = new TH1D( "h_barycenter_rp_ac", "RAW' from approxCluster; barycenter; count", 40, 0, 950);
	TH1D* h_charge_rp_ac = new TH1D( "h_charge_rp_ac", "RAW' from approxCluster; charge; count", 40, 0, 700);
	TH1D* h_width_rp_ac = new TH1D( "h_width_rp_ac", "RAW' from approxCluster; width; count", 40, 0, 20);

	for (int i = 0; i < t_r_c->GetEntries(); ++i)
	{
		t_r_c->GetEntry(i);
		h_barycenter_r_c->Fill(barycenter_r_c);
		h_charge_r_c->Fill(charge_r_c);
		h_width_r_c->Fill(width_r_c);
	}

	for (int i = 0; i < t_rp_c->GetEntries(); ++i)
	{
		t_rp_c->GetEntry(i);
		h_barycenter_rp_c->Fill(barycenter_rp_c);
		h_charge_rp_c->Fill(charge_rp_c);
		h_width_rp_c->Fill(width_rp_c);
	}

	for (int i = 0; i < t_rp_ac->GetEntries(); ++i)
	{
		t_rp_ac->GetEntry(i);
		h_barycenter_rp_ac->Fill(barycenter_rp_ac/10.);
		h_charge_rp_ac->Fill(width_rp_ac*charge_rp_ac);
		h_width_rp_ac->Fill(width_rp_ac);
	}


	TCanvas *c = new TCanvas("c", "c", 700, 600);
	c->SetMargin(0.18, 0.05, 0.20, 0.05);
	gStyle->SetOptTitle(0);
	PlotStyle(h_barycenter_r_c); h_barycenter_r_c->SetStats(0);
	PlotStyle(h_barycenter_rp_c); h_barycenter_rp_c->SetStats(0);
	PlotStyle(h_barycenter_rp_ac); h_barycenter_rp_ac->SetStats(0);
	h_barycenter_r_c->SetLineColor(kAzure+2);
	h_barycenter_rp_c->SetLineColor(kOrange+1);
	h_barycenter_rp_ac->SetLineColorAlpha(kOrange+1, 0.0);
	h_barycenter_rp_ac->SetFillColorAlpha(kOrange+1, 0.2);
	
	h_barycenter_r_c->Draw("hist");
	// h_barycenter_rp_c->Draw("hist same");
	h_barycenter_rp_ac->Draw("hist same");
	h_barycenter_r_c->GetYaxis()->SetRangeUser(0, h_barycenter_r_c->GetMaximum()*1.5);

	TLegend* leg = c->BuildLegend(0.45,0.70,0.93,0.94);
	formatLegend(leg, 0.040);

	c->SaveAs("img/barycenter_evt79323292.pdf");
	system("dropbox_uploader.sh upload img/barycenter_evt79323292.pdf /tmp/");

	PlotStyle(h_charge_r_c); h_charge_r_c->SetStats(0);
	PlotStyle(h_charge_rp_c); h_charge_rp_c->SetStats(0);
	PlotStyle(h_charge_rp_ac); h_charge_rp_ac->SetStats(0);
	h_charge_r_c->SetLineColor(kAzure+2);
	h_charge_rp_c->SetLineColor(kOrange+1);
	h_charge_rp_ac->SetLineColorAlpha(kOrange+1, 0.0);
	h_charge_rp_ac->SetFillColorAlpha(kOrange+1, 0.2);
	
	h_charge_r_c->Draw("hist");
	// h_charge_rp_c->Draw("hist same");
	h_charge_rp_ac->Draw("hist same");
	h_charge_r_c->GetYaxis()->SetRangeUser(0, h_charge_r_c->GetMaximum()*1.2);

	leg = c->BuildLegend(0.45,0.70,0.93,0.94);
	formatLegend(leg, 0.040);

	c->SaveAs("img/charge_evt79323292.pdf");
	system("dropbox_uploader.sh upload img/charge_evt79323292.pdf /tmp/");


	PlotStyle(h_width_r_c); h_width_r_c->SetStats(0);
	PlotStyle(h_width_rp_c); h_width_rp_c->SetStats(0);
	PlotStyle(h_width_rp_ac); h_width_rp_ac->SetStats(0);
	h_width_r_c->SetLineColor(kAzure+2);
	h_width_rp_c->SetLineColor(kOrange+1);
	h_width_rp_ac->SetLineColorAlpha(kOrange+1, 0.0);
	h_width_rp_ac->SetFillColorAlpha(kOrange+1, 0.2);
	
	h_width_r_c->Draw("hist");
	// h_width_rp_c->Draw("hist same");
	h_width_rp_ac->Draw("hist same");
	h_width_r_c->GetYaxis()->SetRangeUser(0, h_width_r_c->GetMaximum()*1.2);

	leg = c->BuildLegend(0.45,0.70,0.93,0.94);
	formatLegend(leg, 0.040);

	c->SaveAs("img/width_evt79323292.pdf");
	system("dropbox_uploader.sh upload img/width_evt79323292.pdf /tmp/");

	delete c;

}


