
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
// 处理单词点击
document.addEventListener("DOMContentLoaded", function () {
    const englishTextElements = document.querySelectorAll('.line_en');

    englishTextElements.forEach(function (paragraph) {
        const text = paragraph.innerHTML;
        const modifiedText = text.replace(/\b\w+\b/g, function (match) {
            return `<span class="clickable" data-word="${match}">${match}</span>`;
        });
        paragraph.innerHTML = modifiedText;
    });

    document.body.addEventListener('click', function (event) {
        // 先移除之前的高亮
        const highlighted = document.querySelector('.wordClickHighLight');
        if (highlighted) {
            highlighted.classList.remove('wordClickHighLight');
        }

        // 如果点击的是可点击单词
        if (event.target && event.target.classList.contains('clickable')) {
            const wordText = event.target.innerText || event.target.textContent;

            // 给选中的单词添加高亮样式
            event.target.classList.add('wordClickHighLight');
            
            var json = JSON.stringify({
                message: "showWordPopup",
                data: {
                    word: wordText,
                    x: 0,
                    y: 0
                }
            });
            postMsgToEts(json);
            window.showWordPopup.postMessage(json);
        }
    });
});


$(function () {
	
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







document.addEventListener("DOMContentLoaded", function () {
	const lines = document.querySelectorAll('.line_en');

	lines.forEach(function (line) {
		// 防止重复添加按钮
		if (line.querySelector('.audio-control')) return;

		const playButton = document.createElement('button');
		playButton.classList.add('audio-control');

		const playIcon = createPlayIcon();
		playButton.innerHTML = playIcon;

		// 给每个 line 元素增加一个 audio 属性，用来保存对应的音频实例
		line.audio = null;

		// 添加播放按钮事件监听器
		playButton.addEventListener('click', function () {
			const audioUrl = `https://dict.youdao.com/dictvoice?audio=${line.textContent}&le=en`;
			handleAudioControl(audioUrl, playButton, line);
		});

		// 动态添加语速控制器
		const speedControl = createSpeedControl();
		line.appendChild(playButton);
		line.appendChild(speedControl);  // 将语速控制器添加到line下方

		// 将播放按钮和语速控制器放置在一起
	});
});

// 创建播放图标
function createPlayIcon() {
	return `
		<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
			<polygon points="5 3 19 12 5 21 5 3"></polygon>
		</svg>
	`;
}

// 创建暂停图标
function createPauseIcon() {
	return `
		<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
			<rect x="6" y="4" width="4" height="16"></rect>
			<rect x="14" y="4" width="4" height="16"></rect>
		</svg>
	`;
}

// 创建加载图标
function createLoadingIcon() {
	return `
		<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="animate-spin">
			<circle cx="12" cy="12" r="10" opacity="0.25" />
			<path d="M12 2a10 10 0 0 1 10 10" stroke="currentColor" stroke-width="4" />
		</svg>
	`;
}

// 创建语速控制器
function createSpeedControl() {
    const speedControlDiv = document.createElement('div');
    speedControlDiv.classList.add('speed-control');
    speedControlDiv.innerHTML = `
        <span class="speed-lable">语速:</span>
        <input type="range" class="speed-slider" min="0.5" max="1" step="0.1" value="1">
        <span class="speed-value">1.0x</span>
    `;

    const slider = speedControlDiv.querySelector('.speed-slider');
    const valueDisplay = speedControlDiv.querySelector('.speed-value');

    slider.addEventListener('input', function () {
        const rate = parseFloat(this.value);
        valueDisplay.textContent = rate.toFixed(1) + 'x';
        // 获取父元素.line_en
        const line = this.closest('.line_en');
        if (line && line.audio) {
            line.audio.playbackRate = rate;
        }
    });

    return speedControlDiv;
}

// 停止所有正在播放的音频
function stopAllAudioExcept(currentLine) {
	const allLines = document.querySelectorAll('.line_en');
	allLines.forEach(function (line) {
		if (line !== currentLine && line.audio && !line.audio.paused) {
			line.audio.pause();
			line.audio.currentTime = 0; // 你可以选择注释掉这一行，保持播放进度
			const playButton = line.querySelector('.audio-control');
			if (playButton) {
				playButton.innerHTML = createPlayIcon(); // 恢复为播放图标
			}
			// 隐藏语速控制器
			const speedControl = line.querySelector('.speed-control');
			if (speedControl) {
				speedControl.style.display = 'none'; // 隐藏语速控制器
			}
		}
	});
}

// 处理音频控制
function handleAudioControl(audioUrl, playButton, line) {
	// 如果当前音频还没创建，或者已经暂停，则播放
	if (!line.audio) {
		// 插入播放的旋转加载图标
		playButton.innerHTML = createLoadingIcon();

		// 使用 Audio 对象播放在线音频
		line.audio = new Audio(audioUrl);

		// 设置音频的初始语速
		const speedSlider = line.querySelector('.speed-slider');
		console.log('---speedSlider---',speedSlider.value)
		line.audio.playbackRate = parseFloat(speedSlider.value);

		// 音频播放开始时更新按钮图标
		line.audio.addEventListener('play', function () {
			playButton.innerHTML = createPauseIcon();  // 暂停图标
			// 显示语速控制器
			const speedControl = line.querySelector('.speed-control');
			if (speedControl) {
				speedControl.style.display = 'flex'; // 显示语速控制器
			}
		});

		// 音频播放结束时更新按钮图标
		line.audio.addEventListener('ended', function () {
			playButton.innerHTML = createPlayIcon();  // 恢复为播放图标
			// 隐藏语速控制器
			const speedControl = line.querySelector('.speed-control');
			if (speedControl) {
				speedControl.style.display = 'none'; // 隐藏语速控制器
			}
		});

		// 播放音频
		line.audio.play().catch(function(error) {
			console.error("Audio playback failed:", error);
			playButton.innerHTML = createPlayIcon(); // 恢复播放图标
		});
	} else {
		// 如果音频已经在播放，点击则暂停
		if (!line.audio.paused) {
			line.audio.pause();
			playButton.innerHTML = createPlayIcon(); // 恢复播放图标
			// 隐藏语速控制器
			const speedControl = line.querySelector('.speed-control');
			if (speedControl) {
				speedControl.style.display = 'none'; // 隐藏语速控制器
			}
		} else {
			// 音频已暂停，继续播放
			line.audio.play();
			playButton.innerHTML = createPauseIcon(); // 暂停图标
			// 显示语速控制器
			const speedControl = line.querySelector('.speed-control');
			if (speedControl) {
				speedControl.style.display = 'flex'; // 显示语速控制器
			}
		}
	}

	// 在播放新音频之前，暂停其他所有音频
	stopAllAudioExcept(line);
}





// document.addEventListener("DOMContentLoaded", function () {
// 	const lines = document.querySelectorAll('.line_en');

// 	lines.forEach(function (line) {
// 		if (line.querySelector('.audio-control')) return;  // 防止重复添加按钮

// 		const playButton = document.createElement('button');
// 		playButton.classList.add('audio-control');

// 		const svg = `
// 			<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
// 				<polygon points="5 3 19 12 5 21 5 3"></polygon>
// 			</svg>
// 		`;
// 		playButton.innerHTML = svg;

// 		playButton.addEventListener('click', function () {
// 			speakText(line.textContent, playButton, line);
// 		});

// 		// 将按钮放在 line 元素的末尾
// 		line.appendChild(playButton);
// 	});
// });

// function speakText(text, playButton, line) {
// 	const words = text.split(' ');

// 	// 保存按钮位置，防止更新 innerHTML 时丢失
// 	const buttonContainer = playButton.parentNode;
// 	line.innerHTML = words.map(word => {
// 		return `<span class="word">${word}</span>`;
// 	}).join(' ');

// 	// 重新插入按钮
// 	buttonContainer.appendChild(playButton);

// 	if (responsiveVoice.isPlaying()) {
// 		console.log("---------pause---------");
// 		responsiveVoice.cancel();
// 		const svg = `
// 			<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
// 				<polygon points="5 3 19 12 5 21 5 3"></polygon>
// 			</svg>
// 		`;
// 		playButton.innerHTML = svg;
// 		return;
// 	}

// 	const loadingSvg = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="animate-spin">
//             <circle cx="12" cy="12" r="10" opacity="0.25" />
//             <path d="M12 2a10 10 0 0 1 10 10" stroke="currentColor" stroke-width="4" />
//         </svg>`;
// 	playButton.innerHTML = loadingSvg;

// 	let currentWordIndex = 0;
// 	responsiveVoice.speak(text, "US English Female", {
// 		rate: 1, // 语速
// 		onstart: function () {
// 			playButton.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
//             <rect x="6" y="4" width="4" height="16"></rect>
//             <rect x="14" y="4" width="4" height="16"></rect>
//         </svg>`; // 更新按钮图标为暂停样式
// 		},
// 		onend: function () {
// 			console.log("---------end------------------");
// 			playButton.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
//             <polygon points="5 3 19 12 5 21 5 3"></polygon>
//         </svg>`; // 更新按钮图标为播放样式
// 			resetHighlight();
// 		},

// 		onboundary: function(event) {
// 			console.log("---------boundary------------------", event);
// 			if (event.name === "word") {
// 				// 高亮当前单词
// 				highlightWord(currentWordIndex);
// 				currentWordIndex++;
// 			}
// 		}
// 	});

// 	function highlightWord(index) {
// 		console.log("---------highlightWord---------", index);
// 		const wordSpans = line.querySelectorAll('.word');
// 		if (wordSpans[index]) {
// 			resetHighlight();
// 			wordSpans[index].classList.add('highlight');
// 		}
// 	}

// 	function resetHighlight() {
// 		const wordSpans = line.querySelectorAll('.word');
// 		wordSpans.forEach(span => span.classList.remove('highlight'));
// 	}
// }







// document.addEventListener("DOMContentLoaded", function () {
// 	const lines = document.querySelectorAll('.line_en');

// 	lines.forEach(function (line) {
// 		if (line.querySelector('.audio-control')) return;  // 防止重复添加按钮

// 		const playButton = document.createElement('button');
// 		playButton.classList.add('audio-control');

// 		const svg = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
//                         <polygon points="5 3 19 12 5 21 5 3"></polygon>
//                     </svg>`;
// 		playButton.innerHTML = svg;

// 		playButton.addEventListener('click', function () {
// 			if (window.speechSynthesis.speaking) {
// 				// 如果语音正在播放，暂停
// 				window.speechSynthesis.cancel();
// 				playButton.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
// 				<polygon points="5 3 19 12 5 21 5 3"></polygon>
// 			</svg>`;
// 				return;
// 			}
// 			const loadingSvg = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="animate-spin">
//             <circle cx="12" cy="12" r="10" opacity="0.25" />
//             <path d="M12 2a10 10 0 0 1 10 10" stroke="currentColor" stroke-width="4" />
//         </svg>`;
// 			playButton.innerHTML = loadingSvg;
// 			speakText(line.textContent, playButton, line);
// 		});

// 		// 将按钮放在 line 元素的末尾
// 		line.appendChild(playButton);
// 	});

// 	function speakText(text, playButton, line) {
// 		const words = text.split(' ');

// 		// 保存按钮位置，防止更新 innerHTML 时丢失
// 		const buttonContainer = playButton.parentNode;

// 		// 用 <span> 包裹每个单词
// 		line.innerHTML = words.map(word => `<span class="word">${word}</span>`).join(' ');

// 		// 重新插入按钮
// 		buttonContainer.appendChild(playButton);

// 		const utterance = new SpeechSynthesisUtterance(text);
// 		utterance.rate = 1; // 语速
// 		utterance.lang = 'en-US'; // 语音语言

// 		let currentWordIndex = 0;

// 		utterance.onstart = function () {
// 			playButton.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
//                                         <rect x="6" y="4" width="4" height="16"></rect>
//                                         <rect x="14" y="4" width="4" height="16"></rect>
//                                     </svg>`; // 播放中图标
// 		};

// 		utterance.onend = function () {
// 			playButton.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
//                                         <polygon points="5 3 19 12 5 21 5 3"></polygon>
//                                     </svg>`; // 播放完毕图标
// 			resetHighlight();
// 		};

// 		utterance.onboundary = function (event) {
// 			if (event.name === "word") {
// 				highlightWord(currentWordIndex);
// 				currentWordIndex++;
// 			}
// 		};

// 		// 开始语音播放
// 		window.speechSynthesis.speak(utterance);

// 		function highlightWord(index) {
// 			const wordSpans = line.querySelectorAll('.word');
// 			if (wordSpans[index]) {
// 				resetHighlight();
// 				wordSpans[index].classList.add('highlight');
// 			}
// 		}

// 		function resetHighlight() {
// 			const wordSpans = line.querySelectorAll('.word');
// 			wordSpans.forEach(span => span.classList.remove('highlight'));
// 		}
// 	}
// });


