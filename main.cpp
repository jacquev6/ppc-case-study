#include <algorithm>
#include <cassert>
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <vector>


void step(float* r, const float* d, int n);

void test() {
  constexpr int n = 3;
  const float d[n * n] = {
      0, 8, 2,
      1, 0, 9,
      4, 5, 0,
  };
  float r[n * n];

  step(r, d, n);

  const float expected[] = {
    0, 7, 2,
    1, 0, 3,
    4, 5, 0,
  };
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
      assert(r[i * n + j] == expected[i * n + j]);
    }
  }
}

void benchmark(const int n) {
  std::cout
    << "- n: " << n << "\n" << std::flush;

  const size_t bytes = n * n * sizeof(float);
  float* const d = (float*) malloc(bytes);
  for (int i = 0; i != n; ++i) {
    for (int j = 0; j != n; ++j) {
      d[i * n + j] = float(std::rand()) / RAND_MAX;
    }
  }

  float* const r = (float*) malloc(bytes);

  std::cout
    << "  memory:\n"
    << "    bytes: " << 2 * bytes << "\n"
    << "  duration:\n" << std::flush;

  auto before = std::chrono::steady_clock::now();
  step(r, d, n);
  auto after = std::chrono::steady_clock::now();

  std::cout << "    nanoseconds: " << (after - before).count() << std::endl;

  float x = 0;
  for (int i = 0; i != n; ++i) {
    for (int j = 0; j != n; ++j) {
      x += r[i * n + j];
    }
  }
  assert(x != 0);

  free(r);
  free(d);
}

int main(int argc, const char* argv[]) {
  test();

  for (int i = 1; i != argc; ++i) {
    benchmark(std::stoul(argv[i]));
  }
}
