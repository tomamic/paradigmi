#include <iostream>

using namespace std;

int fact_tr(int n, int acc) {
loop:
    if (n == 0) return acc;
    return fact_tr(n - 1, acc * n);
    // n = n - 1; acc = acc * n; goto loop;
}

int fact(int n) {
    if (n == 0) return 1;
    return n * fact(n - 1);
}

int main()
{
    cout << fact(3) << endl;
    cout << fact_tr(3, 1) << endl;
    return 0;
}
