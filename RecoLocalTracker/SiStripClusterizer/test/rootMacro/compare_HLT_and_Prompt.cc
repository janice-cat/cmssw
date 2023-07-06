#include "TFile.h"
#include "TDirectoryFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TGraphErrors.h"

#include "TCanvas.h"
#include "TStyle.h"
#include "TLegend.h"


template<class T>
void PlotStyle(T* h1)
{
	//fonts
        int defaultFont       = 43;
        float x_title_size    = 17;
        float y_title_size    = 17;

        float x_title_offset  = 1.25;
        float y_title_offset  = 2.1;

        float label_size      = 16;
        float label_offset    = 0.013;

	h1->GetXaxis()->SetLabelFont(defaultFont);
	h1->GetXaxis()->SetTitleFont(defaultFont);
	h1->GetYaxis()->SetLabelFont(defaultFont);
	h1->GetYaxis()->SetTitleFont(defaultFont);

        gStyle->SetTitleFontSize(16);

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


void formatLegend(TLegend* leg, double textsize=17)
{
        leg->SetBorderSize(0);
        leg->SetTextFont(43);
        leg->SetTextSize(textsize);
        leg->SetFillStyle(0);
        leg->SetFillColor(0);
        leg->SetLineColor(0);
}

void compare_HLT_and_Prompt(bool doRatio=true)
{
	TDirectoryFile* _;
	TFile* raw_c   = TFile::Open("../output/raw_RAW2DIGI_L1Reco_RECO_run362321_evt79323292_clusterNtuple.root", "read");
	_  = (TDirectoryFile*) raw_c->Get("SiStripClustersDump");
	TTree* t_r_c   = (TTree*) _->Get("clusters");
	
	TFile* rawp_ac  = TFile::Open("../output/step3_RAW2DIGI_L1Reco_RECO_rawprime_run362321_evt79323292_approxClusterNtuple.root", "read");
	_  = (TDirectoryFile*) rawp_ac->Get("SiStripApproximatedClustersDump");
	TTree* t_rp_ac  = (TTree*) _->Get("ApproxClusters");
	
	TFile* hlt_ac = TFile::Open("../output/outputPhysicsHIAll_HLTGT_approxClusterNtuple.root", "read");
	_  = (TDirectoryFile*) hlt_ac->Get("SiStripApproximatedClustersDump");
	TTree* t_hlt_ac = (TTree*) _->Get("ApproxClusters");

	TFile* prompt_ac = TFile::Open("../output/outputPhysicsHIAll_PromptGT_approxClusterNtuple.root", "read");
	_  = (TDirectoryFile*) prompt_ac->Get("SiStripApproximatedClustersDump");
	TTree* t_prompt_ac = (TTree*) _->Get("ApproxClusters");

	TFile* hlt_sub_ac = TFile::Open("../output/outputPhysicsHIAll_HLTGT_Substitute_approxClusterNtuple.root", "read");
	_  = (TDirectoryFile*) hlt_sub_ac->Get("SiStripApproximatedClustersDump");
	TTree* t_hlt_sub_ac = (TTree*) _->Get("ApproxClusters");

	float barycenter_r_c;
	uint16_t  width_r_c;
	int   charge_r_c;
	uint16_t barycenter_rp_ac;
	uint8_t  width_rp_ac;
	uint8_t  charge_rp_ac;
	uint16_t barycenter_hlt_ac;
	uint8_t  width_hlt_ac;
	uint8_t  charge_hlt_ac;
	uint16_t barycenter_prompt_ac;
	uint8_t  width_prompt_ac;
	uint8_t  charge_prompt_ac;
	uint16_t barycenter_hlt_sub_ac;
	uint8_t  width_hlt_sub_ac;
	uint8_t  charge_hlt_sub_ac;

	t_r_c->SetBranchAddress("barycenter", &barycenter_r_c);
	t_r_c->SetBranchAddress("width", &width_r_c);
	t_r_c->SetBranchAddress("charge", &charge_r_c);

	t_rp_ac->SetBranchAddress("barycenter", &barycenter_rp_ac);
	t_rp_ac->SetBranchAddress("width", &width_rp_ac);
	t_rp_ac->SetBranchAddress("charge", &charge_rp_ac);
	
	t_hlt_ac->SetBranchAddress("barycenter", &barycenter_hlt_ac);
	t_hlt_ac->SetBranchAddress("width", &width_hlt_ac);
	t_hlt_ac->SetBranchAddress("charge", &charge_hlt_ac);

	t_prompt_ac->SetBranchAddress("barycenter", &barycenter_prompt_ac);
	t_prompt_ac->SetBranchAddress("width", &width_prompt_ac);
	t_prompt_ac->SetBranchAddress("charge", &charge_prompt_ac);
	
	t_hlt_sub_ac->SetBranchAddress("barycenter", &barycenter_hlt_sub_ac);
	t_hlt_sub_ac->SetBranchAddress("width", &width_hlt_sub_ac);
	t_hlt_sub_ac->SetBranchAddress("charge", &charge_hlt_sub_ac);

	TH1D* h_barycenter_r_c = new TH1D( "h_barycenter_r_c", "RAW; barycenter; count", 40, 0, 950);
	TH1D* h_charge_r_c = new TH1D( "h_charge_r_c", "RAW; charge; count", 40, 0, 700);
	TH1D* h_width_r_c = new TH1D( "h_width_r_c", "RAW; width; count", 40, 0, 20);

	TH1D* h_barycenter_rp_ac = new TH1D( "h_barycenter_rp_ac", "RAW' from approxCluster; barycenter; count", 40, 0, 950);
	TH1D* h_charge_rp_ac = new TH1D( "h_charge_rp_ac", "RAW' from approxCluster; charge; count", 40, 0, 700);
	TH1D* h_width_rp_ac = new TH1D( "h_width_rp_ac", "RAW' from approxCluster; width; count", 40, 0, 20);

	TH1D* h_barycenter_hlt_ac = new TH1D( "h_barycenter_hlt_ac", "HLT GT; barycenter; count", 40, 0, 950);
	TH1D* h_charge_hlt_ac = new TH1D( "h_charge_hlt_ac", "HLT GT; charge; count", 40, 0, 700);
	TH1D* h_width_hlt_ac = new TH1D( "h_width_hlt_ac", "HLT GT; width; count", 40, 0, 20);

	TH1D* h_barycenter_prompt_ac = new TH1D( "h_barycenter_prompt_ac", "Prompt GT; barycenter; count", 40, 0, 950);
	TH1D* h_charge_prompt_ac = new TH1D( "h_charge_prompt_ac", "Prompt GT; charge; count", 40, 0, 700);
	TH1D* h_width_prompt_ac = new TH1D( "h_width_prompt_ac", "Prompt GT; width; count", 40, 0, 20);

	TH1D* h_barycenter_hlt_sub_ac = new TH1D( "h_barycenter_hlt_sub_ac", "HLT GT + Bad module tag; barycenter; count", 40, 0, 950);
	TH1D* h_charge_hlt_sub_ac = new TH1D( "h_charge_hlt_sub_ac", "HLT GT + Bad module tag; charge; count", 40, 0, 700);
	TH1D* h_width_hlt_sub_ac = new TH1D( "h_width_hlt_sub_ac", "HLT GT + Bad module tag; width; count", 40, 0, 20);

	for (int i = 0; i < t_r_c->GetEntries(); ++i)
	{
		t_r_c->GetEntry(i);
		h_barycenter_r_c->Fill(barycenter_r_c);
		h_charge_r_c->Fill(charge_r_c);
		h_width_r_c->Fill(width_r_c);
	}

	for (int i = 0; i < t_rp_ac->GetEntries(); ++i)
	{
		t_rp_ac->GetEntry(i);
		h_barycenter_rp_ac->Fill(barycenter_rp_ac/10.);
		h_charge_rp_ac->Fill(width_rp_ac*charge_rp_ac);
		h_width_rp_ac->Fill(width_rp_ac);
	}

	for (int i = 0; i < t_hlt_ac->GetEntries(); ++i)
	{
		t_hlt_ac->GetEntry(i);
		h_barycenter_hlt_ac->Fill(barycenter_hlt_ac/10.);
		h_charge_hlt_ac->Fill(width_hlt_ac*charge_hlt_ac);
		h_width_hlt_ac->Fill(width_hlt_ac);
	}

	for (int i = 0; i < t_prompt_ac->GetEntries(); ++i)
	{
		t_prompt_ac->GetEntry(i);
		h_barycenter_prompt_ac->Fill(barycenter_prompt_ac/10.);
		h_charge_prompt_ac->Fill(width_prompt_ac*charge_prompt_ac);
		h_width_prompt_ac->Fill(width_prompt_ac);
	}

	for (int i = 0; i < t_hlt_sub_ac->GetEntries(); ++i)
	{
		t_hlt_sub_ac->GetEntry(i);
		h_barycenter_hlt_sub_ac->Fill(barycenter_hlt_sub_ac/10.);
		h_charge_hlt_sub_ac->Fill(width_hlt_sub_ac*charge_hlt_sub_ac);
		h_width_hlt_sub_ac->Fill(width_hlt_sub_ac);
	}


	TCanvas *c = new TCanvas("c", "c", 700, 900);
	// c->SetMargin(0.18, 0.05, 0.20, 0.05);

	TPad * motherpad = new TPad("motherpad","motherpad",0 ,0.45 ,1 ,1);
	motherpad->SetBottomMargin(0.);
	motherpad->SetLeftMargin(0.185);
	motherpad->Draw();

	TPad * pad1 = new TPad("pad1","pad1", 0, 0.35, 1, 0.45);
	TPad * pad2 = new TPad("pad2","pad2", 0, 0.25, 1, 0.35);
	TPad * pad3 = new TPad("pad3","pad3", 0, 0.10, 1, 0.25);

	pad1->SetBottomMargin(0.); pad1->SetTopMargin(0.); pad1->SetLeftMargin(0.185);
	pad2->SetBottomMargin(0.); pad2->SetTopMargin(0.); pad2->SetLeftMargin(0.185);
	pad3->SetBottomMargin(0.35); pad3->SetTopMargin(0.); pad3->SetLeftMargin(0.185);
	pad1->Draw();  
	pad2->Draw();  
	pad3->Draw();  

	motherpad->cd();
	gStyle->SetOptTitle(0);
	PlotStyle(h_barycenter_r_c); h_barycenter_r_c->SetStats(0);
	PlotStyle(h_barycenter_rp_ac); h_barycenter_rp_ac->SetStats(0);
	PlotStyle(h_barycenter_hlt_ac); h_barycenter_hlt_ac->SetStats(0);
	PlotStyle(h_barycenter_prompt_ac); h_barycenter_prompt_ac->SetStats(0);
	PlotStyle(h_barycenter_hlt_sub_ac); h_barycenter_hlt_sub_ac->SetStats(0);
	h_barycenter_r_c->SetLineColorAlpha(kAzure+2,0.0);
	h_barycenter_r_c->SetFillColorAlpha(kAzure+2,0.2);
	h_barycenter_rp_ac->SetLineColorAlpha(kOrange+1, 0.0);
	h_barycenter_rp_ac->SetFillColorAlpha(kOrange+1, 0.2);
	h_barycenter_hlt_ac->SetLineColor(kRed);
	h_barycenter_prompt_ac->SetLineColor(kBlue);
	h_barycenter_hlt_sub_ac->SetLineColor(kGreen);

	printf("RAW %d\n", (int) h_barycenter_r_c->GetEntries());
	printf("RAW' %d\n", (int) h_barycenter_rp_ac->GetEntries());
	printf("HLT %d\n", (int) h_barycenter_hlt_ac->GetEntries());
	printf("Prompt %d\n", (int) h_barycenter_prompt_ac->GetEntries());
	printf("HLT_substituted %d\n", (int) h_barycenter_hlt_sub_ac->GetEntries());

	h_barycenter_r_c->GetYaxis()->SetRangeUser(0, h_barycenter_r_c->GetMaximum()*1.5);
	h_barycenter_r_c->DrawClone("hist");
	h_barycenter_rp_ac->DrawClone("hist same");
	h_barycenter_hlt_ac->DrawClone("hist same");
	h_barycenter_prompt_ac->DrawClone("hist same");
	h_barycenter_hlt_sub_ac->DrawClone("hist same");

	TLegend* leg = motherpad->BuildLegend(0.55,0.66,0.93,0.86);
	formatLegend(leg);
	leg->SetMargin(0.14);

	vector<TH1D*> numList = { h_barycenter_rp_ac, h_barycenter_hlt_ac, h_barycenter_prompt_ac, h_barycenter_hlt_sub_ac};
	for (TH1D* num: numList)
	{
		num->Divide(h_barycenter_r_c);
		num->GetYaxis()->SetRangeUser(-0.2, 2.9);
		num->GetYaxis()->SetTitle("#splitline{    ratio}{#scale[0.7]{(v.s. RAW)}}");
	}

	TLine line(h_barycenter_r_c->GetXaxis()->GetXmin(), 1,
		   h_barycenter_r_c->GetXaxis()->GetXmax(), 1);
	line.SetLineColorAlpha(kGray, 0.5);
	line.SetLineWidth(2);

	pad1->cd();
	TGraphErrors* h_barycenter_rp_ac_cp = new TGraphErrors(h_barycenter_rp_ac); PlotStyle(h_barycenter_rp_ac_cp);
	h_barycenter_rp_ac_cp->GetYaxis()->SetTitle("#splitline{    ratio}{#scale[0.7]{(v.s. RAW)}}");
	h_barycenter_rp_ac_cp->GetXaxis()->SetRangeUser(
		h_barycenter_rp_ac->GetXaxis()->GetXmin(),
		h_barycenter_rp_ac->GetXaxis()->GetXmax() );
	h_barycenter_rp_ac_cp->DrawClone("a3");
	h_barycenter_hlt_ac->DrawClone("E same");
	line.DrawClone("same");
	
	pad2->cd(); h_barycenter_prompt_ac->DrawClone("E");	line.DrawClone("same");
	pad3->cd(); h_barycenter_hlt_sub_ac->DrawClone("E");	line.DrawClone("same");


	c->SaveAs("../img/barycenter_cf_hlt_prompt.pdf");
	system("dropbox_uploader.sh upload ../img/barycenter_cf_hlt_prompt.pdf /tmp/");

	motherpad->cd();
	gStyle->SetOptTitle(0);
	PlotStyle(h_charge_r_c); h_charge_r_c->SetStats(0);
	PlotStyle(h_charge_rp_ac); h_charge_rp_ac->SetStats(0);
	PlotStyle(h_charge_hlt_ac); h_charge_hlt_ac->SetStats(0);
	PlotStyle(h_charge_prompt_ac); h_charge_prompt_ac->SetStats(0);
	PlotStyle(h_charge_hlt_sub_ac); h_charge_hlt_sub_ac->SetStats(0);
	h_charge_r_c->SetLineColorAlpha(kAzure+2,0.0);
	h_charge_r_c->SetFillColorAlpha(kAzure+2,0.2);
	h_charge_rp_ac->SetLineColorAlpha(kOrange+1, 0.0);
	h_charge_rp_ac->SetFillColorAlpha(kOrange+1, 0.2);
	h_charge_hlt_ac->SetLineColor(kRed);
	h_charge_prompt_ac->SetLineColor(kBlue);
	h_charge_hlt_sub_ac->SetLineColor(kGreen);

	h_charge_r_c->GetYaxis()->SetRangeUser(0, h_charge_r_c->GetMaximum()*1.5);
	h_charge_r_c->DrawClone("hist");
	h_charge_rp_ac->DrawClone("hist same");
	h_charge_hlt_ac->DrawClone("hist same");
	h_charge_prompt_ac->DrawClone("hist same");
	h_charge_hlt_sub_ac->DrawClone("hist same");

	leg = motherpad->BuildLegend(0.55,0.66,0.93,0.86);
	formatLegend(leg);
	leg->SetMargin(0.14);

	numList = { h_charge_rp_ac, h_charge_hlt_ac, h_charge_prompt_ac, h_charge_hlt_sub_ac};
	for (TH1D* num: numList)
	{
		num->Divide(h_charge_r_c);
		num->GetYaxis()->SetRangeUser(-0.2, 2.9);
		num->GetYaxis()->SetTitle("#splitline{    ratio}{#scale[0.7]{(v.s. RAW)}}");
	}

	line = TLine(h_charge_r_c->GetXaxis()->GetXmin(), 1,
		     h_charge_r_c->GetXaxis()->GetXmax(), 1);
	line.SetLineColorAlpha(kGray, 0.5);
	line.SetLineWidth(2);

	pad1->cd();
	TGraphErrors* h_charge_rp_ac_cp = new TGraphErrors(h_charge_rp_ac); PlotStyle(h_charge_rp_ac_cp);
	h_charge_rp_ac_cp->GetYaxis()->SetTitle("#splitline{    ratio}{#scale[0.7]{(v.s. RAW)}}");
	h_charge_rp_ac_cp->GetXaxis()->SetRangeUser(
		h_charge_rp_ac->GetXaxis()->GetXmin(),
		h_charge_rp_ac->GetXaxis()->GetXmax() );
	h_charge_rp_ac_cp->DrawClone("a3");
	h_charge_hlt_ac->DrawClone("E same");
	line.DrawClone("same");
	
	pad2->cd(); h_charge_prompt_ac->DrawClone("E");	line.DrawClone("same");
	pad3->cd(); h_charge_hlt_sub_ac->DrawClone("E");line.DrawClone("same");

	c->SaveAs("../img/charge_cf_hlt_prompt.pdf");
	system("dropbox_uploader.sh upload ../img/charge_cf_hlt_prompt.pdf /tmp/");

	motherpad->cd();
	gStyle->SetOptTitle(0);
	PlotStyle(h_width_r_c); h_width_r_c->SetStats(0);
	PlotStyle(h_width_rp_ac); h_width_rp_ac->SetStats(0);
	PlotStyle(h_width_hlt_ac); h_width_hlt_ac->SetStats(0);
	PlotStyle(h_width_prompt_ac); h_width_prompt_ac->SetStats(0);
	PlotStyle(h_width_hlt_sub_ac); h_width_hlt_sub_ac->SetStats(0);
	h_width_r_c->SetLineColorAlpha(kAzure+2,0.0);
	h_width_r_c->SetFillColorAlpha(kAzure+2,0.2);
	h_width_rp_ac->SetLineColorAlpha(kOrange+1, 0.0);
	h_width_rp_ac->SetFillColorAlpha(kOrange+1, 0.2);
	h_width_hlt_ac->SetLineColor(kRed);
	h_width_prompt_ac->SetLineColor(kBlue);
	h_width_hlt_sub_ac->SetLineColor(kGreen);

	h_width_r_c->GetYaxis()->SetRangeUser(0, h_width_r_c->GetMaximum()*1.5);
	h_width_r_c->DrawClone("hist");
	h_width_rp_ac->DrawClone("hist same");
	h_width_hlt_ac->DrawClone("hist same");
	h_width_prompt_ac->DrawClone("hist same");
	h_width_hlt_sub_ac->DrawClone("hist same");

	leg = motherpad->BuildLegend(0.55,0.66,0.93,0.86);
	formatLegend(leg);
	leg->SetMargin(0.14);

	numList = { h_width_rp_ac, h_width_hlt_ac, h_width_prompt_ac, h_width_hlt_sub_ac};
	for (TH1D* num: numList)
	{
		num->Divide(h_width_r_c);
		num->GetYaxis()->SetRangeUser(-0.2, 2.9);
		num->GetYaxis()->SetTitle("#splitline{    ratio}{#scale[0.7]{(v.s. RAW)}}");
	}

	line = TLine(h_width_r_c->GetXaxis()->GetXmin(), 1,
		     h_width_r_c->GetXaxis()->GetXmax(), 1);
	line.SetLineColorAlpha(kGray, 0.5);
	line.SetLineWidth(2);

	pad1->cd();
	TGraphErrors* h_width_rp_ac_cp = new TGraphErrors(h_width_rp_ac); PlotStyle(h_width_rp_ac_cp);
	h_width_rp_ac_cp->GetYaxis()->SetTitle("#splitline{    ratio}{#scale[0.7]{(v.s. RAW)}}");
	h_width_rp_ac_cp->GetXaxis()->SetRangeUser(
		h_width_rp_ac->GetXaxis()->GetXmin(),
		h_width_rp_ac->GetXaxis()->GetXmax() );
	h_width_rp_ac_cp->DrawClone("a4");
	h_width_hlt_ac->DrawClone("E same");
	line.DrawClone("same");
	
	pad2->cd(); h_width_prompt_ac->DrawClone("E");	line.DrawClone("same");
	pad3->cd(); h_width_hlt_sub_ac->DrawClone("E");line.DrawClone("same");

	c->SaveAs("../img/width_cf_hlt_prompt.pdf");
	system("dropbox_uploader.sh upload ../img/width_cf_hlt_prompt.pdf /tmp/");

	delete c;

}


