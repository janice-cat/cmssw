// system includes
#include <memory>
#include <iostream>

// user include files
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/Utils/interface/TFileDirectory.h"
#include "DataFormats/Common/interface/DetSet.h"
#include "DataFormats/Common/interface/DetSetVector.h"
#include "DataFormats/Common/interface/DetSetVectorNew.h"
#include "DataFormats/SiStripCluster/interface/SiStripCluster.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

//ROOT inclusion
#include "TROOT.h"
#include "TFile.h"
#include "TNtuple.h"
#include "TTree.h"
#include "TMath.h"
#include "TList.h"
#include "TString.h"

//
// class decleration
//

class SiStripClustersDump : public edm::one::EDAnalyzer<edm::one::SharedResources> {
public:
  explicit SiStripClustersDump(const edm::ParameterSet&);
  ~SiStripClustersDump() override;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void analyze(const edm::Event&, const edm::EventSetup&) override;

  edm::InputTag inputTagClusters;
  edm::EDGetTokenT<edmNew::DetSetVector<SiStripCluster>> clusterToken;

  TTree* outNtuple;
  edm::Service<TFileService> fs;

  uint32_t detId;
  float barycenter;
  uint16_t width;
  int charge;
  edm::EventNumber_t eventN;
};

SiStripClustersDump::SiStripClustersDump(const edm::ParameterSet& conf) {
  inputTagClusters = conf.getParameter<edm::InputTag>("SiStripClustersTag");
  clusterToken = consumes<edmNew::DetSetVector<SiStripCluster>>(inputTagClusters);

  usesResource("TFileService");

  outNtuple = fs->make<TTree>("clusters", "clusters");
  outNtuple->Branch("event", &eventN, "event/i");
  outNtuple->Branch("detId", &detId, "detId/i");
  outNtuple->Branch("barycenter", &barycenter, "barycenter/F");
  outNtuple->Branch("width", &width, "width/s");
  outNtuple->Branch("charge", &charge, "charge/I");
}

SiStripClustersDump::~SiStripClustersDump() = default;

void SiStripClustersDump::analyze(const edm::Event& event, const edm::EventSetup& es) {
  edm::Handle<edmNew::DetSetVector<SiStripCluster>> clusterCollection = event.getHandle(clusterToken);

  for (const auto& detClusters : *clusterCollection) {
    detId = detClusters.detId();
    eventN = event.id().event();

    for (const auto& cluster : detClusters) {
      barycenter = cluster.barycenter();
      // std::cout << barycenter << ", " << cluster.barycenter() << std::endl;
      width = cluster.size();
      charge = cluster.charge();
      outNtuple->Fill();
    }
  }
}

void SiStripClustersDump::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("SiStripClustersTag", edm::InputTag("siStripClusters"));
  descriptions.add("SiStripClustersDump", desc);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(SiStripClustersDump);
