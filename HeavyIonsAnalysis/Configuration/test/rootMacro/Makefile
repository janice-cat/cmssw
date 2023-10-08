all: L1JetTurnOn.o L1ZDCTrigEff.o

L1JetTurnOn.o: L1JetTurnOn.cc
	g++ `root-config --cflags --glibs` -O3 L1JetTurnOn.cc -o L1JetTurnOn.o

L1ZDCTrigEff.o: L1ZDCTrigEff.cc
	g++ `root-config --cflags --glibs` -O3 L1ZDCTrigEff.cc -o L1ZDCTrigEff.o

