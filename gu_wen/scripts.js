
document.addEventListener('DOMContentLoaded', function() {
    // 获取所有诗节的英文翻译区域
    document.querySelectorAll('.poem-section').forEach(function(section) {
        var englishText = section.querySelector('.english-text');
        
        // 动态创建按钮
        var button = document.createElement('span');
        button.className = 'show-translation';
        button.textContent = '查看英文翻译';
        
        // 按钮点击事件：显示/隐藏英文翻译
        button.addEventListener('click', function() {
            if (englishText.style.display === "none" || englishText.style.display === "") {
                englishText.style.display = "block";  // 确保翻译显示
                button.textContent = '隐藏英文翻译';
            } else {
                englishText.style.display = "none";
                button.textContent = '查看英文翻译';
            }
        });

        // 将按钮添加到每个诗节的末尾
        section.appendChild(button);
    });
});
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

document.addEventListener("DOMContentLoaded", function() {
    // 获取所有的英文文本内容
    const englishTextElements = document.querySelectorAll('.english-text p');

    // 遍历每个段落
    englishTextElements.forEach(function(paragraph) {
        // 获取每个段落的文本内容
        const text = paragraph.innerHTML;

        // 使用正则表达式将单词包裹在 <span> 标签中，并添加点击事件
        const modifiedText = text.replace(/\b\w+\b/g, function(match) {
            return `<span class="clickable" data-word="${match}">${match}</span>`;
        });

        // 更新段落内容
        paragraph.innerHTML = modifiedText;
    });

    // 为每个单词添加点击事件
    document.body.addEventListener('click', function(event) {
        if (event.target && event.target.classList.contains('clickable')) {
           const wordText = event.target.innerText || event.target.textContent;  // 获取点击的单词
           var json = JSON.stringify({
            message: "showWordPopup",
            data: {
                word: wordText,
                x: 0,
                y: 0
            }
        });
        console.log("+++++showWordPopup-----", json);
        postMsgToEts(json);
        window.showWordPopup.postMessage(json);
        }
    });
});

 // 监听用户选择文本的事件
    function handleTextSelection(event) {
        const selection = window.getSelection(); // 获取用户选中的文本
        const selectedText = selection.toString(); // 获取选中的文本

        if (selectedText) {
   console.log('---------'+selectedText)
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




