var h5Port;

window.addEventListener('message', function (event) {
	if (event.data == '__harmony_os_port__') {
		console.error("------__harmony_os_port__----" + event.data);

		if (event.ports[0] != null) {
			h5Port = event.ports[0]; //保存从ets侧发送过来的端口
		}
	}
})
function postMsgToEts(data) {
	if (h5Port) {
		h5Port.postMessage(data);
	} else {
		console.error("h5Port is null, Please initialize first");
	}
}


$(function () {
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


	$(document).on("click", ".word", function (e) {
		var elm = $(this), word = trimWord(elm.text());

		// 获取点击的位置
		var offset = $(this).offset();
		var x = offset.left;
		var y = offset.top;
		var json = JSON.stringify({
			message: "showWordPopup",
			data: {
				word: word,
				x: x,
				y: y
			}
		});
		console.log("+++++showWordPopup-----", json);
		postMsgToEts(json);
		window.showWordPopup.postMessage(json);
	});

	// 获取页面中的所有 <a> 标签
	const links = document.querySelectorAll('.pagebar a');

	let prevLink = null;
	let nextLink = null;

	// 遍历所有链接，查找对应的“上一章”和“下一章”链接
	links.forEach(link => {
		if (link.textContent.trim() === '上一章') {
			prevLink = link;  // 找到“上一章”链接
		}
		if (link.textContent.trim() === '下一章') {
			nextLink = link;  // 找到“下一章”链接
		}
	});

	console.log("--------prevLink:---------", prevLink);
	console.log("--------nextLink:---------", nextLink);
	// 判断链接是否存在
	if (prevLink) {
		prevLink.addEventListener('click', function (event) {
			event.preventDefault(); // 阻止默认的链接跳转行为
			preChapter();  // 执行 preChapter 方法
		});
	}

	if (nextLink) {
		nextLink.addEventListener('click', function (event) {
			event.preventDefault(); // 阻止默认的链接跳转行为
			nextChapter();  // 执行 nextChapter 方法
		});
	}

	function preChapter() {
		console.log("---preChapter---");
		var json = JSON.stringify({
			message: "preChapter"
		});
		postMsgToEts(json);
		window.preChapter.postMessage("");
	}


	function nextChapter() {
		console.log("---nextChapter---");
		var json = JSON.stringify({
			message: "nextChapter"
		});
		postMsgToEts(json);
		window.nextChapter.postMessage("");

	}



	// 定义全局变量G
	window.G = {};



	function trim(str, s, attr) {
		s = s || "\\s"; // 默认去除字符串前后所有的空白，包括空格 \t \r \n等
		s = "(^" + s + "*)|(" + s + "*$)";
		// var regex = eval("/(^" + s + "*)|(" + s + "*$)/g"); // eval转换字符串形式的表达式
		attr = attr || "g"; // 属性 "g"、"i" 和 "m"，分别用于指定全局匹配、区分大小写的匹配和多行匹配
		var regex = new RegExp(s, attr);
		return str.replace(regex, "");
	};

	function trimWord(word) {
		if (!word || "" == word && "string" == typeof (word)) { return; }

		// 匹配单词
		var m = word.match(/[a-z\-']+/ig);
		if (m && 0 < m.length) {
			var word = m[0];
			if (word) {
				// 去除前后符号
				word = trim(word, "[\\s\\-']");
			}
		}
		return word;
	};
});
// 监听用户选择文本的事件
function handleTextSelection(event) {
	const selection = window.getSelection(); // 获取用户选中的文本
	const selectedText = selection.toString(); // 获取选中的文本

	if (selectedText) {
		console.log('---------' + selectedText)
		var json = JSON.stringify({
			message: "showSelectedPopup",
			data: selectedText
		});
		postMsgToEts(json);
		window.getSelection().removeAllRanges();

	}
}

// 监听 touchend 和 mouseup 事件
document.addEventListener('mouseup', handleTextSelection);
document.addEventListener('touchend', handleTextSelection);