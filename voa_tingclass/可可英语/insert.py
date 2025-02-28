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
    "title": "英语短文听力入门 第200期:码头的人们",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-413698.html",
    "index": 179,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-413698.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 7766
  },
  {
    "title": "英语短文听力入门 第199期:上帝的指示",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-413392.html",
    "index": 178,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-413392.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6080
  },
  {
    "title": "英语短文听力入门 第198期:递送",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-413162.html",
    "index": 177,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-413162.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4710
  },
  {
    "title": "英语短文听力入门 第197期:寻找",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-412857.html",
    "index": 176,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-412857.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2670
  },
  {
    "title": "英语短文听力入门 第196期:炎热天气",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-412585.html",
    "index": 175,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-412585.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 8917
  },
  {
    "title": "英语短文听力入门 第195期:笔记本电脑",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-412392.html",
    "index": 174,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-412392.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6050
  },
  {
    "title": "英语短文听力入门 第194期:他说英语",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-412152.html",
    "index": 173,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-412152.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 7778
  },
  {
    "title": "英语短文听力入门 第193期:套头衫",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-411861.html",
    "index": 172,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-411861.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 7609
  },
  {
    "title": "英语短文听力入门 第192期:相信警察局长",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-411600.html",
    "index": 171,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-411600.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2110
  },
  {
    "title": "英语短文听力入门 第191期:饥饿的艺术家",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-411598.html",
    "index": 170,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-411598.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2301
  },
  {
    "title": "英语短文听力入门 第190期:针头很脏",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-411172.html",
    "index": 169,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-411172.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2345
  },
  {
    "title": "英语短文听力入门 第189期:一半",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-411168.html",
    "index": 168,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-411168.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1381
  },
  {
    "title": "英语短文听力入门 第188期:燃烧",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-410858.html",
    "index": 167,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-410858.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2119
  },
  {
    "title": "英语短文听力入门 第187期:职业培训",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-410593.html",
    "index": 166,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-410593.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 3296
  },
  {
    "title": "英语短文听力入门 第186期:这个主意不错",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-410361.html",
    "index": 165,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-410361.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 7931
  },
  {
    "title": "英语短文听力入门 第185期:学习游泳",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-410071.html",
    "index": 164,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-410071.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 9254
  },
  {
    "title": "英语短文听力入门 第184期:睡觉还是起床",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-409786.html",
    "index": 163,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-409786.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1892
  },
  {
    "title": "英语短文听力入门 第183期:春节快乐吗",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-409785.html",
    "index": 162,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-409785.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 8532
  },
  {
    "title": "英语短文听力入门 第182期:砍伐树木",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-409784.html",
    "index": 161,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-409784.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 3340
  },
  {
    "title": "英语短文听力入门 第181期:喧闹的派对",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-409540.html",
    "index": 160,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-409540.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 3656
  },
  {
    "title": "英语短文听力入门 第180期:模仿者",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-409288.html",
    "index": 159,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-409288.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6697
  },
  {
    "title": "英语短文听力入门 第179期:不要捡垃圾",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-409032.html",
    "index": 158,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-409032.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2253
  },
  {
    "title": "英语短文听力入门 第178期:新邻居",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-408740.html",
    "index": 157,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-408740.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 9178
  },
  {
    "title": "英语短文听力入门 第177期:房价升高",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-408326.html",
    "index": 156,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-408326.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1905
  },
  {
    "title": "英语短文听力入门 第176期:图书展销会",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-408323.html",
    "index": 155,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-408323.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2646
  },
  {
    "title": "英语短文听力入门 第175期:加油站",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-408320.html",
    "index": 154,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-408320.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 7934
  },
  {
    "title": "英语短文听力入门 第174期:市长迟到",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-407871.html",
    "index": 153,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-407871.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6438
  },
  {
    "title": "英语短文听力入门 第173期:新宠物店",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-407869.html",
    "index": 152,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-407869.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1785
  },
  {
    "title": "英语短文听力入门 第172期:死亡",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-407558.html",
    "index": 151,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-407558.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 9081
  },
  {
    "title": "英语短文听力入门 第171期:懒惰的狗",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-407289.html",
    "index": 150,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-407289.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6559
  },
  {
    "title": "英语短文听力入门 第170期:山路",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-406865.html",
    "index": 149,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-406865.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4124
  },
  {
    "title": "英语短文听力入门 第169期:车会启动吗",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-406861.html",
    "index": 148,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-406861.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4011
  },
  {
    "title": "英语短文听力入门 第168期:没有食物",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-406858.html",
    "index": 147,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-406858.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 3059
  },
  {
    "title": "英语短文听力入门 第167期:她不吃肉",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-406309.html",
    "index": 146,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-406309.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1270
  },
  {
    "title": "英语短文听力入门 第166期:问题太多",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-406009.html",
    "index": 145,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-406009.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2999
  },
  {
    "title": "英语短文听力入门 第165期:他们想要个孩子",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-405733.html",
    "index": 144,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-405733.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4810
  },
  {
    "title": "英语短文听力入门 第164期:干净的汽车",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-405376.html",
    "index": 143,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-405376.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1564
  },
  {
    "title": "英语短文听力入门 第163期:耐心的妈妈",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-405375.html",
    "index": 142,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-405375.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1914
  },
  {
    "title": "英语短文听力入门 第162期:无家可归者",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-405373.html",
    "index": 141,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-405373.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2616
  },
  {
    "title": "英语短文听力入门 第161期:不是钱的问题",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-405168.html",
    "index": 140,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-405168.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1168
  },
  {
    "title": "英语短文听力入门 第160期:上帝选择好人",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-404821.html",
    "index": 139,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-404821.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 5647
  },
  {
    "title": "英语短文听力入门 第159期:它们飞得真好",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-404605.html",
    "index": 138,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-404605.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 9377
  },
  {
    "title": "英语短文听力入门 第158期:月亮",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-404357.html",
    "index": 137,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-404357.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 3152
  },
  {
    "title": "英语短文听力入门 第157期:下雨",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-403969.html",
    "index": 136,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-403969.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 3728
  },
  {
    "title": "英语短文听力入门 第156期:现金",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-403963.html",
    "index": 135,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-403963.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1567
  },
  {
    "title": "英语短文听力入门 第154期:婴儿",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-403725.html",
    "index": 134,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-403725.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 8643
  },
  {
    "title": "英语短文听力入门 第153期:足球",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-403475.html",
    "index": 133,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-403475.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4384
  },
  {
    "title": "英语短文听力入门 第152期:死尸",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-403250.html",
    "index": 132,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-403250.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2774
  },
  {
    "title": "英语短文听力入门 第151期:我都喜欢",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-402861.html",
    "index": 131,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-402861.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4999
  },
  {
    "title": "英语短文听力入门 第150期:太多犯人",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-402618.html",
    "index": 130,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-402618.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4247
  },
  {
    "title": "英语短文听力入门 第149期:寒冬",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-402616.html",
    "index": 129,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-402616.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4292
  },
  {
    "title": "英语短文听力入门 第148期:借钱",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-402334.html",
    "index": 128,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-402334.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6978
  },
  {
    "title": "英语短文听力入门 第147期:干净的教堂",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-402082.html",
    "index": 127,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-402082.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1525
  },
  {
    "title": "英语短文听力入门 第146期:教师",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-401578.html",
    "index": 126,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-401578.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 5585
  },
  {
    "title": "英语短文听力入门 第145期:月亮上的男人",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-401395.html",
    "index": 125,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-401395.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2975
  },
  {
    "title": "英语短文听力入门 第144期:他会和我结婚吗",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-401194.html",
    "index": 124,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-401194.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6725
  },
  {
    "title": "英语短文听力入门 第142期:胡吃海塞",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-400775.html",
    "index": 123,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-400775.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2583
  },
  {
    "title": "英语短文听力入门 第140期:洗衣服",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-400571.html",
    "index": 122,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-400571.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1242
  },
  {
    "title": "英语短文听力入门 第139期:婴儿保姆",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-400472.html",
    "index": 121,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-400472.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 8594
  },
  {
    "title": "英语短文听力入门 第138期:想要不想要",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-400202.html",
    "index": 120,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-400202.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 9902
  },
  {
    "title": "英语短文听力入门 第137期:谁在按铃",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-399958.html",
    "index": 119,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-399958.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 8824
  },
  {
    "title": "英语短文听力入门 第136期:参观公园",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-399464.html",
    "index": 118,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-399464.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 5698
  },
  {
    "title": "英语短文听力入门 第135期:她去了哪",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-399462.html",
    "index": 117,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-399462.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2514
  },
  {
    "title": "英语短文听力入门 第134期:棒球比赛",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-399204.html",
    "index": 116,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-399204.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 8329
  },
  {
    "title": "英语短文听力入门 第133期:吝啬男友",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-399457.html",
    "index": 115,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-399457.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 5292
  },
  {
    "title": "英语短文听力入门 第132期:耳朵问题",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-399187.html",
    "index": 114,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-399187.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2290
  },
  {
    "title": "英语短文听力入门 第131期:喂鸽子",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-398885.html",
    "index": 113,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-398885.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6922
  },
  {
    "title": "英语短文听力入门 第130期:小憩",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-397884.html",
    "index": 112,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-397884.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 9078
  },
  {
    "title": "英语短文听力入门 第129期:10个俯卧撑",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-397883.html",
    "index": 111,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-397883.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 3353
  },
  {
    "title": "英语短文听力入门 第128期:总在吃饭",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-397668.html",
    "index": 110,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-397668.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6847
  },
  {
    "title": "英语短文听力入门 第127期:手枪",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-397212.html",
    "index": 109,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-397212.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 9082
  },
  {
    "title": "英语短文听力入门 第126期:7点打电话",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-397211.html",
    "index": 108,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-397211.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6493
  },
  {
    "title": "英语短文听力入门 第124期:我的钱在哪",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-396849.html",
    "index": 107,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-396849.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4674
  },
  {
    "title": "英语短文听力入门 第123期:猪流感",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-396677.html",
    "index": 106,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-396677.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 7261
  },
  {
    "title": "英语短文听力入门 第122期:陌生人",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-396675.html",
    "index": 105,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-396675.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1613
  },
  {
    "title": "英语短文听力入门 第121期:东西太多",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-396673.html",
    "index": 104,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-396673.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 5436
  },
  {
    "title": "英语短文听力入门 第120期:著名画家",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-396428.html",
    "index": 103,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-396428.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2271
  },
  {
    "title": "英语短文听力入门 第119期:马戏团",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-395776.html",
    "index": 102,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-395776.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 5275
  },
  {
    "title": "英语短文听力入门 第118期:他喜欢吃热狗",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-395495.html",
    "index": 101,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-395495.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 8886
  },
  {
    "title": "英语短文听力入门 第117期:沙滩趣事",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-395188.html",
    "index": 100,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-395188.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 9506
  },
  {
    "title": "英语短文听力入门 第116期:同事",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-394952.html",
    "index": 99,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-394952.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 3175
  },
  {
    "title": "英语短文听力入门 第115期:美丽的夹克衫",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-394489.html",
    "index": 98,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-394489.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2787
  },
  {
    "title": "英语短文听力入门 第114期:去钓鱼",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-394488.html",
    "index": 97,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-394488.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 5575
  },
  {
    "title": "英语短文听力入门 第113期:车里睡觉",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-393807.html",
    "index": 96,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-393807.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 3870
  },
  {
    "title": "英语短文听力入门 第112期:腿受伤",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-393800.html",
    "index": 95,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-393800.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 7457
  },
  {
    "title": "英语短文听力入门 第111期:头发颜色",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-393185.html",
    "index": 94,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-393185.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 5204
  },
  {
    "title": "英语短文听力入门 第110期:墙上的洞",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-393183.html",
    "index": 93,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-393183.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6979
  },
  {
    "title": "英语短文听力入门 第109期:8个孩子",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-393179.html",
    "index": 92,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-393179.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 9442
  },
  {
    "title": "英语短文听力入门 第108期:开枪",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-391718.html",
    "index": 91,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-391718.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4769
  },
  {
    "title": "英语短文听力入门 第107期:钢琴家",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-391714.html",
    "index": 90,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-391714.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 8533
  },
  {
    "title": "英语短文听力入门 第106期:玫瑰女王",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-391713.html",
    "index": 89,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-391713.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2047
  },
  {
    "title": "英语短文听力入门 第105期:红点",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-391694.html",
    "index": 88,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-391694.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6889
  },
  {
    "title": "英语短文听力入门 第104期:让我开",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-391692.html",
    "index": 87,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-391692.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6041
  },
  {
    "title": "英语短文听力入门 第103期:飞碟",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-391688.html",
    "index": 86,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-391688.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 5013
  },
  {
    "title": "英语短文听力入门 第102期:野猫",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-391589.html",
    "index": 85,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-391589.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2166
  },
  {
    "title": "英语短文听力入门 第101期:门后有什么",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-390170.html",
    "index": 84,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-390170.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 3715
  },
  {
    "title": "英语短文听力入门 第100期:干净地板",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-390169.html",
    "index": 83,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-390169.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1624
  },
  {
    "title": "英语短文听力入门 第99期:收集硬币",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-390167.html",
    "index": 82,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-390167.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1847
  },
  {
    "title": "英语短文听力入门 第98期:暑期工作",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-390166.html",
    "index": 81,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-390166.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 5925
  },
  {
    "title": "英语短文听力入门 第97期:相信上帝",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-390164.html",
    "index": 80,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-390164.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 8377
  },
  {
    "title": "英语短文听力入门 第96期:新鲜沙拉",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-390163.html",
    "index": 79,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-390163.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4959
  },
  {
    "title": "英语短文听力入门 第95期:一辆轮椅",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-390050.html",
    "index": 78,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-390050.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 9882
  },
  {
    "title": "英语短文听力入门 第94期:水道疏通剂",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-389141.html",
    "index": 77,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-389141.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6830
  },
  {
    "title": "英语短文听力入门 第93期:更多牛奶",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-389139.html",
    "index": 76,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-389139.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4455
  },
  {
    "title": "英语短文听力入门 第92期:电池没电",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-389135.html",
    "index": 75,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-389135.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1733
  },
  {
    "title": "英语短文听力入门 第90期:洗衣机",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-388798.html",
    "index": 74,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-388798.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6305
  },
  {
    "title": "英语短文听力入门 第88期:吃花生",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-388482.html",
    "index": 73,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-388482.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4956
  },
  {
    "title": "英语短文听力入门 第87期:洗手",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-386689.html",
    "index": 72,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-386689.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4551
  },
  {
    "title": "英语短文听力入门 第86期:水与苹果",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-386688.html",
    "index": 71,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-386688.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1718
  },
  {
    "title": "英语短文听力入门 第85期:饥饿的鸟",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-386687.html",
    "index": 70,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-386687.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6565
  },
  {
    "title": "英语短文听力入门 第84期:飞走了",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-386685.html",
    "index": 69,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-386685.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 9329
  },
  {
    "title": "英语短文听力入门 第83期:红白蓝",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-386683.html",
    "index": 68,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-386683.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 8759
  },
  {
    "title": "英语短文听力入门 第82期:鸡汤",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-386682.html",
    "index": 67,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-386682.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 8417
  },
  {
    "title": "英语短文听力入门 第81期:露露的信",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-386403.html",
    "index": 66,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-386403.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4461
  },
  {
    "title": "英语短文听力入门 第80期:他的新书",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-386195.html",
    "index": 65,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-386195.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 5714
  },
  {
    "title": "英语短文听力入门 第79期:红色橡胶球",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-385354.html",
    "index": 64,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-385354.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 8683
  },
  {
    "title": "英语短文听力入门 第78期:吃饭的地方",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-385351.html",
    "index": 63,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-385351.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 9755
  },
  {
    "title": "英语短文听力入门 第77期:苹果和鸡蛋",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-385347.html",
    "index": 62,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-385347.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4469
  },
  {
    "title": "英语短文听力入门 第76期:大音量",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-385345.html",
    "index": 61,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-385345.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1005
  },
  {
    "title": "英语短文听力入门 第75期:胳臂上打针",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-385340.html",
    "index": 60,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-385340.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2600
  },
  {
    "title": "英语短文听力入门 第73期:回房间",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-384903.html",
    "index": 59,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-384903.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 9389
  },
  {
    "title": "英语短文听力入门 第70期:一张纸",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-384897.html",
    "index": 58,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-384897.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 5385
  },
  {
    "title": "英语短文听力入门 第69期:农民",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-384011.html",
    "index": 57,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-384011.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1057
  },
  {
    "title": "英语短文听力入门 第68期:给老师苹果",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-384008.html",
    "index": 56,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-384008.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 3758
  },
  {
    "title": "英语短文听力入门 第65期:女孩打架",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-384001.html",
    "index": 55,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-384001.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2376
  },
  {
    "title": "英语短文听力入门 第62期:没房子住",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-382916.html",
    "index": 54,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-382916.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6024
  },
  {
    "title": "英语短文听力入门 第61期:两片阿司匹林",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-382915.html",
    "index": 53,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-382915.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4811
  },
  {
    "title": "英语短文听力入门 第60期:不想生活了",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-382912.html",
    "index": 52,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-382912.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 7102
  },
  {
    "title": "英语短文听力入门 第59期:生日贺卡",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-382053.html",
    "index": 51,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-382053.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1310
  },
  {
    "title": "英语短文听力入门 第58期:上帝",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-382052.html",
    "index": 50,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-382052.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1757
  },
  {
    "title": "英语短文听力入门 第57期:新鞋子",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-382051.html",
    "index": 49,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-382051.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 9915
  },
  {
    "title": "英语短文听力入门 第56期:帕蒂的洋娃娃",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-382050.html",
    "index": 48,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-382050.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6078
  },
  {
    "title": "英语短文听力入门 第55期:流感",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-382042.html",
    "index": 47,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-382042.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 3167
  },
  {
    "title": "英语短文听力入门 第54期:每日新闻",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-382041.html",
    "index": 46,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-382041.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 7704
  },
  {
    "title": "英语短文听力入门 第53期:钱存银行",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-381105.html",
    "index": 45,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-381105.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1161
  },
  {
    "title": "英语短文听力入门 第52期:癌症",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-381103.html",
    "index": 44,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-381103.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6349
  },
  {
    "title": "英语短文听力入门 第51期:坏孩子",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-381102.html",
    "index": 43,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-381102.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 5084
  },
  {
    "title": "英语短文听力入门 第50期:好老师",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-381101.html",
    "index": 42,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-381101.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2059
  },
  {
    "title": "英语短文听力入门 第49期:风暴",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-380561.html",
    "index": 41,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-380561.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 9272
  },
  {
    "title": "英语短文听力入门 第48期:可怜的小狗",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-380549.html",
    "index": 40,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-380549.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 8869
  },
  {
    "title": "英语短文听力入门 第47期:失业",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-380540.html",
    "index": 39,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-380540.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6992
  },
  {
    "title": "英语短文听力入门 第46期:减肥",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-380530.html",
    "index": 38,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-380530.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 3438
  },
  {
    "title": "英语短文听力入门 第44期:喜欢虫子",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-379279.html",
    "index": 37,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-379279.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 9236
  },
  {
    "title": "英语短文听力入门 第42期:问题",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-379276.html",
    "index": 36,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-379276.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 3759
  },
  {
    "title": "英语短文听力入门 第41期:新生儿",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-379275.html",
    "index": 35,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-379275.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4568
  },
  {
    "title": "英语短文听力入门 第40期:开快车的司机",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-379274.html",
    "index": 34,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-379274.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 3855
  },
  {
    "title": "英语短文听力入门 第39期:无活力",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-378625.html",
    "index": 33,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-378625.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4128
  },
  {
    "title": "英语短文听力入门 第38期:工作",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-378624.html",
    "index": 32,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-378624.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 8573
  },
  {
    "title": "英语短文听力入门 第37期:爱",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-378623.html",
    "index": 31,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-378623.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6713
  },
  {
    "title": "英语短文听力入门 第36期:奶酪",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-378621.html",
    "index": 30,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-378621.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 9728
  },
  {
    "title": "英语短文听力入门 第35期:写支票",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-378098.html",
    "index": 29,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-378098.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 5737
  },
  {
    "title": "英语短文听力入门 第34期:打扫公寓",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-378097.html",
    "index": 28,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-378097.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 7062
  },
  {
    "title": "英语短文听力入门 第33期:太无礼了",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-378095.html",
    "index": 27,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-378095.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 7989
  },
  {
    "title": "英语短文听力入门 第32期:简单的沙拉",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-378093.html",
    "index": 26,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-378093.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4210
  },
  {
    "title": "英语短文听力入门 第31期:跑步",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-377161.html",
    "index": 25,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-377161.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 9453
  },
  {
    "title": "英语短文听力入门 第30期:弹钢琴",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-377156.html",
    "index": 24,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-377156.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 5825
  },
  {
    "title": "英语短文听力入门 第29期:游泳运动员",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-376534.html",
    "index": 23,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-376534.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6955
  },
  {
    "title": "英语短文听力入门 第28期:一辆新车",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-376533.html",
    "index": 22,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-376533.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1802
  },
  {
    "title": "英语短文听力入门 第27期:新鞋",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-376529.html",
    "index": 21,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-376529.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1772
  },
  {
    "title": "英语短文听力入门 第26期:他的红色自行车",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-376528.html",
    "index": 20,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-376528.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6285
  },
  {
    "title": "英语短文听力入门 第25期:十岁生日",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-375799.html",
    "index": 19,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-375799.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4121
  },
  {
    "title": "英语短文听力入门 第24期:农场",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-375790.html",
    "index": 18,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-375790.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2277
  },
  {
    "title": "英语短文听力入门 第23期:矮女孩",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-375462.html",
    "index": 17,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-375462.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 7853
  },
  {
    "title": "英语短文听力入门 第22期:写信",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-375458.html",
    "index": 16,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-375458.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 8964
  },
  {
    "title": "英语短文听力入门 第21期:加法",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-375456.html",
    "index": 15,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-375456.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 6640
  },
  {
    "title": "英语短文听力入门 第20期:天气寒冷",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-375453.html",
    "index": 14,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-375453.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 7115
  },
  {
    "title": "英语短文听力入门 第19期:垃圾日",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-375451.html",
    "index": 13,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-375451.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1016
  },
  {
    "title": "英语短文听力入门 第18期:谁啊",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-374711.html",
    "index": 12,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-374711.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 3263
  },
  {
    "title": "英语短文听力入门 第17期:洗手",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-374710.html",
    "index": 11,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-374710.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 3735
  },
  {
    "title": "英语短文听力入门 第16期:瓶中之虫",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-374228.html",
    "index": 10,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-374228.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 8210
  },
  {
    "title": "英语短文听力入门 第15期:笑话",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-374224.html",
    "index": 9,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-374224.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 5135
  },
  {
    "title": "英语短文听力入门 第14期:瘦弱男子",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-374223.html",
    "index": 8,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-374223.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1492
  },
  {
    "title": "英语短文听力入门 第13期:买辆新车",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-374221.html",
    "index": 7,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-374221.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 8460
  },
  {
    "title": "英语短文听力入门 第12期:新鲜的鱼肉",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-373497.html",
    "index": 6,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-373497.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 9464
  },
  {
    "title": "英语短文听力入门 第11期:去上班",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-373496.html",
    "index": 5,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-373496.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 2394
  },
  {
    "title": "英语短文听力入门 第10期:巧克力奶",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-373495.html",
    "index": 4,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-373495.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4802
  },
  {
    "title": "英语短文听力入门 第9期:红莓",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-373494.html",
    "index": 3,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-373494.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4729
  },
  {
    "title": "英语短文听力入门 第7期:划船",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-372966.html",
    "index": 2,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-372966.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 4030
  },
  {
    "title": "英语短文听力入门 第5期:骑马",
    "url": "http://readingstuday.top/tingli/duanwen_tingli_rumen/15615-372234.html",
    "index": 1,
    "mp3_url": "https://774663576.github.io/br_media/tingli/duanwen_tingli_rumen/mp3/15615-372234.mp3",
    "category": "duanwen_tingli_rumen",
    "views": 1553
  }
]
# 插入数据的 SQL 语句
insert_query = """
INSERT INTO tingli (url, `index`, title, view_count, category, mp3_url)
VALUES (%s, %s, %s, %s, %s, %s)
"""

# 插入数据
for item in data:
    cursor.execute(insert_query, (
        item['url'],
        item['index'],
        item['title'],
        item['views'],
        item['category'],
        item['mp3_url']
    ))

# 提交事务
conn.commit()

# 关闭连接
cursor.close()
conn.close()

print("数据插入成功！")
