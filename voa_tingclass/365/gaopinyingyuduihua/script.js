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

document.addEventListener("DOMContentLoaded", function () {
    // 获取内容区域
    const contentElement = document.querySelector('.Contentbox2');

    // 遍历文本节点进行处理
    function processNode(node) {
        if (node.nodeType === 3) { // 文本节点
            const text = node.textContent;
            // 检查是否包含英文内容，不再限制必须在特定样式的span内
            if (/[a-zA-Z]/.test(text)) {
                const wrapper = document.createElement('span');
                const words = text.split(/\b/);
                const fragment = document.createDocumentFragment();

                words.forEach(word => {
                    if (/^[a-zA-Z]+$/.test(word)) {
                        const span = document.createElement('span');
                        span.textContent = word;
                        span.className = 'clickable';
                        fragment.appendChild(span);
                    } else {
                        fragment.appendChild(document.createTextNode(word));
                    }
                });

                wrapper.appendChild(fragment);
                node.parentNode.replaceChild(wrapper, node);
            }
        } else if (node.nodeType === 1) { // 元素节点
            // 跳过已经处理过的节点和图片标签
            if (!node.classList.contains('clickable') && node.tagName !== 'IMG') {
                Array.from(node.childNodes).forEach(child => processNode(child));
            }
        }
    }

    // 处理内容区域
    if (contentElement) {
        // 延迟执行以确保DOM完全加载
        setTimeout(() => {
            try {
                processNode(contentElement);
                console.log('Content processing completed');
            } catch (error) {
                console.error('Error processing content:', error);
            }
        }, 100);
    }

    // 记录上一个点击的元素
    let lastClickedElement = null;

    // 添加点击事件处理
    document.addEventListener('click', function (e) {
        // 如果点击的是可点击单词
        if (e.target.classList.contains('clickable')) {
            // 移除上一个高亮单词的样式
            if (lastClickedElement) {
                lastClickedElement.classList.remove('active');
            }

            // 添加新的高亮样式
            e.target.classList.add('active');
            lastClickedElement = e.target;

            // 获取单词文本
            const word = e.target.textContent.trim();

            // 准备发送的消息
            var json = JSON.stringify({
                message: "showWordPopup",
                data: {
                    word: word,
                }
            });

            // 发送消息到不同的接收者
            postMsgToEts(json);
            if (window.showWordPopup) {
                window.showWordPopup.postMessage(json);
            }
        } else {
            // 如果点击其他区域，移除高亮
            if (lastClickedElement) {
                lastClickedElement.classList.remove('active');
                lastClickedElement = null;
            }
        }
    });

    // 添加错误处理
    window.onerror = function(msg, url, lineNo, columnNo, error) {
        console.error('Error: ' + msg + '\nURL: ' + url + '\nLine: ' + lineNo + '\nColumn: ' + columnNo + '\nError object: ' + JSON.stringify(error));
        return false;
    };

    // 添加调试日志
    console.log('Script loaded and initialized');
});