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

void plotTurnOn(string fileListName, string prefix) 
{    
    std::vector<std::string> fileList = getFileList(fileListName);

    TChain *tHLT 	= new TChain("hltanalysis/HltTree");
    TChain *tSkimHLT 	= new TChain("skimanalysis/HltTree");
    TChain *tL1 	= new TChain("l1object/L1UpgradeFlatTree");
    TChain *tTrack 	= new TChain("ppTracks/trackTree");
    TChain *tDfinder = new TChain("Dfinder/ntDkpi");  // Added the Dfinder tree

    int fileListLen = (500<fileList.size())? 500: fileList.size();
    for (unsigned int fI=0; fI<fileListLen; fI++) {
    	tHLT->Add(fileList.at(fI).c_str());
    	tSkimHLT->Add(fileList.at(fI).c_str());
    	tL1->Add(fileList.at(fI).c_str());
    	tTrack->Add(fileList.at(fI).c_str());
    	tDfinder->Add(fileList.at(fI).c_str());
    }

    tDfinder->AddFriend(tHLT);
    tDfinder->AddFriend(tL1);
    tDfinder->AddFriend(tSkimHLT);
    tDfinder->AddFriend(tTrack);
    TH1D *hDummy = new TH1D("hDummpy", "", 20, 0, 20);
    TH1D *h = new TH1D("h", "", 20, 0, 20);
    TH1D *hTrig0 = new TH1D("hTrig0", "", 20, 0, 20);
    TH1D *hTrig8 = new TH1D("hTrig8", "", 20, 0, 20);
    TH1D *hTrig12 = new TH1D("hTrig12", "", 20, 0, 20);
    TH1D *hTrig16 = new TH1D("hTrig16", "", 20, 0, 20);
    TH1D *hTrig20 = new TH1D("hTrig20", "", 20, 0, 20);
    TH1D *hTrig44 = new TH1D("hTrig44", "", 20, 0, 20); // Histogram for 44 GeV threshold
    TString cut = "pprimaryVertexFilter && L1_MinimumBiasHF1_AND_BptxAND == 0 && "
                  "Dalpha<0.15 && DsvpvDistance/DsvpvDisErr>4. && Dchi2cl>0.05 && ";
    TString target = "Max$(Dpt*(abs(Deta)<2.0))";
    tDfinder->Draw(target + ">>h", cut+"1", "prof");
    tDfinder->Draw(target + ">>hTrig0", cut+ "Max$(jetEt*(jetBx == 0))>0", "prof");
    tDfinder->Draw(target + ">>hTrig8", cut + " Max$(jetEt*(jetBx == 0))>8", "prof");
    tDfinder->Draw(target + ">>hTrig12", cut + " Max$(jetEt*(jetBx == 0))>12", "prof");
    tDfinder->Draw(target + ">>hTrig16", cut + " Max$(jetEt*(jetBx == 0))>16", "prof");
    tDfinder->Draw(target + ">>hTrig20", cut + " Max$(jetEt*(jetBx == 0))>20", "prof");
    tDfinder->Draw(target + ">>hTrig44", cut + " Max$(jetEt*(jetBx == 0))>44", "prof"); // Draw with 44 GeV threshold
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
    hDummy->SetXTitle("Offline D^{0} p_{T} (GeV)");
    hDummy->SetYTitle("D^{0} efficiency");
    hDummy->Draw();
    TLine *l = new TLine(0,1,20,1);
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
    string plotName("img/"+prefix+"_PbPb_D0TurnOnEfficiencies.png" );
    c->SaveAs(plotName.c_str());
    system(("dropbox_uploader.sh upload "+plotName+" /tmp/").c_str());

    delete tHLT;
    delete tSkimHLT ;
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

int main(int argc, char const *argv[])
{
    string inFileName(argv[1]);
    string prefix(inFileName);      prefix.replace(prefix.find(".txt"),4,"");
	plotTurnOn(inFileName, prefix);
	return 0;
}