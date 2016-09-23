#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef unsigned ele;

ele rol (ele num, ele cnt);
ele safe_add (ele x, ele y);
ele cmn (ele q, ele a, ele b, ele x, ele s, ele t);
ele ff (ele a, ele b, ele c, ele d, ele x, ele s, ele t);
ele gg (ele a, ele b, ele c, ele d, ele x, ele s, ele t);
ele hh (ele a, ele b, ele c, ele d, ele x, ele s, ele t);
ele ii (ele a, ele b, ele c, ele d, ele x, ele s, ele t);
ele * coreMD5 (ele * x, int len);
ele * str2binl (char * str);
char * binl2hex (ele * binarray);
char * calcMD5 (char * seq);
int count_cat (char * pid, char * calg, char * count);
int write_en_pswd (char *count, char *pswd, char * enpswd);

int main (int argc, char * argv[])
{
    /* argv[1]: origin password, and after pswd_cat, password change to pid */
    char pid[] = "1";
    char calg[] = "12345678";
    if (argc != 3)
    {
        printf ("Usage: %s [student num] [origin password]\n", argv[0]);
        exit (1);
    }
    count_cat (pid, calg, argv[2]);
    write_en_pswd (argv[1], argv[2], strcat(calcMD5(pid), "123456781"));

    return 0;
}

int write_en_pswd (char *count, char *pswd, char * enpswd)
{
    FILE * pswd_file_pointer;
    if ((pswd_file_pointer = fopen("config.ini", "w")) == NULL)
    {
        fprintf (stdout, "Can't open \"config.ini\" file.\n");
        exit(1);
    }
    fprintf (pswd_file_pointer,
            "[userinfo]\ncount=%s\npassword=%s\nenpassword=%s\n",
            count, pswd, enpswd);
    if (fclose (pswd_file_pointer) != 0)
        fprintf (stderr, "Error closeing file\n");
    return 0;
}

int count_cat (char * pid, char * calg, char * count)
{
    strcat (pid, count);
    strcat (pid, calg);
    return 0;
}

ele safe_add (ele x, ele y)
{
    ele lsw, msw, res;
    lsw = (x & 0xffff) + (y & 0xffff);
    msw = (x >> 16) + (y >> 16) + (lsw >> 16);

    res = (msw << 16) | (lsw & 0xffff);
    return res;
}

ele rol (ele num, ele cnt)
{
    ele res;
    res = (num << cnt) | (num >> (32-cnt));
    return res;
}

ele cmn (ele q, ele a, ele b, ele x, ele s, ele t)
{
    ele res;

    res = safe_add (rol (safe_add (safe_add (a, q), safe_add (x, t)), s), b);
    return res;
}

ele ff(ele a, ele b, ele c, ele d, ele x, ele s, ele t)
{
    ele res;

    res = cmn ((b & c) | ((~b) & d), a, b, x, s, t);

    return res;
}

ele ii (ele a, ele b, ele c, ele d, ele x, ele s, ele t)
{
    return cmn (c ^ (b | (~d)), a, b, x, s, t);
}

ele hh (ele a, ele b, ele c, ele d, ele x, ele s, ele t)
{
    return cmn (b ^ c ^ d, a, b, x, s, t);
}

ele gg (ele a, ele b, ele c, ele d, ele x, ele s, ele t)
{
    return cmn ((b & d) | (c & (~d)), a, b, x, s, t);
}

ele * coreMD5 (ele * x, int len)
{
    int i;
    static ele res_core[4];
    ele a = 1732584193;
    ele b = -271733879;
    ele c = -1732584194;
    ele d = 271733878;
    ele olda, oldb, oldc, oldd;

    for (i=0; i < len; i+=16)
    {
        olda = a;
        oldb = b;
        oldc = c;
        oldd = d;
        a = ff(a, b, c, d, x[i+0], 7, -680876936);
        d = ff(d, a, b, c, x[i+1], 12, -389564586);
        c = ff(c, d, a, b, x[i+2], 17, 606105819);
        b = ff(b, c, d, a, x[i+3], 22, -1044525330);
        a = ff(a, b, c, d, x[i+4], 7, -176418897);
        d = ff(d, a, b, c, x[i+5], 12, 1200080426);
        c = ff(c, d, a, b, x[i+6], 17, -1473231341);
        b = ff(b, c, d, a, x[i+7], 22, -45705983);
        a = ff(a, b, c, d, x[i+8], 7, 1770035416);
        d = ff(d, a, b, c, x[i+9], 12, -1958414417);
        c = ff(c, d, a, b, x[i+10], 17, -42063);
        b = ff(b, c, d, a, x[i+11], 22, -1990404162);
        a = ff(a, b, c, d, x[i+12], 7, 1804603682);
        d = ff(d, a, b, c, x[i+13], 12, -40341101);
        c = ff(c, d, a, b, x[i+14], 17, -1502002290);
        b = ff(b, c, d, a, x[i+15], 22, 1236535329);
        a = gg(a, b, c, d, x[i+1], 5, -165796510);
        d = gg(d, a, b, c, x[i+6], 9, -1069501632);
        c = gg(c, d, a, b, x[i+11], 14 ,643717713);
        b = gg(b, c, d, a, x[i+0], 20, -373897302);
        a = gg(a, b, c, d, x[i+5], 5, -701558691);
        d = gg(d, a, b, c, x[i+10], 9, 38016083);
        c = gg(c, d, a, b, x[i+15], 14, -660478335);
        b = gg(b, c, d, a, x[i+4], 20, -405537848);
        a = gg(a, b, c, d, x[i+9], 5, 568446438);
        d = gg(d, a, b, c, x[i+14], 9, -1019803690);
        c = gg(c, d, a, b, x[i+3], 14, -187363961);
        b = gg(b, c, d, a, x[i+8], 20, 1163531501);
        a = gg(a, b, c, d, x[i+13], 5, -1444681467);
        d = gg(d, a, b, c, x[i+2], 9, -51403784);
        c = gg(c, d, a, b, x[i+7], 14, 1735328473);
        b = gg(b, c, d, a, x[i+12], 20, -1926607734);
        a = hh(a, b, c, d, x[i+5], 4, -378558);
        d = hh(d, a, b, c, x[i+8], 11, -2022574463);
        c = hh(c, d, a, b, x[i+11], 16, 1839030562);
        b = hh(b, c, d, a, x[i+14], 23, -35309556);
        a = hh(a, b, c, d, x[i+1], 4, -1530992060);
        d = hh(d, a, b, c, x[i+4], 11, 1272893353);
        c = hh(c, d, a, b, x[i+7], 16, -155497632);
        b = hh(b, c, d, a, x[i+10], 23, -1094730640);
        a = hh(a, b, c, d, x[i+13], 4, 681279174);
        d = hh(d, a, b, c, x[i+0], 11, -358537222);
        c = hh(c, d, a, b, x[i+3], 16, -722521979);
        b = hh(b, c, d, a, x[i+6], 23, 76029189);
        a = hh(a, b, c, d, x[i+9], 4, -640364487);
        d = hh(d, a, b, c, x[i+12], 11, -421815835);
        c = hh(c, d, a, b, x[i+15], 16, 530742520);
        b = hh(b, c, d, a, x[i+2], 23, -995338651);
        a = ii(a, b, c, d, x[i+0], 6, -198630844);
        d = ii(d, a, b, c, x[i+7], 10, 1126891415);
        c = ii(c, d, a, b, x[i+14], 15, -1416354905);
        b = ii(b, c, d, a, x[i+5], 21, -57434055);
        a = ii(a, b, c, d, x[i+12], 6, 1700485571);
        d = ii(d, a, b, c, x[i+3], 10, -1894986606);
        c = ii(c, d, a, b, x[i+10], 15, -1051523);
        b = ii(b, c, d, a, x[i+1], 21, -2054922799);
        a = ii(a, b, c, d, x[i+8], 6, 1873313359);
        d = ii(d, a, b, c, x[i+15], 10, -30611744);
        c = ii(c, d, a, b, x[i+6], 15, -1560198380);
        b = ii(b, c, d, a, x[i+13], 21, 1309151649);
        a = ii(a, b, c, d, x[i+4], 6, -145523070);
        d = ii(d, a, b, c, x[i+11], 10, -1120210379);
        c = ii(c, d, a, b, x[i+2], 15, 718787259);
        b = ii(b, c, d, a, x[i+9], 21, -343485551);

        a = safe_add (a, olda);
        b = safe_add (b, oldb);
        c = safe_add (c, oldc);
        d = safe_add (d, oldd);
        *res_core = a;
        *(res_core+1) = b;
        *(res_core+2) = c;
        *(res_core+3) = d;
    }

    return res_core;
}

char * binl2hex (ele * binarray)
{
    int i;
    char hex_tab[] = "0123456789abcdef";
    static char seq_hex[] = "01010000111001011000110100010011";

    for (i=0; i < 16; i++)
    {
        *(seq_hex + 2*i) = hex_tab[(binarray[i >> 2] >> ((i % 4) * 8 + 4)) & 0xf];
        *(seq_hex + 2*i + 1) = hex_tab[(binarray[i >> 2] >> ((i % 4) * 8)) & 0xf];
    }
    return seq_hex;
}

ele * str2binl (char * str)
{
    int LEN, i;
    LEN = (int) strlen (str);
    ele nblk = ((LEN + 8) >> 6) + 1;
    static ele blks[16] = {
                    0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 0, 0, 0};

    for (i=0; i < LEN; i++)
        blks[i>>2] |= ((str[i] & 0xff) << ((i % 4) * 8));
    blks[i >> 2] |= (0x80 << ((i % 4) * 8));
    blks[nblk * 16 -2] = LEN * 8;
    return blks;
}

char * calcMD5 (char * seq)
{
    return binl2hex (coreMD5 (str2binl (seq), 16));
}
