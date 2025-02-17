import requests
import os
from pydub import AudioSegment
from io import BytesIO

# MP3 文件链接列表
mp3_list = [
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/1.html",
    "index": 1,
    "title": "I don't care where we go as long as we...",
    "views": 42300,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1091_12.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/2.html",
    "index": 2,
    "title": "l am vacuuming the floor now and have several...",
    "views": 15738,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1091_11.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/3.html",
    "index": 3,
    "title": "I'm doing some washing and John is cooking...",
    "views": 14614,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1091_10.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/4.html",
    "index": 4,
    "title": "Manners are quite different from country...",
    "views": 10768,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1091_9.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/5.html",
    "index": 5,
    "title": "However, Susan has not really made up her mind ye",
    "views": 10545,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1091_8.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/6.html",
    "index": 6,
    "title": "We are all taking medicine against the disease. 我",
    "views": 10224,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1091_7.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/7.html",
    "index": 7,
    "title": "The truth is quite other than what you think. 事实真",
    "views": 11093,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1091_6.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/8.html",
    "index": 8,
    "title": "She intends to make teaching her profession. 她想以教",
    "views": 10641,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1091_5.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/9.html",
    "index": 9,
    "title": "The examination put a lot of stress on him. 那次考试给",
    "views": 10648,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1091_4.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/10.html",
    "index": 10,
    "title": "She feared staying alone in the farmhouse. 她害怕一个人",
    "views": 10839,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1091_3.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/11.html",
    "index": 11,
    "title": "It was your turn to wash them yesterday. 昨天轮到你把它们",
    "views": 11652,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1091_2.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/12.html",
    "index": 12,
    "title": "His cake is three times bigger than mine. 他的蛋糕比我的",
    "views": 16540,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1091_1.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/13.html",
    "index": 13,
    "title": "Where can we make the insurance claim? 我们可以在哪里提出保",
    "views": 10413,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1090_10.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/14.html",
    "index": 14,
    "title": "Don't be uneasy about the consequence. 不必为后果忧",
    "views": 10718,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1090_9.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/15.html",
    "index": 15,
    "title": "As you know, I am a very kind person. 你知道，我是个很和善的",
    "views": 12592,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1090_8.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/16.html",
    "index": 16,
    "title": "I appreciate John's helping in time. 我感谢约翰的及时",
    "views": 11035,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1090_7.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/17.html",
    "index": 17,
    "title": "I hope you enjoy your stay with us. 希望您在这儿过的愉快",
    "views": 14123,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1090_6.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/18.html",
    "index": 18,
    "title": "I'd like to look at some sweaters. 我想看看毛衣",
    "views": 12387,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1090_5.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/19.html",
    "index": 19,
    "title": "Time is more valuable than money. 时间比金钱宝贵",
    "views": 13901,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1090_4.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/20.html",
    "index": 20,
    "title": "You'd better look before you leap. 你比较好三思而后行",
    "views": 18933,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1090_3.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/21.html",
    "index": 21,
    "title": "What ever I said，he'd disagree. 不论我说什么他都不同意",
    "views": 23128,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1090_2.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/22.html",
    "index": 22,
    "title": "Go right back to the beginning. 直接回到起始位置",
    "views": 20115,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1090_1.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/23.html",
    "index": 23,
    "title": "He is taller than I by ahead. 他比我高一头。",
    "views": 18771,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1088_10.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/24.html",
    "index": 24,
    "title": "He neither smokes nor drinks. 他既不抽烟也不喝酒。",
    "views": 19922,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1088_9.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/25.html",
    "index": 25,
    "title": "I went there three days ago. 我三天前去过那儿。",
    "views": 19039,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1088_8.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/26.html",
    "index": 26,
    "title": "I was taking care of Sally. 我在照顾萨莉。",
    "views": 18032,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1088_7.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/27.html",
    "index": 27,
    "title": "There go the house lights. 剧院的灯光灭了。",
    "views": 20556,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1088_6.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/28.html",
    "index": 28,
    "title": "Did you enter the contest? 你参加比赛了吗?",
    "views": 22133,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1088_5.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/29.html",
    "index": 29,
    "title": "I'm not sure I can do it. 恐怕这事我干不了。",
    "views": 24561,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1088_4.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/30.html",
    "index": 30,
    "title": "I get up at six o'clock. 我六点起床。",
    "views": 28432,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1088_3.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/31.html",
    "index": 31,
    "title": "He was not a bit tired. 他一点也不累。",
    "views": 29795,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1088_2.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/32.html",
    "index": 32,
    "title": "He has a large income. 他有很高的收入。",
    "views": 33201,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1088_1.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/33.html",
    "index": 33,
    "title": "We are good friends. 我们是好朋友。",
    "views": 39670,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/8.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/34.html",
    "index": 34,
    "title": "He is just a child. 他只是个孩子。",
    "views": 39149,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/7.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/35.html",
    "index": 35,
    "title": "Don't fall for it! 别上当!",
    "views": 44093,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/6.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/36.html",
    "index": 36,
    "title": "]It sounds great!. 听起来很不错。",
    "views": 57232,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/5.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/37.html",
    "index": 37,
    "title": "Who's calling? 是哪一位",
    "views": 58640,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/4.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/38.html",
    "index": 38,
    "title": "Never mind. 不要紧",
    "views": 73710,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/3.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/39.html",
    "index": 39,
    "title": "So do I. 我也一样",
    "views": 109501,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/2.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/999_kouhu/40.html",
    "index": 40,
    "title": "I see. 我明白了。",
    "views": 222615,
    "category": "999_kouhu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1087/1.mp3"
  }
]

# 创建保存文件的文件夹
output_folder = "999mp3"
os.makedirs(output_folder, exist_ok=True)

def download_and_trim(mp3_url, title, index):
    # 下载 MP3 文件
    response = requests.get(mp3_url,headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
})
    if response.status_code == 200:
        audio = AudioSegment.from_mp3(BytesIO(response.content))
        
        # 剪掉前13秒
        trimmed_audio = audio[13000:]  # 保留从13秒开始的部分
        
        file_path = os.path.join(output_folder, f"{item['index']}.mp3")
        trimmed_audio.export(file_path, format="mp3")
        print(f"文件已保存: {file_path}")
    else:
        print(f"下载失败: {mp3_url}")

# 下载并裁剪所有 MP3 文件
for item in mp3_list:
    download_and_trim(item["mp3_url"], item["title"], item["index"])
