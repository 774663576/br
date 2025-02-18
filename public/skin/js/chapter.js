
var h5Port;
var appVersion;
window.addEventListener('message', function (event) {
	if (event.data == '__harmony_os_port__') {
		console.error("------__harmony_os_port__----" + event.data);
		if (event.ports[0] != null) {
			h5Port = event.ports[0]; //保存从ets侧发送过来的端口
			getAppVersion();
			h5Port.onmessage = function (event) {
				var result = JSON.parse(event.data);
				console.log('---从ets侧发送的消息-----' + result.method)
				switch (result.method) {
					case 'appVersion':
						appVersion = result.version;
						break;
				}
			}
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
function playAudio(audioUrl) {
	console.log("---playAudio---");
	var json = JSON.stringify({
		message: "playAudio",
		audioUrl: audioUrl
	});
	postMsgToEts(json);
}
function getAppVersion() {
	var json = JSON.stringify({
		message: "getAppVersion",
	});
	console.log('---getAppVersion-----' + json)
	postMsgToEts(json);
}
document.addEventListener("DOMContentLoaded", function () {
	if (window.getAppVersion) {
		window.getAppVersion.postMessage('');
	}
});


function receiveMessageFromFlutter(message) {
	console.log('---receiveMessageFromFlutter-----');
	switch (message.method) {
		case 'appVersion':
			appVersion = message.version;
			break;
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
document.addEventListener('contextmenu', function (event) {
	event.preventDefault();  // 阻止右键菜单
});
// 监听用户选择文本的事件

let selectionTimeout;
let currentSelectedText;
document.addEventListener('selectionchange', function () {
	// 清除上一次的定时器
	clearTimeout(selectionTimeout);

	// 设置一个延迟，等待用户停止选择后再处理
	selectionTimeout = setTimeout(function () {
		const selection = window.getSelection(); // 获取用户选中的文本
		let selectedText = selection.toString(); // 获取选中的文本

		if (selectedText) {
			selectedText = selectedText.replace(/[\u4e00-\u9fa5]/g, '');
			currentSelectedText = selectedText;
			console.log('---------' + selectedText);
			const range = selection.getRangeAt(0);
			const rect = range.getBoundingClientRect();
			console.log('----appVersion---' + appVersion);
			if (appVersion && appVersion >= 1500000) {
				showContextMenu(rect.left, rect.bottom);
			} else {
				if (h5Port) {
					var json = JSON.stringify({
						message: "showSelectedPopup",
						data: selectedText
					});
					postMsgToEts(json);
				}
				// 触发自定义的操作，比如向 Flutter 发送消息
				if (window.showSelectedPopup) {
					window.showSelectedPopup.postMessage(selectedText);
				}
			}
			// 清除选择区域
			// window.getSelection().removeAllRanges();
		}
	}, 1000);  // 1000ms 延迟，调整这个值根据需要
});


let contextMenu;

document.addEventListener('click', function (e) {
	if (contextMenu && !contextMenu.contains(e.target)) {
		hideContextMenu();
	}
});

// 通用的菜单项创建函数
function createMenuItem(iconSVG, text, handler) {
	const menuItem = document.createElement('li');
	menuItem.innerHTML = iconSVG + text;  // 使用自定义 SVG 图标和文字
	menuItem.addEventListener('click', function (e) {
		handler();
		hideContextMenu(); // 点击菜单项时隐藏上下文菜单
	});
	return menuItem;
}

// 创建上下文菜单
function createContextMenu(menuItems) {
	// 创建上下文菜单
	contextMenu = document.createElement('div');
	contextMenu.classList.add('context-menu');
	const ul = document.createElement('ul');

	// 动态创建菜单项
	menuItems.forEach(item => {
		const menuItem = createMenuItem(item.iconSVG, item.text, item.handler);
		ul.appendChild(menuItem);
	});

	contextMenu.appendChild(ul);
	document.body.appendChild(contextMenu);
}

// 显示上下文菜单
function showContextMenu(x, y) {
	if (!contextMenu) {
		createContextMenu([
			{ iconSVG: copyIconSVG, text: '复制', handler: handleCopy },
			{ iconSVG: translateIconSVG, text: '翻译', handler: handleTranslate },
			{ iconSVG: aiSvg, text: 'AI解析', handler: handleJieXi },
			{ iconSVG: noteIconSVG, text: '笔记', handler: handleNote }
		]);
	}

	contextMenu.style.display = 'block';

	// 获取滚动偏移量
	const scrollX = window.scrollX || window.pageXOffset;
	const scrollY = window.scrollY || window.pageYOffset;

	// 调整位置，考虑滚动偏移
	x += scrollX;
	y += scrollY;

	// 确保菜单不超出视窗
	const menuRect = contextMenu.getBoundingClientRect();
	const windowWidth = window.innerWidth;
	const windowHeight = window.innerHeight;

	if (x + menuRect.width > windowWidth + scrollX) {
		x = windowWidth + scrollX - menuRect.width - 5;
	}
	if (y + menuRect.height > windowHeight + scrollY) {
		y = y - menuRect.height - 10;
	}

	contextMenu.style.left = x + 'px';
	contextMenu.style.top = y + 'px';
}


// 隐藏上下文菜单
function hideContextMenu() {
	// if (contextMenu) {
	contextMenu.style.display = 'none';
	// }
}

// 复制
function handleCopy() {
	if (currentSelectedText) {
		if (h5Port) {
			var json = JSON.stringify({
				message: "copyText",
				data: currentSelectedText
			});
			postMsgToEts(json);
		}
		if (window.copyText) {
			window.copyText.postMessage(currentSelectedText);
		}
	}
	hideContextMenu();
}


// 翻译
function handleTranslate() {
	if (currentSelectedText) {
		if (h5Port) {
			var json = JSON.stringify({
				message: "translate",
				data: currentSelectedText
			});
			postMsgToEts(json);
		}
		if (window.translate) {
			window.translate.postMessage(currentSelectedText);
		}
	}
}
function handleJieXi() {
	if (currentSelectedText) {
		if (h5Port) {
			var json = JSON.stringify({
				message: "aiJieXi",
				data: currentSelectedText
			});
			postMsgToEts(json);
		}
		if (window.aiJieXi) {
			window.aiJieXi.postMessage(currentSelectedText);
		}
	}
}
// 保存笔记
function handleNote() {
	if (currentSelectedText) {
		if (h5Port) {
			var json = JSON.stringify({
				message: "note",
				data: currentSelectedText
			});
			postMsgToEts(json);
		}
		if (window.note) {
			window.note.postMessage(currentSelectedText);
		}
	}
}



const copyIconSVG = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="18" height="18">
    <path d="M833.33 767.96h-91.9c-21.73 0-39.34-17.6-39.34-39.34s17.62-39.34 39.34-39.34h91.9c8.82 0 15.98-7.18 15.98-15.98V193.8c0-8.8-7.17-15.98-15.98-15.98H353.84c-8.82 0-15.98 7.18-15.98 15.98v90.86c0 21.75-17.62 39.34-39.34 39.34s-39.34-17.6-39.34-39.34V193.8c0-52.21 42.47-94.67 94.67-94.67h479.49c52.19 0 94.67 42.45 94.67 94.67v479.49c-0.01 52.21-42.49 94.67-94.68 94.67z" fill="#ffffff"></path>
    <path d="M675.96 925.33H196.47c-52.19 0-94.67-42.45-94.67-94.67V351.17c0-52.21 42.47-94.67 94.67-94.67h479.49c52.19 0 94.67 42.45 94.67 94.67v479.49c-0.01 52.22-42.48 94.67-94.67 94.67zM196.47 335.19c-8.82 0-15.98 7.18-15.98 15.98v479.49c0 8.8 7.17 15.98 15.98 15.98h479.49c8.82 0 15.98-7.18 15.98-15.98V351.17c0-8.8-7.17-15.98-15.98-15.98H196.47z" fill="#ffffff"></path>
</svg>`;

const translateIconSVG = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="18" height="18">
    <path d="M896 452.256L772.256 576H851.2A341.344 341.344 0 0 1 512 874.656a340.64 340.64 0 0 1-300.8-179.2L136.544 736c74.656 138.656 217.6 224 375.456 224 221.856 0 403.2-168.544 424.544-384h83.2L896 452.256z" fill="#ffffff"></path>
    <path d="M322.144 710.4l78.944 29.856 46.944-121.6h128l44.8 121.6 78.944-29.856-136.544-369.056h-102.4L322.176 710.4zM512 448l32 85.344h-64L512 448z" fill="#ffffff"></path>
    <path d="M172.8 490.656A341.344 341.344 0 0 1 512 192c125.856 0 241.056 68.256 300.8 179.2l74.656-40.544a424.32 424.32 0 0 0-375.456-224c-221.856 0-403.2 168.544-424.544 384h-83.2L128 614.4l123.744-123.744H172.8z" fill="#ffffff"></path>
</svg>`;

const noteIconSVG = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="18" height="18">
    <path d="M770.816 351.61088l-155.0336-155.0336-413.47072 413.39904v155.0336h155.07456l413.42976-413.39904zM893.2352 229.21216l-81.07008 81.07008-155.0336-155.0336 81.05984-81.07008a41.17504 41.17504 0 0 1 58.24512 0l96.78848 96.78848a41.18528 41.18528 0 0 1 0.01024 58.24512zM49.14176 828.11904h919.26528v153.27232H49.14176z" fill="#ffffff"></path>
</svg>`;
const aiSvg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="18" height="18">
    <text x="50%" y="50%" font-weight="700" font-size="800" text-anchor="middle" alignment-baseline="central" fill="#ffffff">AI</text>
</svg>`;



















// function handleTextSelection(event) {
// 	const selection = window.getSelection(); // 获取用户选中的文本
// 	const selectedText = selection.toString(); // 获取选中的文本
// 	console.log('----handleTextSelection-----' + selectedText)

// 	if (selectedText) {
// 		console.log('----handleTextSelection--selectedText---' + selectedText)
// 		var json = JSON.stringify({
// 			message: "showSelectedPopup",
// 			data: selectedText
// 		});
// 		postMsgToEts(json);
// 		window.showSelectedPopup.postMessage("");
// 		window.getSelection().removeAllRanges();

// 	}
// }

// // 监听 touchend 和 mouseup 事件
// document.addEventListener('mouseup', handleTextSelection);
// document.addEventListener('touchend', handleTextSelection);







document.addEventListener("DOMContentLoaded", function () {
	const lines = document.querySelectorAll('.line_en');

	lines.forEach(function (line) {
		// 防止重复添加按钮
		if (line.querySelector('.audio-control')) return;

		const playButton = document.createElement('button');
		playButton.classList.add('audio-control');

		const playIcon = createHearIcon();
		playButton.innerHTML = playIcon;

		// 给每个 line 元素增加一个 audio 属性，用来保存对应的音频实例
		line.audio = null;

		// 添加播放按钮事件监听器
		playButton.addEventListener('click', function () {
			var text = line.textContent;
			if (appVersion && appVersion >= 1800000) {
				const audioUrl = `https://dict.youdao.com/dictvoice?type=2&audio=${encodeURIComponent(text)}&le=en`;
				console.log(audioUrl)
				playAudio(audioUrl);
				return;
			}

			text = text.replace('语速:', '')
			text = text.replace('1.0x', '')

			const activeTab = line.querySelector('.accent-tab.active');
			const accentType = activeTab.dataset.accent;
			const audioUrl = `https://dict.youdao.com/dictvoice?type=${accentType}&audio=${encodeURIComponent(text)}&le=en`;
			handleAudioControl(audioUrl, playButton, line);
		});

		if (appVersion && appVersion >= 1800000) {
			line.appendChild(playButton);
		} else {
			// 动态添加语速控制器
			const speedControl = createSpeedControl();
			line.appendChild(playButton);
			line.appendChild(speedControl);  // 将语速控制器添加到line下方
		}
	});
});
//创建听力图标
function createHearIcon() {
	return `
		<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg class="icon" width="24px" height="24.00px" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M352.8 576c-17.6-0.8-32 12.8-32.8 29.6v140c-0.8 18.4 13.6 33.6 31.2 34.4 18.4 0.8 33.6-13.6 34.4-31.2V608.8c0-18.4-14.4-32.8-32.8-32.8z m320 0c-17.6-0.8-32 12.8-32.8 29.6v140c-0.8 18.4 13.6 33.6 31.2 34.4 18.4 0.8 33.6-13.6 34.4-31.2V608.8c0-18.4-15.2-32.8-32.8-32.8z m-160 45.6c-17.6-0.8-32 12.8-32.8 29.6V700c-0.8 18.4 13.6 33.6 31.2 34.4s33.6-13.6 34.4-31.2v-48c0-19.2-14.4-33.6-32.8-33.6z" fill="#ff9b9b" /><path d="M842.4 484.8v-36c2.4-179.2-140.8-326.4-320-329.6h-9.6C328 119.2 183.2 264 183.2 448.8v36C77.6 491.2-4 581.6 2.4 688c5.6 101.6 89.6 180.8 191.2 181.6H216c17.6 0.8 32-12.8 32.8-29.6V448.8c0-150.4 113.6-264 264-264s264 113.6 264 264v388c-0.8 17.6 12.8 32 29.6 32.8h26.4c106.4-0.8 192-87.2 192-193.6-1.6-101.6-80.8-185.6-182.4-191.2z" fill="#ff9b9b" /></svg>
	`;
}
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
  <div class="speed-row">
            <span class="speed-lable">语速:</span>
            <input type="range" class="speed-slider" min="0.5" max="1" step="0.1" value="1">
            <span class="speed-value">1.0x</span>
        </div>
        <div class="accent-tabs">
		     <button class="accent-tab active" data-accent="0">美音</button>

            <button class="accent-tab" data-accent="1">英音</button>
        </div>
    `;

	const slider = speedControlDiv.querySelector('.speed-slider');
	const valueDisplay = speedControlDiv.querySelector('.speed-value');
	const accentTabs = speedControlDiv.querySelectorAll('.accent-tab');

	slider.addEventListener('input', function () {
		const rate = parseFloat(this.value);
		valueDisplay.textContent = rate.toFixed(1) + 'x';
		// 获取父元素.line_en
		const line = this.closest('.line_en');
		if (line && line.audio) {
			line.audio.playbackRate = rate;
		}
	});
	// 添加音标切换事件
	accentTabs.forEach(tab => {
		tab.addEventListener('click', function () {
			// 移除所有tab的active状态
			accentTabs.forEach(t => t.classList.remove('active'));
			// 添加当前点击tab的active状态
			this.classList.add('active');

			// 获取当前行元素
			const line = this.closest('.line_en');
			console.log('--audio---' + line.audio)
			// 如果有正在播放的音频，停止它
			if (line && line.audio) {
				line.audio.pause();
				line.audio.currentTime = 0;
				line.audio = null;
				// 重置播放按钮图标
				const playButton = line.querySelector('.audio-control');
				if (playButton) {
					playButton.innerHTML = createHearIcon();
				}
				// 隐藏语速控制器
				// const speedControl = line.querySelector('.speed-control');
				// if (speedControl) {
				// 	speedControl.style.display = 'none';
				// }
			}
		});
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
		console.log('---speedSlider---', speedSlider.value)
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
			playButton.innerHTML = createHearIcon();  // 恢复为播放图标
			// 隐藏语速控制器
			const speedControl = line.querySelector('.speed-control');
			if (speedControl) {
				speedControl.style.display = 'none'; // 隐藏语速控制器
			}
		});

		// 播放音频
		line.audio.play().catch(function (error) {
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


