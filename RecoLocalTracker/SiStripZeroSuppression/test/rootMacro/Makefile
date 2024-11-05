all: plotClusterShape.o

plotClusterShape.o: plotClusterShape.cc
	g++ `root-config --cflags --glibs` -O3 plotClusterShape.cc -o plotClusterShape.o

runAll: plotClusterShape.o
	./plotClusterShape.o ../output/hybridZS_sep19_2_1_dump_rawprime.root \
											 img/hybridZS/ \
											 0 44835133
	./plotClusterShape.o ../output/hybridZS_sep19_2_1_dump_rawprime.root \
											 img/hybridZS/ \
											 1 44835133

	./plotClusterShape.o ../output/hybridZS_withDetIDMask_sep19_2_1_dump_rawprime.root \
											 img/hybridZS_withDetIDMask/ \
											 0 44835133
	./plotClusterShape.o ../output/hybridZS_withDetIDMask_sep19_2_1_dump_rawprime.root \
											 img/hybridZS_withDetIDMask/ \
											 1 44835133

	./plotClusterShape.o ../output/FEDlikeZS_sep19_2_1_dump_rawprime.root \
											 img/FEDlikeZS/ \
											 0 44835133
	./plotClusterShape.o ../output/FEDlikeZS_sep19_2_1_dump_rawprime.root \
											 img/FEDlikeZS/ \
											 1 44835133
	
	ls img/hybridZS/ | grep approxclustersShape > img/hybridZS/catalog_ev44835133.txt
	ls img/hybridZS_withDetIDMask/ | grep approxclustersShape > img/hybridZS_withDetIDMask/catalog_ev44835133.txt
	ls img/FEDlikeZS/ | grep approxclustersShape > img/FEDlikeZS/catalog_ev44835133.txt

	diff img/FEDlikeZS/catalog_ev44835133.txt img/hybridZS/catalog_ev44835133.txt > log/FEDlikeZS_vs_hybridZS.diff || echo '< FEDlikeZS > hybridZS'
	cat log/FEDlikeZS_vs_hybridZS.diff
	diff img/hybridZS/catalog_ev44835133.txt img/hybridZS_withDetIDMask/catalog_ev44835133.txt > log/woMask_vs_wMask.diff || echo '< w/o DetID mask > w/ DetID mask'
	cat log/woMask_vs_wMask.diff