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
// 处理单词点击
document.addEventListener("DOMContentLoaded", function () {
    const englishTextElements = document.querySelectorAll('.english-text p');

    englishTextElements.forEach(function (paragraph) {
        const text = paragraph.innerHTML;
        const modifiedText = text.replace(/\b\w+\b/g, function (match) {
            return `<span class="clickable" data-word="${match}">${match}</span>`;
        });
        paragraph.innerHTML = modifiedText;
    });

    document.body.addEventListener('click', function (event) {
        if (event.target && event.target.classList.contains('clickable')) {
            const wordText = event.target.innerText || event.target.textContent;
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







document.addEventListener('DOMContentLoaded', function () {
    let currentAudioButton = null;
    let currentAudio = null;

    // 初始化所有语速控制器
    document.querySelectorAll('.speed-slider').forEach(slider => {
        const valueDisplay = slider.nextElementSibling;

        slider.addEventListener('input', function () {
            const rate = parseFloat(this.value);
            valueDisplay.textContent = rate.toFixed(1) + 'x';

            // 如果当前正在播放，实时更新语速
            if (currentAudio && !currentAudio.paused) {
                currentAudio.playbackRate = rate;
            }
        });
    });

    function stopCurrentAudio() {
        if (currentAudio && !currentAudio.paused) {
            currentAudio.pause();
            if (currentAudioButton) {
                currentAudioButton.innerHTML = createPlayIcon();  // 恢复为播放图标
            }
        }
    }

    function createPlayIcon() {
        return `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
            </svg>
        `;
    }

    function createPauseIcon() {
        return `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="6" y="4" width="4" height="16"></rect>
                <rect x="14" y="4" width="4" height="16"></rect>
            </svg>
        `;
    }

    document.querySelectorAll('.translation-toggle').forEach(button => {
        button.addEventListener('click', function () {
            const section = this.closest('.english-container');
            const englishText = section.querySelector('.english-text');
            const audioButton = section.querySelector('.audio-control');
            const speedControl = section.querySelector('.speed-control');
            const isHidden = englishText.style.display === 'none' || englishText.style.display === '';

            englishText.style.display = isHidden ? 'block' : 'none';
            audioButton.style.display = isHidden ? 'block' : 'none';
            speedControl.style.display = isHidden ? 'flex' : 'none';
            this.textContent = isHidden ? '隐藏英文翻译' : '显示英文翻译';

            if (!isHidden) {
                stopCurrentAudio();
            }
        });
    });

    document.querySelectorAll('.audio-control').forEach(button => {
        button.addEventListener('click', function () {
            const section = this.closest('.english-text');
            const englishText = section.getAttribute('data-text');
            const container = this.closest('.english-container');
            const speedSlider = container.querySelector('.speed-slider');

            // 如果当前语音已经播放且是当前按钮，则暂停
            if (currentAudio && !currentAudio.paused && currentAudioButton === this) {
                currentAudio.pause();
                currentAudioButton.innerHTML = createPlayIcon();
                return;
            }

            // 停止之前的语音播放
            stopCurrentAudio();
            currentAudioButton = this;
            currentAudioButton.innerHTML = createPauseIcon();  // 显示暂停图标

            // 如果没有现有的音频，则创建新的 Audio
            if (!currentAudio) {
                currentAudio = new Audio();
                currentAudio.src = `https://dict.youdao.com/dictvoice?audio=${encodeURIComponent(englishText)}&le=en`;
                currentAudio.playbackRate = parseFloat(speedSlider.value);  // 语速控制

                // 播放开始时的回调
                currentAudio.addEventListener('play', function () {
                    currentAudioButton.innerHTML = createPauseIcon();  // 更新为暂停图标
                });

                // 播放结束时的回调
                currentAudio.addEventListener('ended', function () {
                    currentAudioButton.innerHTML = createPlayIcon();  // 恢复为播放图标
                    currentAudio = null;
                    currentAudioButton = null;
                });

                // 错误处理
                currentAudio.addEventListener('error', function () {
                    console.error('音频加载出错');
                    currentAudioButton.innerHTML = createPlayIcon();  // 恢复为播放图标
                });

                currentAudio.play();
            } else {
                // 如果已有音频实例，继续播放
                currentAudio.play();
            }
        });
    });

    // 页面切换时停止播放
    document.addEventListener('visibilitychange', function () {
        if (document.hidden) {
            stopCurrentAudio();
        }
    });
});













// document.addEventListener('DOMContentLoaded', function () {
//     let currentAudioButton = null;

//     // 初始化所有语速控制器
//     document.querySelectorAll('.speed-slider').forEach(slider => {
//         const valueDisplay = slider.nextElementSibling;

//         slider.addEventListener('input', function () {
//             const rate = parseFloat(this.value);
//             valueDisplay.textContent = rate.toFixed(1) + 'x';

//             // 如果当前正在播放，实时更新语速
//             if (responsiveVoice.isPlaying()) {
//                 stopCurrentSpeech();
//                 const audioButton = currentAudioButton;
//                 if (audioButton) {
//                     audioButton.click();
//                 }
//             }
//         });
//     });

//     function stopCurrentSpeech() {
//         if (responsiveVoice.isPlaying()) {
//             responsiveVoice.cancel();
//             if (currentAudioButton) {
//                 currentAudioButton.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
//                 <polygon points="5 3 19 12 5 21 5 3"></polygon>
//             </svg>`;
//             }
//             currentUtterance = null;
//             currentAudioButton = null;
//         }
//     }

//     document.querySelectorAll('.translation-toggle').forEach(button => {
//         button.addEventListener('click', function () {
//             const section = this.closest('.english-container');
//             const englishText = section.querySelector('.english-text');
//             const audioButton = section.querySelector('.audio-control');
//             const speedControl = section.querySelector('.speed-control');
//             const isHidden = englishText.style.display === 'none' || englishText.style.display === '';

//             englishText.style.display = isHidden ? 'block' : 'none';
//             audioButton.style.display = isHidden ? 'block' : 'none';
//             speedControl.style.display = isHidden ? 'flex' : 'none';
//             this.textContent = isHidden ? '隐藏英文翻译' : '显示英文翻译';

//             if (!isHidden) {
//                 stopCurrentSpeech();
//             }
//         });
//     });

//     document.querySelectorAll('.audio-control').forEach(button => {
//         button.addEventListener('click', function () {
//             const section = this.closest('.english-text');
//             const englishText = section.getAttribute('data-text');
//             const container = this.closest('.english-container');
//             const speedSlider = container.querySelector('.speed-slider');

//             if (responsiveVoice.isPlaying() && currentAudioButton === this) {
//                 stopCurrentSpeech();
//                 return;
//             }

//             stopCurrentSpeech();
//             currentAudioButton = this;
//             currentAudioButton.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="animate-spin">
//             <circle cx="12" cy="12" r="10" opacity="0.25" />
//             <path d="M12 2a10 10 0 0 1 10 10" stroke="currentColor" stroke-width="4" />
//         </svg>`;
//             responsiveVoice.cancel();
//             responsiveVoice.speak(englishText, "US English Female", {
//                 rate: parseFloat(speedSlider.value), // 语速
//                 onstart: function () {
//                     // 播放开始时的回调
//                     speedSlider.disabled = true;
//                     console.log("Audio started");  // 调试信息
//                     currentAudioButton = button;  // 确保正确引用当前按钮
//                     currentAudioButton.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
//             <rect x="6" y="4" width="4" height="16"></rect>
//             <rect x="14" y="4" width="4" height="16"></rect>
//         </svg>`; // 更新按钮图标为暂停样式
//                 },
//                 onend: function () {
//                     // 播放结束时的回调
//                     speedSlider.disabled = false;
//                     console.log("Audio ended");  // 调试信息
//                     currentAudioButton.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
//             <polygon points="5 3 19 12 5 21 5 3"></polygon>
//         </svg>`; // 更新按钮图标为播放样式
//                     currentAudioButton = null;
//                 }
//             });
//         });
//     });

//     document.addEventListener('visibilitychange', function () {
//         if (document.hidden) {
//             stopCurrentSpeech();
//         }
//     });
// });