//
// Created by hzx on 10/12/18.
//

#ifndef POLYNOMIAL_POLYNOMIAL_H
#define POLYNOMIAL_POLYNOMIAL_H

#include <algorithm>
#include <cassert>
#include <ostream>
#include <unordered_map>
#include <cmath>
#include <iostream>

using namespace std;
#define ULL unsigned long long
#define PUU pair<ULL, ULL>


class Polynomial {
public:
    Polynomial(unsigned long long expression) {
        this->expression = expression;
    }

    Polynomial operator+(const Polynomial &x) const {
        return {this->add(x.expression, this->expression)};
    }

    Polynomial operator-(const Polynomial &x) const {
        return {this->sub(this->expression, x.expression)};
    }

    Polynomial operator*(const Polynomial &x) const {
        return {this->mul(this->expression, x.expression)};
    }

    Polynomial operator/(const Polynomial &x) const {
        if (x.expression == 0) {
            throw ZeroModulusException();
        }
        return {this->divAndMod(this->expression, x.expression).first};
    }

    Polynomial operator%(const Polynomial &x) const {
        if (x.expression == 0) {
            throw ZeroModulusException();
        }
        return {this->divAndMod(this->expression, x.expression).second};
    }

    bool operator==(const Polynomial &x) const {
        return this->expression == x.expression;
    }

    bool operator!=(const Polynomial &x) const {
        return this->expression != x.expression;
    }

    friend ostream &operator<<(ostream &out, const Polynomial &x) {
        out << x.expression;
        return out;
    }

    Polynomial gcd(const Polynomial &x) const {
        ULL a = this->expression;
        ULL b = x.expression;
        while (b) {
            ULL t = this->divAndMod(a, b).second;
            a = b, b = t;
        }
        return {a};
    }

    /**
     * @param x the number to calculate egcd(this, x)
     * @return  ((a, b), gcd) where ax+bThis = gcd(x, this)
     */
    pair<pair<Polynomial, Polynomial>, Polynomial> extendGcd(const Polynomial &x) const {
        ULL x1 = 1, x2 = 0, y1 = 0, y2 = 1, v = x.expression, w = this->expression;
        while (w) {
            PUU t = this->divAndMod(v, w);
            v = w, w = t.second;
            ULL t1 = y1, t2 = y2;
            y1 = this->sub(x1, this->mul(y1, t.first));
            y2 = this->sub(x2, this->mul(y2, t.first));
            x1 = t1, x2 = t2;
        }
        return {{x1, x2}, v};
    }

    /**
     * @param x the multiplicative inverse of this mod x
     * @return (doseHas, multiplicativeInverse)
     */
    pair<bool, Polynomial> mulInverse(const Polynomial &x) const {
        if (x.expression == 1) {
            throw MultiplicativeInverseUseModulusOne();
        }
        auto s = this->extendGcd(x);
        return {s.second == 1, s.first.second};
    }

    /**
     * calculate y which st g^y = this
     * @param g: the generating element
     * @param cnt: the element number of this group
     * @return (whether there exist solution, solution)
     */
    pair<bool, Polynomial> discreteLog(const Polynomial &g, const Polynomial &mod, int cnt) const {
        return this->babyStepGiantStep(g.expression, this->expression, mod.expression, cnt);
    }

private:
    int bitLen(ULL x) const {
        int s = 0;
        while (x) {
            s++, x >>= 1;
        }
        return s;
    }

    ULL add(ULL x, ULL y) const {
        return x ^ y;
    }

    ULL mul(ULL x, ULL y) const {
        ULL ans = 0;
        while (y) {
            if (y & 1) {
                ans = this->add(ans, x);
            }
            x <<= 1, y >>= 1;
        }
        return ans;
    }

    ULL sub(ULL x, ULL y) const {
        return this->add(x, y);
    }

    /**
     * return x//y
     */
    ULL div(ULL x, ULL y) const {
        return divAndMod(x, y).first;
    }

    ULL mod(ULL x, ULL y) const {
        return divAndMod(x, y).second;
    }

    /**
     * @param x the number to be div
     * @param y  the number to div x, y should not be zero
     * @return  pair<ULL, ULL>(x//y, x%y)
     */
    pair<ULL, ULL> divAndMod(ULL x, ULL y) const {
        assert(y != 0);
        int xl = bitLen(x), yl = bitLen(y);
        if (xl < yl) {
            return PUU(0, x);
        }
        ULL d = 0;
        while (xl >= yl) {
            x = this->sub(x, y << (xl - yl));
            d = this->add(d, 1ULL << (xl - yl));
            xl = this->bitLen(x);
        }
        return PUU(d, x);
    }

    /**
     * calculate g^x = y (mod n)
     * for an problem on a group, the babyStepGiantStep algorithm works
     * @param cnt: the element count of this group
     * @return (isThereExistSolution, solution)
     */
    pair<bool, ULL> babyStepGiantStep(ULL g, ULL y, ULL n, int cnt) const {
        int x = (int) sqrt(cnt) + 1;
        ULL anMap[x + 1], tmp = 1;
        unordered_map<ULL, int> anMapReserve;
        // for any g and n, there is an cyclic group
        for (int i = 0; i <= x; i++) {
            if (anMapReserve.find(tmp) != anMapReserve.end()) {
                assert(tmp == anMap[0]);
                for (int j = i; j <= x; j++) {
                    anMap[j] = anMap[j % i];
                }
                break;
            }
            anMap[i] = tmp;
            anMapReserve[tmp] = i;
            tmp = mod(mul(tmp, g), n);
        }
        return __babyStepGiantStep(mod(g, n), mod(y, n), n, x, anMap, anMapReserve);
    }

    pair<bool, ULL> __babyStepGiantStep(ULL g, ULL y, ULL n, int x, const ULL anMap[],
                                        unordered_map<ULL, int> &anMapReserve) const {
        ULL s = Polynomial(g).gcd(n).expression;
        if (s != 1) {
            if (mod(y, s) != 0) {
                return {false, 0};
            } else {
                ULL nn = div(n, s), ny = div(y, s), ng = div(g, s);
                auto k = Polynomial(ng).mulInverse(nn);
                ULL ngr = k.second.expression, nny = mod(mul(ngr, ny), nn);
                assert(k.first);
                auto t = __babyStepGiantStep(g, nny, nn, x, anMap, anMapReserve);
                return {t.first, t.second + 1};
            }
        }
        ULL tmp = anMap[0];
        for (int i = 0; i < x; i++) {
            auto w = (Polynomial(tmp)).mulInverse(n);
            assert(w.first);
            ULL q = mod(mul(y, w.second.expression), n);
            auto p = anMapReserve.find(q);
            if (p != anMapReserve.end()) {
                return {true, static_cast<const ULL &>(i * x + p->second)};
            }
            tmp = mod(mul(tmp, anMap[x]), n);
        }
        return {false, 0};
    }

private:
    ULL expression;

    class ZeroModulusException : public exception {
        const char *what() const noexcept override {
            return "the Modulus is zero";
        }
    };

    class MultiplicativeInverseUseModulusOne : public exception {
        const char *what() const noexcept override {
            return "the Modulus use to calculate multiplication inverse is one";
        }
    };
};


#endif //POLYNOMIAL_POLYNOMIAL_H
