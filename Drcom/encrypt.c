#include <stdio.h>
#include <string.h>

#define sv 2
#define sv1 0
#define ps 1
#define pid '1'
#define calg "12345678"

typedef unsigned ele;

ele rol (ele num, ele cnt);
ele safe_add (ele x, ele y);
ele cmn (ele q, ele a, ele b, ele x, ele s, ele t);
ele ff(ele a, ele b, ele c, ele d, ele x, ele s, ele t);
ele gg (ele a, ele b, ele c, ele d, ele x, ele s, ele t);
ele hh (ele a, ele b, ele c, ele d, ele x, ele s, ele t);
ele ii (ele a, ele b, ele c, ele d, ele x, ele s, ele t);
ele coreMD5 (ele * x, int len);
char * binl2hex (ele * binarray);
ele * str2binl (char * str);

int main (void)
{
    ele a = 1732584193;
    ele b = -271733879;
    ele c = -1732584194;
    ele d = 271733878;
    ele res = 0;

//    res = ff ((b & c) | ((~b) & d), a, b, -1120239730, 875574577, 7, -680876936);
    res = ff (a, b, c, d, 875574577, 7, -680876936);
    printf ("res: %x\n", res);
    printf ("wanna res: %x\n", -1120239730);

    return 0;
}

ele safe_add (ele x, ele y)
{
    ele lsw, msw, res;
    lsw = (x & 0xffff) + (y & 0xffff);
    msw = (x >> 16) + (y >> 16) + (lsw >> 16);

    res = (msw << 16) | (lsw & 0xffff);
//    printf ("safe_add: %u\n", res);
    return res;
}

ele rol (ele num, ele cnt)
{
    ele res;
    res = (num << cnt) | (num >> (32-cnt));
//    printf ("rol: %u\n", res);
    return res;
}

ele cmn (ele q, ele a, ele b, ele x, ele s, ele t)
{
    ele res;

    res = safe_add (rol (safe_add (safe_add (a, q), safe_add (x, t)), s), b);
//    printf ("cmn: %u\n", res);
    return res;
}

ele ff(ele a, ele b, ele c, ele d, ele x, ele s, ele t)
{
    ele res;

    res = cmn ((b & c) | ((~b) & d), a, b, x, s, t);

    return res;
}
