document.addEventListener("DOMContentLoaded", function () {
    const contentElement = document.querySelector('.article-content');

    function processContent() {
        // 找到第一张图片
        const firstImg = contentElement.querySelector('img');
        if (!firstImg) return;

        // 获取所有段落
        const paragraphs = contentElement.getElementsByTagName('p');
        let foundImage = false;

        // 遍历所有段落
        for (let p of paragraphs) {
            // 检查是否已经遇到了图片
            if (!foundImage) {
                if (p.contains(firstImg)) {
                    foundImage = true;
                }
                continue;
            }

            // 处理图片后的段落
            const textNodes = [];
            const walk = document.createTreeWalker(p, NodeFilter.SHOW_TEXT);
            let node;
            while (node = walk.nextNode()) {
                textNodes.push(node);
            }

            textNodes.forEach(textNode => {
                const text = textNode.textContent;
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
                    textNode.parentNode.replaceChild(wrapper, textNode);
                }
            });
        }
    }

    // 处理内容区域
    if (contentElement) {
        setTimeout(() => {
            try {
                processContent();
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