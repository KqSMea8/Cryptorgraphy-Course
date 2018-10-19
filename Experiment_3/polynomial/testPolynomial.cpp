//
// Created by hzx on 10/19/18.
//


#include "Polynomial.h"

void testPolynomial(ULL times) {
    for (int i = 0; i < times; i++) {
        Polynomial p1 = random() % 0xffff + 1;
        Polynomial p2 = random() % 0xffff + 1;
        Polynomial p3 = p1 + p2;
        auto p4 = p3 - p2;
        auto p5 = p3 - p1;
        cout << p1 << " " << p2 << " " << p3 << " " << p4 << " " << p5 << endl;
        assert(p1 == p4);
        assert(p2 == p5);
        p3 = p1 * p2;
        p4 = p3 / p1;
        p5 = p3 / p2;
        cout << p1 << " " << p2 << " " << p3 << " " << p4 << " " << p5 << endl;
        assert(p4 == p2);
        assert(p5 == p1);
        p3 = p1 / p2;
        p4 = p1 % p2;
        cout << p1 << " " << p2 << " " << p3 << " " << p4 << endl;
        assert(p3 * p2 + p4 == p1);
        auto s = p1.extendGcd(p2);
        p5 = s.first.first * p2 + s.first.second * p1;
        cout << p1 << " " << p2 << " " << s.first.first << " " << s.first.second << " " << s.second << " " << p5
             << endl;
        assert(p5 == s.second);
        p3 = p1.gcd(p2);
        cout << p1 << " " << p2 << " " << p3 << " " << s.second << endl;
        assert(p3 == s.second);
        if (p2 == 1) {
            continue;
        }
        auto k = p1.mulInverse(p2);
        cout << p1 << " " << p2 << " " << k.second << endl;
        if (k.first) {
            assert(k.second * p1 % p2 == Polynomial(1));
        }
    }
}
