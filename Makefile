versions=$(patsubst %.cpp,%,$(wildcard v?.cpp))

default: $(patsubst %,build/%,$(versions))

build/%: build/main.o build/%.o
	g++ $^ -o $@

build/%.o: %.cpp
	g++ -c -O3 $< -o $@
