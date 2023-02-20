/**
 * @author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
 * @license This software is free - http://www.gnu.org/licenses/gpl.html
 */

#include <chrono>
#include <iostream>

double some_func(double x) {
    return x * x + x;
}

double integral(double (*f)(double), double a, double b, int n) {
    /**
     * Estimate the area beneath the curve f, between the
     * abscissas a and b; the region is approximated as n rectangles.
     */
    auto total = 0.0;
    auto dx = (b - a) / n;
    for (auto i = 0; i < n; ++i) {
        total += dx * f(a + dx * i);
    }
    return total;
}

int main(int argc, char **argv) {
    double a = 1, b = 10;
    int n = 100'000'000;
    if (argc >= 4) {
        a = std::stod(argv[1]);
        b = std::stod(argv[2]);
        n = std::stoi(argv[3]);
    }

    auto start = std::chrono::steady_clock::now();

    std::cout << "integral: " << integral(some_func, a, b, n) << std::endl;

    auto end = std::chrono::steady_clock::now();
    std::chrono::duration<double> elapsed_seconds = end-start;
    std::cout << "elapsed time: " << elapsed_seconds.count() << "s\n";
}
