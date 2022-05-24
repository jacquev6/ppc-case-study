versions=$(patsubst %.cpp,%,$(wildcard v?.cpp))


link: $(patsubst %,build/%,$(versions)) $(patsubst %,build/%-paral,$(versions))

CFLAGS=-O3 -march=native -std=c++17

build/%: build/main.o build/%.o
	g++ $^ $(CFLAGS) -o $@

build/%.o: %.cpp
	g++ $(CFLAGS) -c $< -o $@

build/%-paral: build/main.o build/%-paral.o
	g++ $^ $(CFLAGS) -fopenmp -o $@

build/%-paral.o: %.cpp
	g++ $(CFLAGS) -fopenmp -c $< -o $@


benchmark: $(patsubst %,build/%-seq.yml,$(versions)) $(patsubst %,build/%-paral-4.yml,$(versions)) $(patsubst %,build/%-paral-14.yml,$(versions)) $(patsubst %,build/%-paral-28.yml,$(versions))

build/%-seq.yml: build/%
	$< $$(seq 250 250 5000) | tee $@.tmp
	mv $@.tmp $@

build/%-paral-4.yml: build/%-paral
	OMP_NUM_THREADS=4 $< $$(seq 250 250 5000) | tee $@.tmp
	mv $@.tmp $@

build/%-paral-14.yml: build/%-paral
	OMP_NUM_THREADS=14 $< $$(seq 250 250 5000) | tee $@.tmp
	mv $@.tmp $@

build/%-paral-28.yml: build/%-paral
	OMP_NUM_THREADS=28 $< $$(seq 250 250 5000) | tee $@.tmp
	mv $@.tmp $@
