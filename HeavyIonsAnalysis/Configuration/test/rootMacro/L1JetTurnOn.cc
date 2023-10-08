#include <string>
#include <vector>
#include <fstream>
#include <stdio.h>
#include <iostream>

#include <TFile.h>
#include <TChain.h>
#include <TH1D.h>
#include <TEfficiency.h>
#include <TLegend.h>
#include <TCanvas.h>
#include <TLine.h>
#include <TStyle.h>

using namespace std;

std::vector<std::string> getFileList(std::string inFileName) // fileListTxt, root file
{
	std::vector<std::string> fileList;
	
	int type;
	if(inFileName.size() < 5){
		std::cout << "Given inFileName \'" << inFileName << "\' is invalid, exit 1." << std::endl;
		exit(1);
	}
	else if(inFileName.substr(inFileName.size()-4, 4).find(".txt") != std::string::npos)	type = 0;
	else if(inFileName.substr(inFileName.size()-5, 5).find(".root") != std::string::npos)	type = 1;
	else{
		std::cout << "Given inFileName \'" << inFileName << "\' is invalid, exit 1." << std::endl;
		exit(1);
	}

	if(type==0) {
		std::ifstream pathFile(inFileName.c_str());
		std::string paths;
		while(std::getline(pathFile, paths)){
			if(paths.size() == 0) continue;
			fileList.push_back(paths);
		}
		pathFile.close();
	}
	else { // 1		
		fileList.push_back(inFileName);
	}
	return(fileList);
}

void plotTurnOn(string fileListName, int mode,
                string prefix) 
{    
    std::vector<std::string> fileList = getFileList(fileListName);

    TChain *tHLT 	= new TChain("hltanalysis/HltTree");
    TChain *tSkimHLT 	= new TChain("skimanalysis/HltTree");
    TChain *tJet 	= (mode==1) ? new TChain("ak4CaloJetAnalyzer/caloJetTree"): 
                      (mode==2) ? new TChain("ak2PFJetAnalyzer/t"): 
                      (mode==3) ? new TChain("ak3PFJetAnalyzer/t"): 
    				              new TChain("ak4PFJetAnalyzer/t");
    TChain *tL1 	= new TChain("l1object/L1UpgradeFlatTree");
    TChain *tTrack 	= new TChain("ppTracks/trackTree");
    // TChain *tDfinder = new TChain("Dfinder/ntDkpi");  // Added the Dfinder tree

    int fileListLen = (500<fileList.size())? 500: fileList.size();
    for (unsigned int fI=0; fI<fileListLen; fI++) {
    	tHLT->Add(fileList.at(fI).c_str());
    	tSkimHLT->Add(fileList.at(fI).c_str());
    	tJet->Add(fileList.at(fI).c_str());
    	tL1->Add(fileList.at(fI).c_str());
    	tTrack->Add(fileList.at(fI).c_str());
    	// tDfinder->Add(fileList.at(fI).c_str());
    }

    tJet->AddFriend(tHLT);
    tJet->AddFriend(tL1);
    tJet->AddFriend(tSkimHLT);
    tJet->AddFriend(tTrack);
    // tJet->AddFriend(tDfinder);  // Add Dfinder tree as a friend if needed
    TH1D *hDummy = new TH1D("hDummpy", "", 20, 0, 200);
    TH1D *h = new TH1D("h", "", 20, 0, 200);
    TH1D *hTrig0 = new TH1D("hTrig0", "", 20, 0, 200);
    TH1D *hTrig8 = new TH1D("hTrig8", "", 20, 0, 200);
    TH1D *hTrig12 = new TH1D("hTrig12", "", 20, 0, 200);
    TH1D *hTrig16 = new TH1D("hTrig16", "", 20, 0, 200);
    TH1D *hTrig20 = new TH1D("hTrig20", "", 20, 0, 200);
    TH1D *hTrig44 = new TH1D("hTrig44", "", 20, 0, 200); // Histogram for 44 GeV threshold
    TString cut = "pprimaryVertexFilter && L1_MinimumBiasHF1_AND_BptxAND == 0 &&";
    TString target = "Max$(jtpt*(abs(jteta)<1.3))";
    tJet->Draw(target + ">>h", cut+"1", "prof");
    tJet->Draw(target + ">>hTrig0", cut+ "Max$(jetEt*(jetBx == 0))>0", "prof");
    tJet->Draw(target + ">>hTrig8", cut + " Max$(jetEt*(jetBx == 0))>8", "prof");
    tJet->Draw(target + ">>hTrig12", cut + " Max$(jetEt*(jetBx == 0))>12", "prof");
    tJet->Draw(target + ">>hTrig16", cut + " Max$(jetEt*(jetBx == 0))>16", "prof");
    tJet->Draw(target + ">>hTrig20", cut + " Max$(jetEt*(jetBx == 0))>20", "prof");
    tJet->Draw(target + ">>hTrig44", cut + " Max$(jetEt*(jetBx == 0))>44", "prof"); // Draw with 44 GeV threshold
    TEfficiency *efficiency0 = new TEfficiency(*hTrig0, *h);
    TEfficiency *efficiency8 = new TEfficiency(*hTrig8, *h);
    TEfficiency *efficiency12 = new TEfficiency(*hTrig12, *h);
    TEfficiency *efficiency16 = new TEfficiency(*hTrig16, *h);
    TEfficiency *efficiency20 = new TEfficiency(*hTrig20, *h);
    TEfficiency *efficiency44 = new TEfficiency(*hTrig44, *h); // Efficiency for 44 GeV threshold
    TCanvas *c = new TCanvas("c", "Efficiencies", 600, 600);
    gStyle->SetOptStat(0);
    efficiency0->SetLineColor(kCyan);
    efficiency0->SetMarkerColor(kCyan);
    hDummy->SetXTitle((mode==1)? "Max PU-sub Calo Jet E_{T} (GeV)":
                      (mode==2)? "Max PF Jet_{R=.2} E_{T} (GeV)":
                      (mode==3)? "Max PF Jet_{R=.3} E_{T} (GeV)":
    				             "Max PF Jet_{R=.4} E_{T} (GeV)");
    hDummy->SetYTitle("Efficiency");
    hDummy->Draw();
    TLine *l = new TLine(0,1,200,1);
    l->SetLineStyle(2);
    l->Draw();
    efficiency0->Draw("same");
    efficiency8->SetLineColor(kRed);
    efficiency8->SetMarkerColor(kRed);
    efficiency8->Draw("same");
    efficiency12->SetLineColor(kGreen+2);
    efficiency12->SetMarkerColor(kGreen+2);
    efficiency12->Draw("same");
    efficiency16->SetLineColor(kMagenta);
    efficiency16->SetMarkerColor(kMagenta);
    efficiency16->Draw("same");
    efficiency20->SetLineColor(kBlack);
    efficiency20->SetMarkerColor(kBlack);
    efficiency20->Draw("same");
    efficiency44->SetLineColor(kYellow+2); // Line color for 44 GeV threshold
    efficiency44->SetMarkerColor(kYellow+2); // Marker color for 44 GeV threshold
    efficiency44->Draw("same"); // Draw efficiency for 44 GeV threshold
    TLegend *leg = new TLegend(0.6, 0.2, 0.85, 0.6); // Adjusted legend coordinates
    leg->SetFillStyle(0);
    leg->SetBorderSize(0);
    leg->AddEntry(efficiency0, "L1 JetEt > 0", "l");
    leg->AddEntry(efficiency8, "L1 JetEt > 8", "l");
    leg->AddEntry(efficiency12, "L1 JetEt > 12", "l");
    leg->AddEntry(efficiency16, "L1 JetEt > 16", "l");
    leg->AddEntry(efficiency20, "L1 JetEt > 20", "l");
    leg->AddEntry(efficiency44, "L1 JetEt > 44", "l"); // Legend entry for 44 GeV threshold
    leg->Draw();
    string plotName((mode==1)?  "img/"+prefix+"_ak4CaloJetAnalyzer_PbPb_JetTurnOnEfficiencies.png":
                    (mode==2)?  "img/"+prefix+"_ak2PFJetAnalyzer_PbPb_JetTurnOnEfficiencies.png":
                    (mode==3)?  "img/"+prefix+"_ak3PFJetAnalyzer_PbPb_JetTurnOnEfficiencies.png":
                                "img/"+prefix+"_ak4PFJetAnalyzer_PbPb_JetTurnOnEfficiencies.png" );
    c->SaveAs(plotName.c_str());
    system(("dropbox_uploader.sh upload "+plotName+" /tmp/").c_str());

    delete tHLT;
    delete tSkimHLT ;
    delete tJet;
    delete tL1;
    delete tTrack;
    // delete tDfinder;
    delete hDummy;
    delete h;
    delete hTrig0;
    delete hTrig8;
    delete hTrig12;
    delete hTrig16;
    delete hTrig20;
    delete hTrig44;
    delete efficiency0;
    delete efficiency8;
    delete efficiency12;
    delete efficiency16;
    delete efficiency20;
    delete efficiency44;
    delete l;
    delete leg;
    delete c;

}


void plotPTSpectra(string fileListName, int mode,
                   string prefix)
{
    std::vector<std::string> fileList = getFileList(fileListName);


    TChain *tHLT 	= new TChain("hltanalysis/HltTree");
    TChain *tSkimHLT 	= new TChain("skimanalysis/HltTree");
    TChain *tJet    = (mode==1) ? new TChain("ak4CaloJetAnalyzer/caloJetTree"): 
                      (mode==2) ? new TChain("ak2PFJetAnalyzer/t"): 
                      (mode==3) ? new TChain("ak3PFJetAnalyzer/t"): 
                                  new TChain("ak4PFJetAnalyzer/t");
    TChain *tL1 	= new TChain("l1object/L1UpgradeFlatTree");
    TChain *tTrack 	= new TChain("ppTracks/trackTree");
    // TChain *tDfinder = new TChain("Dfinder/ntDkpi");  // Added the Dfinder tree

    int fileListLen = (500<fileList.size())? 500: fileList.size();
    for (unsigned int fI=0; fI<fileListLen; fI++) {
    	tHLT->Add(fileList.at(fI).c_str());
    	tSkimHLT->Add(fileList.at(fI).c_str());
    	tJet->Add(fileList.at(fI).c_str());
    	tL1->Add(fileList.at(fI).c_str());
    	tTrack->Add(fileList.at(fI).c_str());
    	// tDfinder->Add(fileList.at(fI).c_str());
    }

    tJet->AddFriend(tL1);
    tJet->AddFriend(tSkimHLT);
    tJet->AddFriend(tHLT);
    
    TH1D *jtpt_eta1 = new TH1D("jtpt_eta1", ";Jet p_{T}; Yield", 50, 0, 200);
    TH1D *jtpt_eta1p5 = new TH1D("jtpt_eta1p5", ";Jet p_{T}; Yield", 50, 0, 200);
    TH1D *jtpt_eta2 = new TH1D("jtpt_eta2", ";Jet p_{T}; Yield", 50, 0, 200);
    TH1D *jtpt_eta2p5 = new TH1D("jtpt_eta2p5", ";Jet p_{T}; Yield", 50, 0, 200);

    TCanvas *c = new TCanvas("c", "c_pt", 600, 600);
    tJet->Draw("jtpt>>jtpt_eta2p5","(pprimaryVertexFilter && L1_MinimumBiasHF1_AND_BptxAND == 0)*(abs(jteta)<2.5)");
    tJet->Draw("jtpt>>jtpt_eta2","(pprimaryVertexFilter && L1_MinimumBiasHF1_AND_BptxAND == 0)*(abs(jteta)<2)","same");
    tJet->Draw("jtpt>>jtpt_eta1p5","(pprimaryVertexFilter && L1_MinimumBiasHF1_AND_BptxAND == 0)*(abs(jteta)<1.5)","same");
    tJet->Draw("jtpt>>jtpt_eta1","(pprimaryVertexFilter && L1_MinimumBiasHF1_AND_BptxAND == 0)*(abs(jteta)<1)","same");

    jtpt_eta1->SetLineColor(kBlue+3);
    jtpt_eta1p5->SetLineColor(kBlue);
    jtpt_eta2->SetLineColor(kRed);
    jtpt_eta2p5->SetLineColor(kRed+2);

    TLegend *leg = new TLegend(0.6, 0.2, 0.85, 0.6); // Adjusted legend coordinates
    leg->SetFillStyle(0);
    leg->SetBorderSize(0);
    leg->AddEntry(jtpt_eta1, "|#eta| < 1", "l");
    leg->AddEntry(jtpt_eta1p5, "|#eta| < 1.5", "l");
    leg->AddEntry(jtpt_eta2, "|#eta| < 2", "l");
    leg->AddEntry(jtpt_eta2p5, "|#eta| < 2.5", "l");
    leg->Draw();
    string plotName((mode==1)? 	"img/"+prefix+"_ak4CaloJetAnalyzer_ptSpectra.png":
                    (mode==2)?  "img/"+prefix+"_ak2PFJetAnalyzer_ptSpectra.png":
                    (mode==3)?  "img/"+prefix+"_ak3PFJetAnalyzer_ptSpectra.png":
				                "img/"+prefix+"_ak4PFJetAnalyzer_ptSpectra.png" );
    c->SaveAs(plotName.c_str());
    system(("dropbox_uploader.sh upload "+plotName+" /tmp/").c_str());

    delete tHLT;
    delete tSkimHLT ;
    delete tJet;
    delete tL1;
    delete tTrack;
    // delete tDfinder;
    delete jtpt_eta1;
    delete jtpt_eta1p5;
    delete jtpt_eta2;
    delete jtpt_eta2p5;
    delete leg;
    delete c;

}

int main(int argc, char const *argv[])
{
    string inFileName(argv[1]);
    string prefix(inFileName);      prefix.replace(prefix.find(".txt"),4,"");
	plotTurnOn(inFileName, 1, prefix);
    plotTurnOn(inFileName, 2, prefix);
    plotTurnOn(inFileName, 3, prefix);
	plotTurnOn(inFileName, 4, prefix);
	plotPTSpectra(inFileName, 1, prefix);
    plotPTSpectra(inFileName, 2, prefix);
    plotPTSpectra(inFileName, 3, prefix);
	plotPTSpectra(inFileName, 4, prefix);
	return 0;
}