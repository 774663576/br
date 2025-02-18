const crypto = require('crypto');
 
 
function a(e){
        const md5 = crypto.createHash('md5');
        return md5.update(e).digest('hex')
}
u = function(t) {
                return ~~(Math["random"]() * t)
            };
function get_xmsign(timestamp) {
                    var t, e, r, n = 0;
                    return n =timestamp ,
                    t = this["secretKey"],
                    e = n,
                    r = Date["now"](),
                    ("{" + t + e + "}(" + u(100) + ")" + e + "(" + u(100) + ")" + r)["replace"](/{([\w-]+)}/, (function(t, e) {
                        return a(e)
                    }
                    ))
                }
 
                console.log(get_xmsign())
