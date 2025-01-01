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

document.addEventListener('mouseup', handleTextSelection);
document.addEventListener('touchend', handleTextSelection);

// 处理文本选择
function handleTextSelection(event) {
    const selection = window.getSelection();
    const selectedText = selection.toString();

    if (selectedText) {
        var json = JSON.stringify({
            message: "showSelectedPopup",
            data: selectedText
        });
        postMsgToEts(json);
        window.getSelection().removeAllRanges();
    }
}

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