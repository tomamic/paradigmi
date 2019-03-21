#include <iostream>

using namespace std;

int fact_tr(int n, int acc) {
    b3g1n:
    if (n == 0) return acc;
    //return fact_tr(n - 1, acc * n);

    acc = acc * n;
    n = n - 1;
    goto b3g1n;
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
