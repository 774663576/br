var opts = {
		content: 		'[title]',		// content to display ('[title]', 'string', element, function(updateCallback){...}, jQuery)
		className:		'tip-yellowsimple',	// class for the tips
		bgImageFrameSize:	10,			// size in pixels for the background-image (if set in CSS) frame around the inner content of the tip
		showTimeout:		500,		// timeout before showing the tip (in milliseconds 1000 == 1 second)
		hideTimeout:		100,		// timeout before hiding the tip
		timeOnScreen:		0,			// timeout before automatically hiding the tip after showing it (set to > 0 in order to activate)
		showOn:			'hover',		// handler for showing the tip ('hover', 'focus', 'none') - use 'none' to trigger it manually
		liveEvents:		false,			// use live events
		alignTo:		'target',		// align/position the tip relative to ('cursor', 'target')
		alignX:			'center',		// horizontal alignment for the tip relative to the mouse cursor or the target element
										// ('right', 'center', 'left', 'inner-left', 'inner-right') - 'inner-*' matter if alignTo:'target'
		alignY:			'top',			// vertical alignment for the tip relative to the mouse cursor or the target element
										// ('bottom', 'center', 'top', 'inner-bottom', 'inner-top') - 'inner-*' matter if alignTo:'target'
		offsetX:		10,			// offset X pixels from the default position - doesn't matter if alignX:'center'
		offsetY:		0,				// offset Y pixels from the default position - doesn't matter if alignY:'center'
		keepInViewport:		true,		// reposition the tooltip if needed to make sure it always appears inside the viewport
		allowTipHover:		true,		// allow hovering the tip without hiding it onmouseout of the target - matters only if showOn:'hover'
		followCursor:		false,		// if the tip should follow the cursor - matters only if showOn:'hover' and alignTo:'cursor'
		fade: 			true,			// use fade animation
		slide: 			true,			// use slide animation
		slideOffset: 		8,			// slide animation offset
		showAniDuration: 	0,		// show animation duration - set to 0 if you don't want show animation
		hideAniDuration: 	0,		// hide animation duration - set to 0 if you don't want hide animation
		refreshAniDuration:	0			// refresh animation duration - set to 0 if you don't want animation when updating the tooltip asynchronously
};
function calcPos(tip,el,e) {
	var pos = {l: 0, t: 0, al: 0, arrow: ''},
		$win = $(window),
		win = {
			l: $win.scrollLeft(),
			t: $win.scrollTop(),
			w: $win.width(),
			h: $win.height()
		}, xL, xC, xR, yT, yC, yB;
	if (opts.alignTo == 'cursor') {
		xL = xC = xR = e.pageX;
		yT = yC = yB = e.pageY;
	} else { // opts.alignTo == 'target'
		var elmOffset = el.offset(),
			elm = {
				l: elmOffset.left,
				t: elmOffset.top,
				w: el.get(0).offsetWidth,
				h: el.get(0).offsetHeight
			};
		xL = elm.l + (opts.alignX != 'inner-right' ? 0 : elm.w);	// left edge
		xC = xL + Math.floor(elm.w / 2);				// h center
		xR = xL + (opts.alignX != 'inner-left' ? elm.w : 0);	// right edge
		yT = elm.t + (opts.alignY != 'inner-bottom' ? 0 : elm.h);	// top edge
		yC = yT + Math.floor(elm.h / 2);				// v center
		yB = yT + (opts.alignY != 'inner-top' ? elm.h : 0);	// bottom edge
	}
	tipOuterW = tip.outerWidth();
	tipOuterH = tip.outerHeight();

	// keep in viewport and calc arrow position
	switch (opts.alignX) {
		case 'right':
		case 'inner-left':
			pos.l = xR + opts.offsetX;
			if (opts.keepInViewport && pos.l + tipOuterW > win.l + win.w)
				pos.l = win.l + win.w - tipOuterW;
			if (opts.alignX == 'right' || opts.alignY == 'center')
				pos.arrow = 'left';
			break;
		case 'center':
			pos.l = xC - Math.floor(tipOuterW / 2);
			if (opts.keepInViewport) {
				if (pos.l + tipOuterW > win.l + win.w)
					pos.l = win.l + win.w - tipOuterW;
				else if (pos.l < win.l)
					pos.l = win.l;
			}
			break;
		default: // 'left' || 'inner-right'
			pos.l = xL - tipOuterW - opts.offsetX;
			if (opts.keepInViewport && pos.l < win.l)
				pos.l = win.l;
			if (opts.alignX == 'left' || opts.alignY == 'center')
				pos.arrow = 'right';
	}
	if (pos.l == 0 || (pos.l+tipOuterW) >= win.w) {
		pos.al = elmOffset.left +  Math.floor(elm.w / 2) - pos.l;
	}
	switch (opts.alignY) {
		case 'bottom':
		case 'inner-top':
			pos.t = yB + opts.offsetY;
			// 'left' and 'right' need priority for 'target'
			if (!pos.arrow || opts.alignTo == 'cursor')
				pos.arrow = 'top';
			if (opts.keepInViewport && pos.t + tipOuterH > win.t + win.h) {
				pos.t = yT - tipOuterH - opts.offsetY;
				if (pos.arrow == 'top')
					pos.arrow = 'bottom';
			}
			break;
		case 'center':
			pos.t = yC - Math.floor(tipOuterH / 2);
			if (opts.keepInViewport) {
				if (pos.t + tipOuterH > win.t + win.h)
					pos.t = win.t + win.h - tipOuterH;
				else if (pos.t < win.t)
					pos.t = win.t;
			}
			break;
		default: // 'top' || 'inner-bottom'
			pos.t = yT - tipOuterH - opts.offsetY;
			// 'left' and 'right' need priority for 'target'
			if (!pos.arrow || opts.alignTo == 'cursor')
				pos.arrow = 'bottom';
			if (opts.keepInViewport && pos.t < win.t) {
				pos.t = yB + opts.offsetY;
				if (pos.arrow == 'bottom')
					pos.arrow = 'top';
			}
	}
	return pos
}
function popTip(d,elm,e) {
	if (!$('#poshytip-css-' + opts.className)[0])
		$(['<style id="poshytip-css-',opts.className,'" type="text/css">',
			'div.',opts.className,'{position:absolute;top:0;left:0;}',
			'div.',opts.className,' table.tip-table, div.',opts.className,' table.tip-table td{margin:0;font-family:inherit;font-size:inherit;font-weight:inherit;font-style:inherit;font-variant:inherit;vertical-align:middle;}',
			'div.',opts.className,' td.tip-bg-image span{display:block;font:1px/1px sans-serif;height:',opts.bgImageFrameSize,'px;width:',opts.bgImageFrameSize,'px;overflow:hidden;}',
			'div.',opts.className,' td.tip-right{background-position:100% 0;}',
			'div.',opts.className,' td.tip-bottom{background-position:100% 100%;}',
			'div.',opts.className,' td.tip-left{background-position:0 100%;}',
			'div.',opts.className,' div.tip-inner{background-position:-',opts.bgImageFrameSize,'px -',opts.bgImageFrameSize,'px;}',
			'div.',opts.className,' div.tip-arrow{visibility:hidden;position:absolute;overflow:hidden;font:1px/1px sans-serif;}',
		'</style>'].join('')).appendTo('head');
	var a = $('<div id="J_FIXED" class="'+opts.className+'"><div class="tip-inner tip-bg-image"></div><div class="tip-arrow tip-arrow-top"></div></div>');
	$("#J_FIXED").length>0 || $("body").prepend(a);
	$(".tip-inner").empty().html(d);
	var tip = $("#J_FIXED"), pos = calcPos(tip,elm,e);
	if (pos.arrow) {
		$(".tip-arrow").attr("class", 'tip-arrow tip-arrow-' + pos.arrow);
		$(".tip-arrow").css({left: '50%', 'visibility': 'inherit'});
	}
	if (pos.al) {
		//console.log(pos);
		$(".tip-arrow").css({left: pos.al});
	}
	tip.css({left: pos.l, top: pos.t, 'visibility': 'inherit'});
}

$(function() {
	// 英文行
	$(".line_en").each(function (index, element) {
		$(this).mouseover(function (e) {
			e.stopPropagation();
			$this = $(this);
			var a = $this.find("a");
			if (0 < $(a).length) { return; }

			this.text = this.text || $this.text();
			var arr = this.text.split(" ");
			var words = [];
			var en = "";
			$(arr).each(function (i, w) {
				en += '<a class="word">' + w + '</a> ';
			});

			$this.html(en);
		});
	});
	// 中文行
	var $cnLines = $(".line_cn");
	for (var i = 0; i < $cnLines.length; i++) {
		var line = $cnLines[i];
		var $line = $(line);
		$line.click(function () {
			var $this = $(this);
			var title = $this.attr("title");
			if (title) {
				$this.text(title);
				$this.removeAttr("title");
				$this.css("background-color", "");
			} else {
				$this.attr("title", $this.text());
				$this.text("查看中文翻译");
			}
		});
	}
	
// 	$(document).on("click", ".word", function(e){
//     var elm = $(this), word = G.trimWord(elm.text());
//     $.ajax({
//         url: "https://www.shubang.net/dict/getword.php?word=" + word,
//         type: 'GET',
//         dataType: 'json',
//         crossDomain: true,
//         xhrFields: {
//             withCredentials: true
//         },
//         success: function(res) {
//             var msg = '';
//             if (1 == res.flag) {
//                 msg = '<div class="tipWord">' + word + '<a href="/dict/word/' + word + '" target="_blank">详细解释</a></div>';
//                 var wordInfo = res.data;
//                 if(wordInfo.am!=''){
//                     msg += '<div style="clear:both;">美：[<i>' + wordInfo.am + '</i>] <img class="audio" align="absmiddle" src="../public/skin/images/mp3.png"  onclick="G.playVoice(\'' + wordInfo.ammp3 + '\')"></div>';
//                 }
//                 if(wordInfo.en!=''){
//                     msg += '<div style="clear:both;">英：[<i>' + wordInfo.en + '</i>] <img class="audio" align="absmiddle" src="../public/skin/images/mp3.png"  onclick="G.playVoice(\'' + wordInfo.enmp3 + '\')"></div>';
//                 }
//                 msg += '<div style="clear:both;">' + G.replace(wordInfo.trans, "\n", "<br/>") + '</div>';
//                 // 自动播放
//                 console.log("自动播放-----",wordInfo.ammp3);
//                 if(wordInfo.en!=''){
//                     G.playVoice(wordInfo.ammp3);
//                 }
//             } else {
//                 msg = '<div class="tipWord">' + word + '</div><span style="color:red;">' + res.msg + '</span>';
//             }
//             msg = '<div class="tip">' + msg + '</div>';
//             popTip(msg, elm, e);
//         },
//         error: function(xhr, status, error) {
//             console.error('Error:', error);
//         }
//     });
// });
// 	var appid = '20210916000946027';
//     var key = 'Rvzi3t2kah8QpNkNFneP';
// 	$(document).on("click", ".word", function(e){
//     var elm = $(this), word = G.trimWord(elm.text());
//     var salt = (new Date).getTime();
//     var query = word;
//     var from = 'en';
//     var to = 'zh';
//     var str1 = appid + query + salt +key;
//     var sign = MD5(str1);
// $.ajax({
//     url: 'https://fanyi-api.baidu.com/api/trans/vip/translate',
//     type: 'get',
//     dataType: 'jsonp',
//     data: {
//         q: query,
//         appid: appid,
//         salt: salt,
//         from: from,
//         to: to,
//         sign: sign
//     },
//     success: function (res) {
//          var wordInfo = res.trans_result[0];
//           console.log("data___-"+JSON.stringify(wordInfo));
//           var wordHref=`https://www.youdao.com/m/result?word=${word}&lang=en`
//       var msg = '';
//       msg = '<div class="tipWord">' + word + '<a href="' + wordHref + '" target="_blank">详细解释</a></div>';
//      msg += '<div style="clear:both;">' + wordInfo.dst+ '</div>';
//      msg = '<div class="tip">' + msg + '</div>';
//      popTip(msg, elm, e);    
//     } ,
//     error: function(xhr, status, error) {
//             console.error('Error:', error);
//         }
// });
// });

// 	$(document).on("click", ".word", function(e) {
//     var elm = $(this), word = G.trimWord(elm.text());
//     var targetUrl = "https://www.shubang.net/dict/getword.php?word=" + encodeURIComponent(word);
//     // var proxyUrl = "https://api.allorigins.win/get?url=" + encodeURIComponent(targetUrl);
//     var proxyUrl = "https://api.codetabs.com/v1/proxy/?quest=" + encodeURIComponent(targetUrl);

//     $.ajax({
//         url: proxyUrl,
//         type: 'GET',
//         dataType: 'json',
//         success: function(res) {
//             var msg = '';
//             // AllOrigins返回的数据在`contents`字段里，需要解析
//             // var response = JSON.parse(res.contents);
//            var response = res;

//             var wordHref=`https://www.youdao.com/m/result?word=${word}&lang=en`
//             if (1 == response.flag) {
//                 msg = '<div class="tipWord">' + word + '<a href="' + wordHref + '" target="_blank">详细解释</a></div>';
//                 var wordInfo = response.data;
                
//                 if (wordInfo.am != '') {
//                     msg += '<div style="clear:both;">美：[<i>' + wordInfo.am + '</i>] <img class="audio" align="absmiddle" src="../public/skin/images/mp3.png" onclick="G.playVoice(\'' + wordInfo.ammp3 + '\')"></div>';
//                 }
//                 if (wordInfo.en != '') {
//                     msg += '<div style="clear:both;">英：[<i>' + wordInfo.en + '</i>] <img class="audio" align="absmiddle" src="../public/skin/images/mp3.png" onclick="G.playVoice(\'' + wordInfo.enmp3 + '\')"></div>';
//                 }
//                 msg += '<div style="clear:both;">' + G.replace(wordInfo.trans, "\n", "<br/>") + '</div>';
                
//                 // 自动播放
//                 console.log("自动播放-----", wordInfo.ammp3);
//                 if (wordInfo.en != '') {
//                     G.playVoice(wordInfo.ammp3);
//                 }
//             } else {
//                 msg = '<div class="tipWord">' + word + '</div><span style="color:red;">' + response.msg + '</span>';
//             }
//             msg = '<div class="tip">' + msg + '</div>';
//             popTip(msg, elm, e);
//         },
//         error: function(xhr, status, error) {
//             console.error('Error:', error);
//         }
//     });
// });
$(document).on("click", ".word", function(e) {
    var elm = $(this), word = G.trimWord(elm.text());
    var targetUrl = "https://www.shubang.net/dict/getword.php?word=" + encodeURIComponent(word);
    var proxyUrl = "https://api.codetabs.com/v1/proxy/?quest=" + encodeURIComponent(targetUrl);

    // 在点击时立即弹出一个空的提示框
    var msg = '<div class="tip"><div class="tipWord">' + word + '</div><div class="loading">查询中...</div></div>';
    popTip(msg, elm, e);

    // 发送 AJAX 请求
    $.ajax({
        url: proxyUrl,
        type: 'GET',
        dataType: 'json',
        success: function(res) {
            var msg = '';
            var response = res;
            var wordHref = `https://www.youdao.com/m/result?word=${word}&lang=en`;

            if (1 == response.flag) {
                var wordInfo = response.data;
                
                // 将wordInfo转换为JSON字符串并进行HTML转义
                var escapedWordInfo = encodeURIComponent(JSON.stringify(wordInfo));

                // 构建显示信息，现在包含完整的wordInfo数据
                msg = '<div class="tipWord">' + word + 
                      '<a href="' + wordHref + '" target="_blank" style="margin-left: 10px;">详细解释</a>' +
                      '<button class="add-to-wordbook" data-word="' + word + '" data-word-info="' + escapedWordInfo + '" style="margin-left: 10px;">加入到生词本</button></div>';

                // 添加发音和翻译
                if (wordInfo.am != '') {
                    msg += '<div style="clear:both;">美：[<i>' + wordInfo.am + '</i>] <img class="audio" align="absmiddle" src="../public/skin/images/mp3.png" onclick="G.playVoice(\'' + wordInfo.ammp3 + '\')"></div>';
                }
                if (wordInfo.en != '') {
                    msg += '<div style="clear:both;">英：[<i>' + wordInfo.en + '</i>] <img class="audio" align="absmiddle" src="../public/skin/images/mp3.png" onclick="G.playVoice(\'' + wordInfo.enmp3 + '\')"></div>';
                }
                msg += '<div style="clear:both;">' + G.replace(wordInfo.trans, "\n", "<br/>") + '</div>';

                // 自动播放
                if (wordInfo.ammp3) {
                    G.playVoice(wordInfo.ammp3);
                }
            } else {
                msg = '<div class="tipWord">' + word + '</div><span style="color:red;">' + response.msg + '</span>';
            }
            msg = '<div class="tip">' + msg + '</div>';
            
            // 更新提示框内容
            popTip(msg, elm, e);
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
            var errorMsg = '<div class="tipWord">' + word + '</div><span style="color:red;">请求失败，请稍后再试。</span>';
            popTip('<div class="tip">' + errorMsg + '</div>', elm, e);
        }
    });
});

// 处理"加入到生词本"按钮的点击事件
$(document).on("click", ".add-to-wordbook", function() {
    var word = $(this).data("word");
    var wordInfoStr = $(this).data("word-info");
    
    try {
        // 解码并解析wordInfo
        var wordInfo = JSON.parse(decodeURIComponent(wordInfoStr));
        
        // 将单词信息传递给 Flutter 端
		var json=JSON.stringify({
            word: word, 
            wordInfo: wordInfo
        });
		console.log("将单词和详细信息加入到生词本：", json);
        window.addToWordBook.postMessage(json);
    } catch (e) {
        console.error("解析单词信息时出错:", e);
    }
});



	$(document).on("mouseleave", "#J_FIXED", function(){
		$(".tipWord a").hide(), $("#J_FIXED").css('visibility', 'hidden');
	});
	$('body').click(function(e){
		var $this = $(e.target);
		if( $("#J_FIXED").length>0 && !$this.hasClass('audio')) {
			$(".tipWord a").hide(), $("#J_FIXED").css('visibility', 'hidden');
		}
	});

	// 监听滚动
	$(document).scroll(function() {
		var p = 'p1';
		$(".ap").each(function (index, element) {
			if( $(this).offset().top - $(window).scrollTop() > 0 )
				return false;
			p = $(this).attr('name')
		});
		p = p.substring(1);
		$.get("/book/j.php?ac=read&bookid=" + bookid + "&chapterid=" + chapterid + "&page=" + p);
	});

	// 定义全局变量G
	window.G = {};

	// 去除字符串前后指定字符串（注：参数中需使用\\s代替\s，\\|代替\|，但可以用 \t \n \r \f \v 或 \\t \\n \\r \\f \\v 这些）
	G.trim = function (str, s, attr) {
		s = s || "\\s"; // 默认去除字符串前后所有的空白，包括空格 \t \r \n等
		s = "(^" + s + "*)|(" + s + "*$)";
		// var regex = eval("/(^" + s + "*)|(" + s + "*$)/g"); // eval转换字符串形式的表达式
		attr = attr || "g"; // 属性 "g"、"i" 和 "m"，分别用于指定全局匹配、区分大小写的匹配和多行匹配
		var regex = new RegExp(s, attr);
		return str.replace(regex, "");
	};

	// 字符串替换（注：参数中需使用\\s代替\s，\\|代替\|，但可以用 \t \n \r \f \v 或 \\t \\n \\r \\f \\v 这些）
	G.replace = function (str, s1, s2, attr) {
		s1 = s1 || "\\s"; // 默认去除字符串前后所有的空白，包括空格 \t \r \n等
		s2 = s2 || "";
		attr = attr || "g"; // 属性 "g"、"i" 和 "m"，分别用于指定全局匹配、区分大小写的匹配和多行匹配
		var regex = new RegExp(s1, attr);
		return str.replace(regex, s2);
	};

	// 播放声音
	G.playVoice = function (voiceUrl) {
		voiceUrl='https://www.shubang.net'+voiceUrl;
		console.log("voice-url-----"+voiceUrl);
		var c = false;
		try {
			var b = document.createElement("audio");
			c = b.canPlayType && b.canPlayType("audio/mpeg") != "no" && b.canPlayType("audio/mpeg") != ""
		} catch(f) {}
		if (!c) {
			window.open(voiceUrl, "Sound", "menubar=no, status=no, scrollbars=no, menubar=no, width=200, height=100");
			return
		}
		if (window.audio != null && !window.audio.ended) {
			window.audio.pause();
			window.audio.currentTime = 0
		}
		window.audio = new Audio(voiceUrl);
		audio.addEventListener("error", function(a) {
			alert("Apologies, the sound is not available." + JSON.stringify(a));
		});
		audio.play();
	};

	// 过滤单词
	G.trimWord = function (word) {
		if (!word || "" == word && "string" == typeof (word)) { return; }

		// 匹配单词
		var m = word.match(/[a-z\-']+/ig);
		if (m && 0 < m.length) {
			var word = m[0];
			if (word) {
				// 去除前后符号
				word = G.trim(word, "[\\s\\-']");
			}
		}
		return word;
	};
});
var MD5 = function (string) {
  
    function RotateLeft(lValue, iShiftBits) {
        return (lValue<<iShiftBits) | (lValue>>>(32-iShiftBits));
    }
  
    function AddUnsigned(lX,lY) {
        var lX4,lY4,lX8,lY8,lResult;
        lX8 = (lX & 0x80000000);
        lY8 = (lY & 0x80000000);
        lX4 = (lX & 0x40000000);
        lY4 = (lY & 0x40000000);
        lResult = (lX & 0x3FFFFFFF)+(lY & 0x3FFFFFFF);
        if (lX4 & lY4) {
            return (lResult ^ 0x80000000 ^ lX8 ^ lY8);
        }
        if (lX4 | lY4) {
            if (lResult & 0x40000000) {
                return (lResult ^ 0xC0000000 ^ lX8 ^ lY8);
            } else {
                return (lResult ^ 0x40000000 ^ lX8 ^ lY8);
            }
        } else {
            return (lResult ^ lX8 ^ lY8);
        }
    }
  
    function F(x,y,z) { return (x & y) | ((~x) & z); }
    function G(x,y,z) { return (x & z) | (y & (~z)); }
    function H(x,y,z) { return (x ^ y ^ z); }
    function I(x,y,z) { return (y ^ (x | (~z))); }
  
    function FF(a,b,c,d,x,s,ac) {
        a = AddUnsigned(a, AddUnsigned(AddUnsigned(F(b, c, d), x), ac));
        return AddUnsigned(RotateLeft(a, s), b);
    };
  
    function GG(a,b,c,d,x,s,ac) {
        a = AddUnsigned(a, AddUnsigned(AddUnsigned(G(b, c, d), x), ac));
        return AddUnsigned(RotateLeft(a, s), b);
    };
  
    function HH(a,b,c,d,x,s,ac) {
        a = AddUnsigned(a, AddUnsigned(AddUnsigned(H(b, c, d), x), ac));
        return AddUnsigned(RotateLeft(a, s), b);
    };
  
    function II(a,b,c,d,x,s,ac) {
        a = AddUnsigned(a, AddUnsigned(AddUnsigned(I(b, c, d), x), ac));
        return AddUnsigned(RotateLeft(a, s), b);
    };
  
    function ConvertToWordArray(string) {
        var lWordCount;
        var lMessageLength = string.length;
        var lNumberOfWords_temp1=lMessageLength + 8;
        var lNumberOfWords_temp2=(lNumberOfWords_temp1-(lNumberOfWords_temp1 % 64))/64;
        var lNumberOfWords = (lNumberOfWords_temp2+1)*16;
        var lWordArray=Array(lNumberOfWords-1);
        var lBytePosition = 0;
        var lByteCount = 0;
        while ( lByteCount < lMessageLength ) {
            lWordCount = (lByteCount-(lByteCount % 4))/4;
            lBytePosition = (lByteCount % 4)*8;
            lWordArray[lWordCount] = (lWordArray[lWordCount] | (string.charCodeAt(lByteCount)<<lBytePosition));
            lByteCount++;
        }
        lWordCount = (lByteCount-(lByteCount % 4))/4;
        lBytePosition = (lByteCount % 4)*8;
        lWordArray[lWordCount] = lWordArray[lWordCount] | (0x80<<lBytePosition);
        lWordArray[lNumberOfWords-2] = lMessageLength<<3;
        lWordArray[lNumberOfWords-1] = lMessageLength>>>29;
        return lWordArray;
    };
  
    function WordToHex(lValue) {
        var WordToHexValue="",WordToHexValue_temp="",lByte,lCount;
        for (lCount = 0;lCount<=3;lCount++) {
            lByte = (lValue>>>(lCount*8)) & 255;
            WordToHexValue_temp = "0" + lByte.toString(16);
            WordToHexValue = WordToHexValue + WordToHexValue_temp.substr(WordToHexValue_temp.length-2,2);
        }
        return WordToHexValue;
    };
  
    function Utf8Encode(string) {
        string = string.replace(/\r\n/g,"\n");
        var utftext = "";
  
        for (var n = 0; n < string.length; n++) {
  
            var c = string.charCodeAt(n);
  
            if (c < 128) {
                utftext += String.fromCharCode(c);
            }
            else if((c > 127) && (c < 2048)) {
                utftext += String.fromCharCode((c >> 6) | 192);
                utftext += String.fromCharCode((c & 63) | 128);
            }
            else {
                utftext += String.fromCharCode((c >> 12) | 224);
                utftext += String.fromCharCode(((c >> 6) & 63) | 128);
                utftext += String.fromCharCode((c & 63) | 128);
            }
  
        }
  
        return utftext;
    };
  
    var x=Array();
    var k,AA,BB,CC,DD,a,b,c,d;
    var S11=7, S12=12, S13=17, S14=22;
    var S21=5, S22=9 , S23=14, S24=20;
    var S31=4, S32=11, S33=16, S34=23;
    var S41=6, S42=10, S43=15, S44=21;
  
    string = Utf8Encode(string);
  
    x = ConvertToWordArray(string);
  
    a = 0x67452301; b = 0xEFCDAB89; c = 0x98BADCFE; d = 0x10325476;
  
    for (k=0;k<x.length;k+=16) {
        AA=a; BB=b; CC=c; DD=d;
        a=FF(a,b,c,d,x[k+0], S11,0xD76AA478);
        d=FF(d,a,b,c,x[k+1], S12,0xE8C7B756);
        c=FF(c,d,a,b,x[k+2], S13,0x242070DB);
        b=FF(b,c,d,a,x[k+3], S14,0xC1BDCEEE);
        a=FF(a,b,c,d,x[k+4], S11,0xF57C0FAF);
        d=FF(d,a,b,c,x[k+5], S12,0x4787C62A);
        c=FF(c,d,a,b,x[k+6], S13,0xA8304613);
        b=FF(b,c,d,a,x[k+7], S14,0xFD469501);
        a=FF(a,b,c,d,x[k+8], S11,0x698098D8);
        d=FF(d,a,b,c,x[k+9], S12,0x8B44F7AF);
        c=FF(c,d,a,b,x[k+10],S13,0xFFFF5BB1);
        b=FF(b,c,d,a,x[k+11],S14,0x895CD7BE);
        a=FF(a,b,c,d,x[k+12],S11,0x6B901122);
        d=FF(d,a,b,c,x[k+13],S12,0xFD987193);
        c=FF(c,d,a,b,x[k+14],S13,0xA679438E);
        b=FF(b,c,d,a,x[k+15],S14,0x49B40821);
        a=GG(a,b,c,d,x[k+1], S21,0xF61E2562);
        d=GG(d,a,b,c,x[k+6], S22,0xC040B340);
        c=GG(c,d,a,b,x[k+11],S23,0x265E5A51);
        b=GG(b,c,d,a,x[k+0], S24,0xE9B6C7AA);
        a=GG(a,b,c,d,x[k+5], S21,0xD62F105D);
        d=GG(d,a,b,c,x[k+10],S22,0x2441453);
        c=GG(c,d,a,b,x[k+15],S23,0xD8A1E681);
        b=GG(b,c,d,a,x[k+4], S24,0xE7D3FBC8);
        a=GG(a,b,c,d,x[k+9], S21,0x21E1CDE6);
        d=GG(d,a,b,c,x[k+14],S22,0xC33707D6);
        c=GG(c,d,a,b,x[k+3], S23,0xF4D50D87);
        b=GG(b,c,d,a,x[k+8], S24,0x455A14ED);
        a=GG(a,b,c,d,x[k+13],S21,0xA9E3E905);
        d=GG(d,a,b,c,x[k+2], S22,0xFCEFA3F8);
        c=GG(c,d,a,b,x[k+7], S23,0x676F02D9);
        b=GG(b,c,d,a,x[k+12],S24,0x8D2A4C8A);
        a=HH(a,b,c,d,x[k+5], S31,0xFFFA3942);
        d=HH(d,a,b,c,x[k+8], S32,0x8771F681);
        c=HH(c,d,a,b,x[k+11],S33,0x6D9D6122);
        b=HH(b,c,d,a,x[k+14],S34,0xFDE5380C);
        a=HH(a,b,c,d,x[k+1], S31,0xA4BEEA44);
        d=HH(d,a,b,c,x[k+4], S32,0x4BDECFA9);
        c=HH(c,d,a,b,x[k+7], S33,0xF6BB4B60);
        b=HH(b,c,d,a,x[k+10],S34,0xBEBFBC70);
        a=HH(a,b,c,d,x[k+13],S31,0x289B7EC6);
        d=HH(d,a,b,c,x[k+0], S32,0xEAA127FA);
        c=HH(c,d,a,b,x[k+3], S33,0xD4EF3085);
        b=HH(b,c,d,a,x[k+6], S34,0x4881D05);
        a=HH(a,b,c,d,x[k+9], S31,0xD9D4D039);
        d=HH(d,a,b,c,x[k+12],S32,0xE6DB99E5);
        c=HH(c,d,a,b,x[k+15],S33,0x1FA27CF8);
        b=HH(b,c,d,a,x[k+2], S34,0xC4AC5665);
        a=II(a,b,c,d,x[k+0], S41,0xF4292244);
        d=II(d,a,b,c,x[k+7], S42,0x432AFF97);
        c=II(c,d,a,b,x[k+14],S43,0xAB9423A7);
        b=II(b,c,d,a,x[k+5], S44,0xFC93A039);
        a=II(a,b,c,d,x[k+12],S41,0x655B59C3);
        d=II(d,a,b,c,x[k+3], S42,0x8F0CCC92);
        c=II(c,d,a,b,x[k+10],S43,0xFFEFF47D);
        b=II(b,c,d,a,x[k+1], S44,0x85845DD1);
        a=II(a,b,c,d,x[k+8], S41,0x6FA87E4F);
        d=II(d,a,b,c,x[k+15],S42,0xFE2CE6E0);
        c=II(c,d,a,b,x[k+6], S43,0xA3014314);
        b=II(b,c,d,a,x[k+13],S44,0x4E0811A1);
        a=II(a,b,c,d,x[k+4], S41,0xF7537E82);
        d=II(d,a,b,c,x[k+11],S42,0xBD3AF235);
        c=II(c,d,a,b,x[k+2], S43,0x2AD7D2BB);
        b=II(b,c,d,a,x[k+9], S44,0xEB86D391);
        a=AddUnsigned(a,AA);
        b=AddUnsigned(b,BB);
        c=AddUnsigned(c,CC);
        d=AddUnsigned(d,DD);
    }
  
    var temp = WordToHex(a)+WordToHex(b)+WordToHex(c)+WordToHex(d);
  
    return temp.toLowerCase();
}