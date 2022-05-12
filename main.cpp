#include <iostream>
#include <cassert>


void step(float* r, const float* d, int n);

void test() {
  constexpr int n = 3;
  const float d[n*n] = {
      0, 8, 2,
      1, 0, 9,
      4, 5, 0,
  };
  float r[n*n];
  step(r, d, n);

  const float expected[] = {
    0, 7, 2,
    1, 0, 3,
    4, 5, 0,
  };
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
      assert(r[i*n + j] == expected[i * n + j]);
    }
  }
}

void benchmark(const unsigned long max_size) {
  std::cout << max_size << "\n";
}

int main(int argc, const char* argv[]) {
  test();
  assert(argc == 2);
  benchmark(std::stoul(argv[1]));
}
