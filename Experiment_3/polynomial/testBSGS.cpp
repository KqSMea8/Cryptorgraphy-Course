//
// Created by hzx on 10/19/18.
//


#include <iostream>
#include "Polynomial.h"

/**
 * test the discreteLog method of GF(2^8), using the GF(2^8)'s generating element
 */
void testGF28() {
    int x[] = {3, 5, 6, 9, 11, 14, 17, 18, 19, 20, 23, 24, 25, 26, 28, 30, 31, 33, 34, 35, 39, 40, 42, 44, 48, 49, 60,
               62, 63, 65, 69, 70, 71, 72, 73, 75, 76, 78, 79, 82, 84, 86, 87, 88, 89, 90, 91, 95, 100, 101, 104, 105,
               109, 110, 112, 113, 118, 119, 121, 122, 123, 126, 129, 132, 134, 135, 136, 138, 142, 143, 144, 147, 149,
               150, 152, 153, 155, 157, 160, 164, 165, 166, 167, 169, 170, 172, 173, 178, 180, 183, 184, 185, 186, 190,
               191, 192, 193, 196, 200, 201, 206, 207, 208, 214, 215, 218, 220, 221, 222, 226, 227, 229, 230, 231, 233,
               234, 235, 238, 240, 241, 244, 245, 246, 248, 251, 253, 254, 255};
    int xl = sizeof(x) / sizeof(int);
    for (int i = 0; i < xl; i++) {
        Polynomial mod(0x11b);
        Polynomial g(static_cast<ULL>(x[i]));
        Polynomial tmp(g);
        const int groupOrder = (1 << 8) - 1;
        for (int j = 0; j < (1 << 8) - 1; j++) {
            auto k = tmp.discreteLog(g, mod, groupOrder);
            cout << k.first << " " << k.second << " " << (j + 1) << " " << g << " " << tmp << " " << mod << " " << endl;
            tmp = tmp * g % mod;
            assert(k.first);
            assert(k.second == (j + 1) % groupOrder);
        }
    }
}
