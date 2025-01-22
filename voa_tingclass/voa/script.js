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
            // 如果文本节点在span标签内且包含样式信息，则保留原有结构
            if (node.parentNode.tagName === 'SPAN' &&
                node.parentNode.getAttribute('style')?.includes('font-size')) {
                if (/^[a-zA-Z\s.,!?'"]+$/.test(text.trim())) { // 英文内容
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
            }
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