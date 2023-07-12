/*
 * @Description: 
 * @FilePath: \youdao\youdao.js
 */
const crypto = require('crypto');
var d = 'fanyideskweb'
var u = 'webfanyi'

function get_cookies() {
    let e = "OUTFOX_SEARCH_USER_ID_NCOO";
    let t = 2147483647 * Math.random();
    let o = new Date;
    o.setTime(o.getTime() + 63072e6);
    return e + "=" + t + ";expires=" + o.toGMTString() + ";path=/;domain=.youdao.com";
}
function md5_1(e) {
    let t = crypto.createHash('md5');
    return t.update(e.toString()).digest('hex')
}
function md5_2(e) {
    let t = crypto.createHash('md5');
    return t.update(e).digest()
}
function get_sign(e, t){
    result = `client=${d}&mysticTime=${e}&product=${u}&key=${t}`
    return md5_1(result)
}

function decode_code(o, n, msg) {
    const a = Buffer.alloc(16, md5_2(o))
        , c = Buffer.alloc(16, md5_2(n))
        , i = crypto.createDecipheriv("aes-128-cbc", a, c);
        let s = i.update(msg, "base64", "utf-8");
        return s += i.final("utf-8"), s
}