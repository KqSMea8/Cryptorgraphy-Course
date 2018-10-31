/**********************************************************************************
*   Copyright © 2018 H-ZeX. All Rights Reserved.
*
*   File Name:    attack.cpp
*   Author:       H-ZeX
*   Create Time:  2018-10-23-16:59:54
*   Describe:
*
**********************************************************************************/
#include "dec.h"
#include <assert.h>
#include <gmp.h>
#include <stdio.h>

const char *N =
    "1071508607186267320948425049060001810561404811705533607443750388370351051124936122493198"
    "3788156958581275946729175531469002933770824382865926730400902798743137187335810705309884"
    "6355341597977322595205943373851868976298683624144753090015077192592725086694196765086066"
    "30823351242964205044695669333236417591";
const char *E =
    "1033507197783958849532434330701272124186803034586769923345150080902155598940302810374322"
    "1782417440900848403102247012012875905268518785845678756696925714007988778268752026049276"
    "2810253290380710870214468348565666875377299183728637292920159788095066074117110737168986"
    "91660211835403800810547133032654209857";
const char *c_star =
    "77578956825544771401324791883447519867965391774167533692559933526520559797455687879"
    "66196883914901534005536907151568251864100834672394418679303623687590728247425128214"
    "23959166270736914130604102452801162684877374802075310241079026986641176079329871431"
    "448404341153307957496668749957011118721172866996397";

int main() {
    mpz_t n, e, cs, x, y, two, twoInverse, toDec, ans;
    mpz_init(n), mpz_init(e), mpz_init(cs);
    mpz_init(x), mpz_init(y), mpz_init(two), mpz_init(toDec), mpz_init(ans), mpz_init(twoInverse);
    mpz_set_str(n, N, 10), mpz_set_str(e, E, 10), mpz_set_str(cs, c_star, 10), mpz_set_ui(two, 2);
    mpz_powm(y, two, e, n);
    mpz_mul(toDec, cs, y);
    mpz_mod(toDec, toDec, n);
    mpz_out_str(stdout, 10, toDec);
    printf("\n\n");
    char *s = dec(toDec);
    printf("%s\n\n", s);
    mpz_set_str(ans, s, 10);

    mpz_powm_ui(twoInverse, two, -1, n);
    mpz_out_str(stdout, 10, twoInverse);
    printf("\n\n");
    mpz_invert(twoInverse, two, n);
    mpz_out_str(stdout, 10, twoInverse);
    printf("\n\n");

    mpz_mul(ans, twoInverse, ans);
    mpz_mod(ans, ans, n);
    printf("answer: ");
    mpz_out_str(stdout, 10, ans);
    printf("\n\n");
}
