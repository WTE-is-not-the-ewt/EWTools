var randomStringChars = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678";
function randomString() {
    for (var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : 8, t = randomStringChars.length, r = "", n = 0; n < e; n++)
        r += randomStringChars.charAt(Math.floor(Math.random() * t));
    return r
}

`
fcUpload = function e(t) {
    var r, n, o, s, a, u, l, c, d, h, p, f, g, m, y, v;
    r = i._options,
    n = r.secret,
    o = r.sessionId,
    s = t.CommonPackage,
    a = s.mstid,
    u = s.userid,
    l = t.EventPackage,
    c = l[0],
    d = c.stay_time,
    h = c.report_time,
    p = c.lesson_id,
    f = c.uuid,
    g = c.action,
    m = makeSecretKey({
        action: g,
        duration: d,
        mstid: a,
        timestamp: h,
        version: "2022-08-02",
        signatureMethod: "HMAC-SHA1",
        signatureVersion: "1.0"
    }, n),
    y = _objectSpread$5(_objectSpread$5({}, t), {}, {
        signature: m,
        sn: "ewt_web_video_detail"
    }),
    pointFCUpload(y, {
        TrVideoBizCode: i._options.videoBizCode,
        TrFallback: 0,
        TrUserId: u,
        TrLessonId: p,
        TrUuId: f
    }, {
        "x-bfe-session-id": o
    });
}

// --- m3u8 related ---

function b(r) {
    for (var n = 0; void 0 !== n; ) {
        var i = 3 & n >> 2;
        switch (3 & n) {
        case 0:
            switch (i) {
            case 0:
                var o = t[13][t[14]](t[15])[t[16]]()[e[12]](e[2]) + e[13]
                    , s = t[17]
                    , a = e[2]
                    , u = e[0];
                n = 4;
                continue;
            case 1:
                n = u < s[e[14]] ? 8 : 5;
                continue;
            case 2:
                var l = t[18];
                l = s[e[15]](u) - (e[16] + l);
                a += e[17][t[6]](l),
                n = 1;
                continue
            }
            continue;
        case 1:
            switch (i) {
            case 0:
                u++,
                n = 4;
                continue;
            case 1:
                var c = (o += a) + t[19]
                    , d = new de;
                return d[e[18]](c),
                d[e[19]](r)
            }
            continue
        }
    }
}

function a(r) {
    for (var n = 4; void 0 !== n; ) {
        var i = 3 & n >> 2;
        switch (3 & n) {
        case 0:
            switch (i) {
            case 0:
                o = d,
                s = Math[g](),
                s *= c,
                s = Math[m](s),
                d = o + (s = _[y](s)),
                n = 6;
                continue;
            case 1:
                var o = t[1]
                    , s = e[0]
                    , a = (t[1],
                e[1])
                    , u = e[2]
                    , l = e[0];
                n = 14;
                continue;
            case 2:
                r = b;
                var c = _[t[2]]
                    , d = e[2]
                    , h = e[0]
                    , p = t[1]
                    , f = t[9]
                    , g = (f += e[7]) + e[8]
                    , m = e[9]
                    , y = (f = t[10],
                (f += e[10]) + t[11]);
                n = 6;
                continue;
            case 3:
                n = 13;
                continue
            }
            continue;
        case 1:
            switch (i) {
            case 0:
                h += e[11],
                n = 3;
                continue;
            case 1:
                l++,
                n = 14;
                continue;
            case 2:
                n = p ? 1 : 3;
                continue;
            case 3:
                return d
            }
            continue;
        case 2:
            switch (i) {
            case 0:
                b = t[7] - parseInt(e[6], t[8]),
                n = 8;
                continue;
            case 1:
                n = t[12] ? 9 : 13;
                continue;
            case 2:
                var v = parseInt(e[3], t[3]);
                v = a[t[4]](l) - (parseInt(e[4], e[5]) + v);
                u += t[5][t[6]](v),
                n = 5;
                continue;
            case 3:
                n = l < a[t[2]] ? 10 : 7;
                continue
            }
            continue;
        case 3:
            switch (i) {
            case 0:
                p = t[12],
                n = (o = h < r) ? 0 : 12;
                continue;
            case 1:
                var _ = u
                    , b = r;
                n = b ? 8 : 2;
                continue
            }
            continue
        }
    }
}

randomUUID = function() {
    for (var e = [], t = "0123456789abcdef", r = 0; r < 36; r++)
        e[r] = t.substr(Math.floor(16 * Math.random()), 1);
    return e[14] = "4",
    e[19] = t.substr(3 & e[19] | 8, 1),
    e[8] = e[13] = e[18] = e[23] = "-",
    e.join("")
}
`
