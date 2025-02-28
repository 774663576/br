import pymysql


DB_CONFIG = {
   'host': '59.110.149.111',
    'user': 'root',
    'password': 'SP123456!',
    'db': 'reading'
}
# 数据库连接
conn = pymysql.connect(**DB_CONFIG)

cursor = conn.cursor()

# 要插入的数据
data =[
  {
    "title": "千万别学英语 第6阶段 情景24:麦克和咪咪见面",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253795.html",
    "index": 112,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253795.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 4972
  },
  {
    "title": "千万别学英语 第6阶段 情景23:麦克和比尔到了宿舍",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253793.html",
    "index": 111,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253793.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 7765
  },
  {
    "title": "千万别学英语 第6阶段 情景22:因特网",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253792.html",
    "index": 110,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253792.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 8458
  },
  {
    "title": "千万别学英语 第6阶段 情景21:碰到比尔",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253791.html",
    "index": 109,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253791.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 5867
  },
  {
    "title": "千万别学英语 第6阶段 情景20:洗衣间",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253790.html",
    "index": 108,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253790.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 1855
  },
  {
    "title": "千万别学英语 第6阶段 情景19:社会学课",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253789.html",
    "index": 107,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253789.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 4421
  },
  {
    "title": "千万别学英语 第6阶段 情景18:政治讨论",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253788.html",
    "index": 106,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253788.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 9375
  },
  {
    "title": "千万别学英语 第6阶段 情景17:去喝咖啡",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253787.html",
    "index": 105,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253787.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 5801
  },
  {
    "title": "千万别学英语 第6阶段 情景16:第二天早上",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253652.html",
    "index": 104,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253652.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 1012
  },
  {
    "title": "千万别学英语 第6阶段 情景15:晚会后在一个酿酒酒吧里",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253650.html",
    "index": 103,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253650.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 1138
  },
  {
    "title": "千万别学英语 第6阶段 情景14:在晚会上",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253648.html",
    "index": 102,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253648.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 6374
  },
  {
    "title": "千万别学英语 第6阶段 情景13:到达晚会现场",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253646.html",
    "index": 101,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253646.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 5674
  },
  {
    "title": "千万别学英语 第6阶段 情景12:开车去宾馆",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253638.html",
    "index": 100,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253638.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 9836
  },
  {
    "title": "千万别学英语 第6阶段 情景11:Mike将Charles介绍给Bill",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253637.html",
    "index": 99,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253637.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 9237
  },
  {
    "title": "千万别学英语 第6阶段 情景10:打电话问地址",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253636.html",
    "index": 98,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253636.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 2218
  },
  {
    "title": "千万别学英语 第6阶段 情景9:准备晚会",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253635.html",
    "index": 97,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253635.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 3187
  },
  {
    "title": "千万别学英语 第6阶段 情景8:Charles的英语课",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253633.html",
    "index": 96,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253633.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 3517
  },
  {
    "title": "千万别学英语 第6阶段 情景7:在的士里",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253631.html",
    "index": 95,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253631.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 4459
  },
  {
    "title": "千万别学英语 第6阶段 情景6:买衬衫",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253630.html",
    "index": 94,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253630.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 3226
  },
  {
    "title": "千万别学英语 第6阶段 情景5:电话对话",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253627.html",
    "index": 93,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253627.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 5350
  },
  {
    "title": "千万别学英语 第6阶段 情景4:回到宿舍",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253625.html",
    "index": 92,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253625.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 2306
  },
  {
    "title": "千万别学英语 第6阶段 情景3:早午餐",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253621.html",
    "index": 91,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253621.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 7536
  },
  {
    "title": "千万别学英语 第6阶段 情景2:历史课",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253616.html",
    "index": 90,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253616.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 1319
  },
  {
    "title": "千万别学英语 第6阶段 情景1:起床晚点",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253615.html",
    "index": 89,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253615.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 5045
  },
  {
    "title": "千万别学英语 第5阶段 情景23:回到办公室",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253567.html",
    "index": 88,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253567.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 9789
  },
  {
    "title": "千万别学英语 第5阶段 情景22:在饭馆里",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253565.html",
    "index": 87,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253565.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 4359
  },
  {
    "title": "千万别学英语 第5阶段 情景21:在James的办公室",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253564.html",
    "index": 86,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253564.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 5900
  },
  {
    "title": "千万别学英语 第5阶段 情景20:在先生的办公室",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253563.html",
    "index": 85,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253563.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 9715
  },
  {
    "title": "千万别学英语 第5阶段 情景19:在办公室",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253561.html",
    "index": 84,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253561.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 4468
  },
  {
    "title": "千万别学英语 第5阶段 情景18:在Dunkin Donuts",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253559.html",
    "index": 83,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253559.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 5756
  },
  {
    "title": "千万别学英语 第5阶段 情景17:早餐",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253557.html",
    "index": 82,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253557.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 2984
  },
  {
    "title": "千万别学英语 第5阶段 情景16:早上起床",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253556.html",
    "index": 81,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253556.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 6806
  },
  {
    "title": "千万别学英语 第5阶段 情景15:回到家里",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253555.html",
    "index": 80,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253555.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 9324
  },
  {
    "title": "千万别学英语 第5阶段 情景14:在酒吧里",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253553.html",
    "index": 79,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253553.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 7923
  },
  {
    "title": "千万别学英语 第5阶段 情景13:在停车场",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253552.html",
    "index": 78,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253552.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 8111
  },
  {
    "title": "千万别学英语 第5阶段 情景12:回到老板办公室",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253550.html",
    "index": 77,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253550.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 8324
  },
  {
    "title": "千万别学英语 第5阶段 情景11:和同事在一起",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253548.html",
    "index": 76,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253548.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 2561
  },
  {
    "title": "千万别学英语 第5阶段 情景10:开会",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253546.html",
    "index": 75,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253546.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 3375
  },
  {
    "title": "千万别学英语 第5阶段 情景9:吃午餐",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253544.html",
    "index": 74,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253544.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 5435
  },
  {
    "title": "千万别学英语 第5阶段 情景8:见老板",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253543.html",
    "index": 73,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253543.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 6054
  },
  {
    "title": "千万别学英语 第5阶段 情景7:秘书",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253542.html",
    "index": 72,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253542.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 4495
  },
  {
    "title": "千万别学英语 第5阶段 情景6:会议部署",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253541.html",
    "index": 71,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253541.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 5698
  },
  {
    "title": "千万别学英语 第5阶段 情景5:到达公司",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253539.html",
    "index": 70,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253539.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 1291
  },
  {
    "title": "千万别学英语 第5阶段 情景4:加油站",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253534.html",
    "index": 69,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253534.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 8535
  },
  {
    "title": "千万别学英语 第5阶段 情景3:开车去上班",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253531.html",
    "index": 68,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253531.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 1871
  },
  {
    "title": "千万别学英语 第5阶段 情景2:早餐",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253530.html",
    "index": 67,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253530.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 1713
  },
  {
    "title": "千万别学英语 第5阶段 情景1:早晨起床",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253529.html",
    "index": 66,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253529.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 3137
  },
  {
    "title": "千万别学英语 第4阶段 情景20:睡觉",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253448.html",
    "index": 65,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253448.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 7453
  },
  {
    "title": "千万别学英语 第4阶段 情景19:柯文的父母准备睡觉",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253445.html",
    "index": 64,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253445.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 6843
  },
  {
    "title": "千万别学英语 第4阶段 情景18:晚会 2",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253444.html",
    "index": 63,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253444.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 7610
  },
  {
    "title": "千万别学英语 第4阶段 情景17:晚会",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253443.html",
    "index": 62,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253443.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 8851
  },
  {
    "title": "千万别学英语 第4阶段 情景16:足球赛",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253441.html",
    "index": 61,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253441.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 7922
  },
  {
    "title": "千万别学英语 第4阶段 情景15:电视新闻",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253439.html",
    "index": 60,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253439.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 9676
  },
  {
    "title": "千万别学英语 第4阶段 情景14:在家里",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253437.html",
    "index": 59,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253437.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 9974
  },
  {
    "title": "千万别学英语 第4阶段 情景13:英语课",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253436.html",
    "index": 58,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253436.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 4122
  },
  {
    "title": "千万别学英语 第4阶段 情景12:在比萨店",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253434.html",
    "index": 57,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253434.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 2956
  },
  {
    "title": "千万别学英语 第4阶段 情景11:午餐",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253433.html",
    "index": 56,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253433.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 3906
  },
  {
    "title": "千万别学英语 第4阶段 情景10:健康教育",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253401.html",
    "index": 55,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253401.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 7672
  },
  {
    "title": "千万别学英语 第4阶段 情景9:早餐时间2",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253400.html",
    "index": 54,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253400.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 8354
  },
  {
    "title": "千万别学英语 第4阶段 情景8:吃早餐",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253398.html",
    "index": 53,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253398.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 7738
  },
  {
    "title": "千万别学英语 第4阶段 情景7:体育课",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253396.html",
    "index": 52,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253396.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 3038
  },
  {
    "title": "千万别学英语 第4阶段 情景6:读书",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253395.html",
    "index": 51,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253395.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 7023
  },
  {
    "title": "千万别学英语 第4阶段 情景5:美国历史",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253394.html",
    "index": 50,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253394.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 7106
  },
  {
    "title": "千万别学英语 第4阶段 情景4:在学校",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253393.html",
    "index": 49,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253393.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 7701
  },
  {
    "title": "千万别学英语 第4阶段 情景3:乐队排练",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253392.html",
    "index": 48,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253392.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 4390
  },
  {
    "title": "千万别学英语 第4阶段 情景1:在早上",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253390.html",
    "index": 47,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253390.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 7730
  },
  {
    "title": "千万别学英语 第3阶段 情景21:与哥哥谈话",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253369.html",
    "index": 46,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253369.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 3474
  },
  {
    "title": "千万别学英语 第3阶段 情景20:网络",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253368.html",
    "index": 45,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253368.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 6487
  },
  {
    "title": "千万别学英语 第3阶段 情景19:罗勃特给米舍打电话",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253366.html",
    "index": 44,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253366.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 1652
  },
  {
    "title": "千万别学英语 第3阶段 情景18:和爸爸谈话",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253365.html",
    "index": 43,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253365.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 5661
  },
  {
    "title": "千万别学英语 第3阶段 情景17:晚餐",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253364.html",
    "index": 42,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253364.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 7302
  },
  {
    "title": "千万别学英语 第3阶段 情景16:家庭作业",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253363.html",
    "index": 41,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253363.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 6777
  },
  {
    "title": "千万别学英语 第3阶段 情景14:篮球训练2",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253360.html",
    "index": 40,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253360.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 3184
  },
  {
    "title": "千万别学英语 第3阶段 情景13:篮球训练1",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253358.html",
    "index": 39,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253358.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 9955
  },
  {
    "title": "千万别学英语 第3阶段 情景12:在诊所",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253356.html",
    "index": 38,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253356.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 1004
  },
  {
    "title": "千万别学英语 第3阶段 情景11:社会学习",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253262.html",
    "index": 37,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253262.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 1571
  },
  {
    "title": "千万别学英语 第3阶段 情景10:休息2",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253259.html",
    "index": 36,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253259.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 5806
  },
  {
    "title": "千万别学英语 第3阶段 情景9:休息1",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253354.html",
    "index": 35,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253354.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 8808
  },
  {
    "title": "千万别学英语 第3阶段 情景8:第二课",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253253.html",
    "index": 34,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253253.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 8961
  },
  {
    "title": "千万别学英语 第3阶段 情景7:第一课",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253251.html",
    "index": 33,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253251.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 3690
  },
  {
    "title": "千万别学英语 第3阶段 情景6:篮球",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253247.html",
    "index": 32,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253247.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 4352
  },
  {
    "title": "千万别学英语 第3阶段 情景5:在校车上",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253246.html",
    "index": 31,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253246.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 3025
  },
  {
    "title": "千万别学英语 第3阶段 情景4:妈妈和爸爸谈话",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253244.html",
    "index": 30,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253244.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 8260
  },
  {
    "title": "千万别学英语 第3阶段 情景3:与父亲谈话",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253242.html",
    "index": 29,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253242.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 8683
  },
  {
    "title": "千万别学英语 第3阶段 情景2:早餐",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253240.html",
    "index": 28,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253240.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 5600
  },
  {
    "title": "千万别学英语 第3阶段 情景1:起床",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253239.html",
    "index": 27,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253239.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 2656
  },
  {
    "title": "千万别学英语 第2阶段 情景15:返回汉城",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253020.html",
    "index": 26,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253020.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 2197
  },
  {
    "title": "千万别学英语 第2阶段 情景14:返回汉城",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253018.html",
    "index": 25,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253018.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 6852
  },
  {
    "title": "千万别学英语 第2阶段 情景13:参观大峡谷",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253016.html",
    "index": 24,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253016.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 6207
  },
  {
    "title": "千万别学英语 第2阶段 情景12:去旧金山",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253014.html",
    "index": 23,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253014.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 7465
  },
  {
    "title": "千万别学英语 第2阶段 情景11:遇见吉米的朋友",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253012.html",
    "index": 22,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253012.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 5950
  },
  {
    "title": "千万别学英语 第2阶段 情景10:参观洛杉矶",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253010.html",
    "index": 21,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253010.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 5029
  },
  {
    "title": "千万别学英语 第2阶段 情景9:步行在洛杉矶",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253008.html",
    "index": 20,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253008.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 4884
  },
  {
    "title": "千万别学英语 第2阶段 情景8:在Kim的家里",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-253007.html",
    "index": 19,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-253007.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 5909
  },
  {
    "title": "千万别学英语 第2阶段 情景7:达到洛杉矶",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-252633.html",
    "index": 18,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-252633.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 4262
  },
  {
    "title": "千万别学英语 第2阶段 情景6:在飞机上",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-252632.html",
    "index": 17,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-252632.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 1734
  },
  {
    "title": "千万别学英语 第2阶段 情景5:在机场",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-252631.html",
    "index": 16,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-252631.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 4958
  },
  {
    "title": "千万别学英语 第2阶段 情景4:去机场",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-252630.html",
    "index": 15,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-252630.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 8325
  },
  {
    "title": "千万别学英语 第2阶段 情景3:谈论假期",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-252628.html",
    "index": 14,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-252628.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 3680
  },
  {
    "title": "千万别学英语 第2阶段 情景2:向帕克夫人和泰格解释",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-252627.html",
    "index": 13,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-252627.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 8662
  },
  {
    "title": "千万别学英语 第2阶段 情景1:谈论美国",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-252625.html",
    "index": 12,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-252625.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 6688
  },
  {
    "title": "千万别学英语 第1阶段 情景15:睡觉",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-252461.html",
    "index": 11,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-252461.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 7345
  },
  {
    "title": "千万别学英语 第1阶段 情景14:看电视",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-184674.html",
    "index": 10,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-184674.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 7025
  },
  {
    "title": "千万别学英语 第1阶段 情景12:李先生下班回家",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-3955.html",
    "index": 9,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-3955.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 3325
  },
  {
    "title": "千万别学英语 第1阶段 情景11:仇女士和安迪",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-3954.html",
    "index": 8,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-3954.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 9136
  },
  {
    "title": "千万别学英语 第1阶段 情景10:电话对话",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-3953.html",
    "index": 7,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-3953.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 7713
  },
  {
    "title": "千万别学英语 第1阶段 场景9:回家",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-3952.html",
    "index": 6,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-3952.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 2861
  },
  {
    "title": "千万别学英语 第1阶段 场景8:在学校吃午餐",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-3951.html",
    "index": 5,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-3951.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 5982
  },
  {
    "title": "千万别学英语 第1阶段 场景7:在咖啡店",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-3950.html",
    "index": 4,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-3950.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 7781
  },
  {
    "title": "千万别学英语 第1阶段 场景6:买食品",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-3949.html",
    "index": 3,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-3949.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 3934
  },
  {
    "title": "千万别学英语 第1阶段 场景4:回到家中",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-3947.html",
    "index": 2,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-3947.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 2548
  },
  {
    "title": "千万别学英语 第1阶段 场景3:上学",
    "url": "http://readingstuday.top/yyrm/qianwanbiexueyingyu/118-3946.html",
    "index": 1,
    "mp3_url": "https://774663576.github.io/br_media/tingli/qianwanbiexueyingyu/mp3/118-3946.mp3",
    "category": "qianwanbiexueyingyu",
    "view_count": 3235
  }
]
# 插入数据的 SQL 语句
insert_query = """
INSERT INTO yingyu_rumen (url, `index`, title, view_count, category, mp3_url)
VALUES (%s, %s, %s, %s, %s, %s)
"""

# 插入数据
for item in data:
    cursor.execute(insert_query, (
        item['url'],
        item['index'],
        item['title'],
        item['view_count'],
        item['category'],
        item['mp3_url']
    ))

# 提交事务
conn.commit()

# 关闭连接
cursor.close()
conn.close()

print("数据插入成功！")
