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
    const contentElement = document.querySelector('.article-content');

    function processNode(node) {
        if (node.nodeType === 3) { // 文本节点
            // 检查父节点是否是第一个p标签
            if (node.parentElement.tagName === 'P' && 
                node.parentElement === contentElement.querySelector('p:first-child')) {
                return; // 跳过第一个p标签的处理
            }

            const text = node.textContent;
            if (/[a-zA-Z]/.test(text)) {
                const wrapper = document.createElement('span');
                const words = text.split(/(\s+|[.,!?;])/);
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
            // 跳过第一个p标签
            if (node.tagName === 'P' && node === contentElement.querySelector('p:first-child')) {
                return;
            }
            
            if (!node.classList.contains('clickable') && node.tagName !== 'IMG') {
                Array.from(node.childNodes).forEach(child => processNode(child));
            }
        }
    }

    // 处理内容区域
    if (contentElement) {
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
        if (e.target.classList.contains('clickable')) {
            if (lastClickedElement) {
                lastClickedElement.classList.remove('active');
            }

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
            if (window.showWordPopup) {
                window.showWordPopup.postMessage(json);
            }
        } else {
            if (lastClickedElement) {
                lastClickedElement.classList.remove('active');
                lastClickedElement = null;
            }
        }
    });
});