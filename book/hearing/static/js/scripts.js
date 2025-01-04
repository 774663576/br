var h5Port;
window.addEventListener('message', function (event) {
    if (event.data == '__harmony_os_port__') {
        if (event.ports[0] != null) {
            h5Port = event.ports[0];
        }
    }
});
function postMsgToEts(data) {
    if (h5Port) {
        h5Port.postMessage(data);
    } else {
        console.error("h5Port is null, Please initialize first");
    }
}


document.addEventListener('contextmenu', function (event) {
	event.preventDefault();  // 阻止右键菜单
});
// 监听用户选择文本的事件

let selectionTimeout;

document.addEventListener('selectionchange', function () {
	// 清除上一次的定时器
	clearTimeout(selectionTimeout);

	// 设置一个延迟，等待用户停止选择后再处理
	selectionTimeout = setTimeout(function () {
		const selection = window.getSelection(); // 获取用户选中的文本
		let selectedText = selection.toString(); // 获取选中的文本

		if (selectedText) {
			selectedText = selectedText.replace(/[\u4e00-\u9fa5]/g, '');
			console.log('---------' + selectedText);
			var json = JSON.stringify({
				message: "showSelectedPopup",
				data: selectedText
			});
			postMsgToEts(json);
			// 触发自定义的操作，比如向 Flutter 发送消息
			window.showSelectedPopup.postMessage(selectedText);

			// 清除选择区域
			window.getSelection().removeAllRanges();
		}
	}, 1000);  // 1000ms 延迟，调整这个值根据需要
});


document.addEventListener("DOMContentLoaded", function() {
    // 获取内容区域
    const contentElement = document.querySelector('.content');
    
    // 添加样式
    const style = document.createElement('style');
    style.textContent = `
        .clickable.active {
            color: #ff9b9b;
        }
    `;
    document.head.appendChild(style);
    
    // 遍历文本节点进行处理
    function processNode(node) {
        if (node.nodeType === 3) { // 文本节点
            const text = node.textContent;
            const wrapper = document.createElement('span');
            
            // 分词并添加span
            const words = text.split(/\b/); // 在词边界分割
            const fragment = document.createDocumentFragment();
            
            words.forEach(word => {
                if (/\w+/.test(word)) { // 如果是单词
                    const span = document.createElement('span');
                    span.textContent = word;
                    span.className = 'clickable';
                    span.style.cursor = 'pointer';
                    fragment.appendChild(span);
                } else {
                    fragment.appendChild(document.createTextNode(word));
                }
            });
            
            wrapper.appendChild(fragment);
            node.parentNode.replaceChild(wrapper, node);
        } else if (node.nodeType === 1) { // 元素节点
            Array.from(node.childNodes).forEach(child => processNode(child));
        }
    }

    // 处理内容区域
    if (contentElement) {
        processNode(contentElement);
    }
    
    // 记录上一个点击的元素
    let lastClickedElement = null;
    
    // 添加点击事件处理
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('clickable')) {
            // 移除上一个高亮
            if (lastClickedElement) {
                lastClickedElement.classList.remove('active');
            }
            
            // 高亮当前点击的单词
            e.target.classList.add('active');
            lastClickedElement = e.target;
            
            const word = e.target.textContent.trim();
 
            var json = JSON.stringify({
                message: "showWordPopup",
                data: {
                    word: word,
                }
            });
            postMsgToEts(json);
            window.showWordPopup.postMessage(json);
        } else {
            // 点击其他地方时移除高亮
            if (lastClickedElement) {
                lastClickedElement.classList.remove('active');
                lastClickedElement = null;
            }
        }
    });
});