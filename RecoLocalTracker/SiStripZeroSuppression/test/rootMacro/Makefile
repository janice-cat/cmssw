all: plotClusterShape.o

plotClusterShape.o: plotClusterShape.cc
	g++ `root-config --cflags --glibs` -O3 plotClusterShape.cc -o plotClusterShape.o

runSmallSample: plotClusterShape.o
	rm -rf img/smallSample/ log/smallSample/
	mkdir -p img/smallSample/ log/smallSample/

	$(eval ev := $(shell echo 44835133))

	./plotClusterShape.o ../output/hybridZS_sep19_2_1_dump_rawprime.root \
											 img/smallSample/hybridZS/ \
											 0 ${ev} > log/smallSample/hybridZS_sep19_2_1_dump_rawprime_0.log
	./plotClusterShape.o ../output/hybridZS_sep19_2_1_dump_rawprime.root \
											 img/smallSample/hybridZS/ \
											 1 ${ev} > log/smallSample/hybridZS_sep19_2_1_dump_rawprime_1.log

	./plotClusterShape.o ../output/hybridZS_withDetIDMask_sep19_2_1_dump_rawprime.root \
											 img/smallSample/hybridZS_withDetIDMask/ \
											 0 ${ev} > log/smallSample/hybridZS_withDetIDMask_sep19_2_1_dump_rawprime_0.log
	./plotClusterShape.o ../output/hybridZS_withDetIDMask_sep19_2_1_dump_rawprime.root \
											 img/smallSample/hybridZS_withDetIDMask/ \
											 1 ${ev} > log/smallSample/hybridZS_withDetIDMask_sep19_2_1_dump_rawprime_1.log

	./plotClusterShape.o ../output/FEDlikeZS_sep19_2_1_dump_rawprime.root \
											 img/smallSample/FEDlikeZS/ \
											 0 ${ev} > log/smallSample/FEDlikeZS_sep19_2_1_dump_rawprime_0.log
	./plotClusterShape.o ../output/FEDlikeZS_sep19_2_1_dump_rawprime.root \
											 img/smallSample/FEDlikeZS/ \
											 1 ${ev} > log/smallSample/FEDlikeZS_sep19_2_1_dump_rawprime_1.log
	
	ls img/smallSample/hybridZS/ | grep approxclustersShape > img/smallSample/hybridZS/catalog_ev${ev}.txt
	ls img/smallSample/hybridZS_withDetIDMask/ | grep approxclustersShape > img/smallSample/hybridZS_withDetIDMask/catalog_ev${ev}.txt
	ls img/smallSample/FEDlikeZS/ | grep approxclustersShape > img/smallSample/FEDlikeZS/catalog_ev${ev}.txt

	diff img/smallSample/FEDlikeZS/catalog_ev${ev}.txt img/smallSample/hybridZS/catalog_ev${ev}.txt > log/smallSample/FEDlikeZS_vs_hybridZS.diff || echo '< FEDlikeZS > hybridZS'
	cat log/smallSample/FEDlikeZS_vs_hybridZS.diff
	diff img/smallSample/hybridZS/catalog_ev${ev}.txt img/smallSample/hybridZS_withDetIDMask/catalog_ev${ev}.txt > log/smallSample/woMask_vs_wMask_ev${ev}.diff || echo '< w/o DetID mask > w/ DetID mask'
	cat log/smallSample/woMask_vs_wMask_ev${ev}.diff


run2024Data_crab_ls35: plotClusterShape.o
	rm -rf img/2024Data_crab_ls35/ log/2024Data_crab_ls35/
	mkdir -p img/2024Data_crab_ls35/ log/2024Data_crab_ls35/

	$(eval ev := $(shell echo 36741922))

	./plotClusterShape.o ../output/hybridZS_2024Data_crab_ls35_sep19_2_1_dump_rawprime.root \
											 img/2024Data_crab_ls35/hybridZS/ \
											 0 ${ev} > log/2024Data_crab_ls35/hybridZS_2024Data_crab_ls35_sep19_2_1_dump_rawprime_0_ev${ev}.log
	#./plotClusterShape.o ../output/hybridZS_2024Data_crab_ls35_sep19_2_1_dump_rawprime.root \
	#										 img/2024Data_crab_ls35/hybridZS/ \
	#										 1 ${ev} > log/2024Data_crab_ls35/hybridZS_2024Data_crab_ls35_sep19_2_1_dump_rawprime_1_ev${ev}.log

	./plotClusterShape.o ../output/hybridZS_withDetIDMask_2024Data_crab_ls35_sep19_2_1_dump_rawprime.root \
											 img/2024Data_crab_ls35/hybridZS_withDetIDMask/ \
											 0 ${ev} > log/2024Data_crab_ls35/hybridZS_withDetIDMask_2024Data_crab_ls35_sep19_2_1_dump_rawprime_0_ev${ev}.log
	#./plotClusterShape.o ../output/hybridZS_withDetIDMask_2024Data_crab_ls35_sep19_2_1_dump_rawprime.root \
	#										 img/2024Data_crab_ls35/hybridZS_withDetIDMask/ \
	#										 1 ${ev} > log/2024Data_crab_ls35/hybridZS_withDetIDMask_2024Data_crab_ls35_sep19_2_1_dump_rawprime_1_ev${ev}.log
	
	ls img/2024Data_crab_ls35/hybridZS/ | grep lustersShape > img/2024Data_crab_ls35/hybridZS/catalog_ev${ev}.txt
	ls img/2024Data_crab_ls35/hybridZS_withDetIDMask/ | grep lustersShape > img/2024Data_crab_ls35/hybridZS_withDetIDMask/catalog_ev${ev}.txt

	diff img/2024Data_crab_ls35/hybridZS/catalog_ev${ev}.txt img/2024Data_crab_ls35/hybridZS_withDetIDMask/catalog_ev${ev}.txt > log/2024Data_crab_ls35/woMask_vs_wMask_ev${ev}.diff || echo '< w/o DetID mask > w/ DetID mask'
	cat log/2024Data_crab_ls35/woMask_vs_wMask_ev${ev}.diff

	$(eval ev := $(shell echo 36998187))

	./plotClusterShape.o ../output/hybridZS_2024Data_crab_ls35_sep19_2_1_dump_rawprime.root \
											 img/2024Data_crab_ls35/hybridZS/ \
											 0 ${ev} > log/2024Data_crab_ls35/hybridZS_2024Data_crab_ls35_sep19_2_1_dump_rawprime_0_ev${ev}.log
	#./plotClusterShape.o ../output/hybridZS_2024Data_crab_ls35_sep19_2_1_dump_rawprime.root \
	#										 img/2024Data_crab_ls35/hybridZS/ \
	#										 1 ${ev} > log/2024Data_crab_ls35/hybridZS_2024Data_crab_ls35_sep19_2_1_dump_rawprime_1_ev${ev}.log

	./plotClusterShape.o ../output/hybridZS_withDetIDMask_2024Data_crab_ls35_sep19_2_1_dump_rawprime.root \
											 img/2024Data_crab_ls35/hybridZS_withDetIDMask/ \
											 0 ${ev} > log/2024Data_crab_ls35/hybridZS_withDetIDMask_2024Data_crab_ls35_sep19_2_1_dump_rawprime_0_ev${ev}.log
	#./plotClusterShape.o ../output/hybridZS_withDetIDMask_2024Data_crab_ls35_sep19_2_1_dump_rawprime.root \
	#										 img/2024Data_crab_ls35/hybridZS_withDetIDMask/ \
	#										 1 ${ev} > log/2024Data_crab_ls35/hybridZS_withDetIDMask_2024Data_crab_ls35_sep19_2_1_dump_rawprime_1_ev${ev}.log
	
	ls img/2024Data_crab_ls35/hybridZS/ | grep lustersShape > img/2024Data_crab_ls35/hybridZS/catalog_ev${ev}.txt
	ls img/2024Data_crab_ls35/hybridZS_withDetIDMask/ | grep lustersShape > img/2024Data_crab_ls35/hybridZS_withDetIDMask/catalog_ev${ev}.txt

	diff img/2024Data_crab_ls35/hybridZS/catalog_ev${ev}.txt img/2024Data_crab_ls35/hybridZS_withDetIDMask/catalog_ev${ev}.txt > log/2024Data_crab_ls35/woMask_vs_wMask_ev${ev}.diff || echo '< w/o DetID mask > w/ DetID mask'
	cat log/2024Data_crab_ls35/woMask_vs_wMask_ev${ev}.diff

	$(eval ev := $(shell echo 37012525))

	./plotClusterShape.o ../output/hybridZS_2024Data_crab_ls35_sep19_2_1_dump_rawprime.root \
											 img/2024Data_crab_ls35/hybridZS/ \
											 0 ${ev} > log/2024Data_crab_ls35/hybridZS_2024Data_crab_ls35_sep19_2_1_dump_rawprime_0_ev${ev}.log
	#./plotClusterShape.o ../output/hybridZS_2024Data_crab_ls35_sep19_2_1_dump_rawprime.root \
	#										 img/2024Data_crab_ls35/hybridZS/ \
	#										 1 ${ev} > log/2024Data_crab_ls35/hybridZS_2024Data_crab_ls35_sep19_2_1_dump_rawprime_1_ev${ev}.log

	./plotClusterShape.o ../output/hybridZS_withDetIDMask_2024Data_crab_ls35_sep19_2_1_dump_rawprime.root \
											 img/2024Data_crab_ls35/hybridZS_withDetIDMask/ \
											 0 ${ev} > log/2024Data_crab_ls35/hybridZS_withDetIDMask_2024Data_crab_ls35_sep19_2_1_dump_rawprime_0_ev${ev}.log
	#./plotClusterShape.o ../output/hybridZS_withDetIDMask_2024Data_crab_ls35_sep19_2_1_dump_rawprime.root \
	#										 img/2024Data_crab_ls35/hybridZS_withDetIDMask/ \
	#										 1 ${ev} > log/2024Data_crab_ls35/hybridZS_withDetIDMask_2024Data_crab_ls35_sep19_2_1_dump_rawprime_1_ev${ev}.log
	
	ls img/2024Data_crab_ls35/hybridZS/ | grep lustersShape > img/2024Data_crab_ls35/hybridZS/catalog_ev${ev}.txt
	ls img/2024Data_crab_ls35/hybridZS_withDetIDMask/ | grep lustersShape > img/2024Data_crab_ls35/hybridZS_withDetIDMask/catalog_ev${ev}.txt

	diff img/2024Data_crab_ls35/hybridZS/catalog_ev${ev}.txt img/2024Data_crab_ls35/hybridZS_withDetIDMask/catalog_ev${ev}.txt > log/2024Data_crab_ls35/woMask_vs_wMask_ev${ev}.diff || echo '< w/o DetID mask > w/ DetID mask'
	cat log/2024Data_crab_ls35/woMask_vs_wMask_ev${ev}.diff
	