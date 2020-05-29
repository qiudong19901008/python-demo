/*
 * @Author: 秋冬
 * @Date: 2020-04-24 18:30:03
 */
function tacSign(e, t) {
    var n = "";
    /^http/.test(e) || (/\/toutiao\//.test(e) || (e = "/toutiao" + e),
    e = location.protocol + "//" + location.host + e);
    for (var r in t)
        n += "&" + r + "=" + encodeURIComponent(t[r]);
    e += e.indexOf("?") > -1 ? e.indexOf("&") > -1 ? n : n.slice(1) : "?" + n.slice(1);
    var o = {
        url: e
    }
      , i = window.byted_acrawler.sign ? window.byted_acrawler.sign(o) : "";
    return i
}
