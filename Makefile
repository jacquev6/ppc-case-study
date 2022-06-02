cpu_versions=$(patsubst %.cpp,%,$(wildcard cpu-*.cpp))
gpu_versions=$(patsubst %.cu,%,$(wildcard gpu-*.cu))


link: $(patsubst %,build/%,$(cpu_versions) $(gpu_versions)) $(patsubst %,build/%-paral,$(cpu_versions))

gpp_flags=-O3 -march=native -std=c++17

build/cpu-%: build/main.o build/cpu-%.o
	g++ $^ $(gpp_flags) -L/usr/local/cuda-11.2/targets/x86_64-linux/lib -lcudart -o $@

build/%.o: %.cpp
	g++ $(gpp_flags) -c $< -o $@

build/cpu-%-paral: build/main.o build/cpu-%-paral.o
	g++ $^ $(gpp_flags) -fopenmp -o $@

build/%-paral.o: %.cpp
	g++ $(gpp_flags) -fopenmp -c $< -o $@


nvcc_flags=-O3 -std=c++17

build/gpu-%: build/main.o build/gpu-%.o
	nvcc $^ $(nvcc_flags) -o $@

build/%.o: %.cu
	nvcc $(nvcc_flags) -c $< -o $@


benchmark: $(patsubst %,build/%-seq.yml,$(cpu_versions)) $(patsubst %,build/%-paral-4.yml,$(cpu_versions)) $(patsubst %,build/%-paral-14.yml,$(cpu_versions)) $(patsubst %,build/%-paral-28.yml,$(cpu_versions)) $(patsubst %,build/%.yml,$(gpu_versions))

upper_bound=5000

build/cpu-%-seq.yml: build/cpu-%
	$< $$(seq 250 250 $(upper_bound)) | tee $@.tmp
	mv $@.tmp $@

build/cpu-%-paral-4.yml: build/cpu-%-paral
	OMP_NUM_THREADS=4 $< $$(seq 250 250 $(upper_bound)) | tee $@.tmp
	mv $@.tmp $@

build/cpu-%-paral-14.yml: build/cpu-%-paral
	OMP_NUM_THREADS=14 $< $$(seq 250 250 $(upper_bound)) | tee $@.tmp
	mv $@.tmp $@

build/cpu-%-paral-28.yml: build/cpu-%-paral
	OMP_NUM_THREADS=28 $< $$(seq 250 250 $(upper_bound)) | tee $@.tmp
	mv $@.tmp $@

build/gpu-%.yml: build/gpu-%
	$< $$(seq 250 250 $(upper_bound)) | tee $@.tmp
	mv $@.tmp $@
