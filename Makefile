versions=$(patsubst %.cpp,%,$(wildcard v?.cpp))


link: $(patsubst %,build/%,$(versions))

build/%: build/main.o build/%.o
	g++ $^ -o $@

build/%.o: %.cpp
	g++ -c -O3 -march=native -std=c++17 $< -o $@


benchmark: v0.yml

v0.yml: build/v0
	build/v0 $$(seq 250 250 4000) | tee build/v0.yml
	mv build/v0.yml v0.yml
