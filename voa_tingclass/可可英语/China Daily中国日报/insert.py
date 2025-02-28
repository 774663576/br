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
    "title": "企业寻求采用中国芯片进行训练",
    "url": "http://readingstuday.top/tingli/china_deily/html/18141-700641.html",
    "index": 10,
    "mp3_url": "https://774663576.github.io/br_media/tingli/china_deily/mp3/18141-700641.mp3",
    "category": "china_deily",
    "views": 6321,
    "update_time":"2025-02-19"
  },
  {
    "title": "美对加关税威胁仍悬而未决",
    "url": "http://readingstuday.top/tingli/china_deily/html/18141-700390.html",
    "index": 9,
   "mp3_url": "https://774663576.github.io/br_media/tingli/china_deily/mp3/18141-700390.mp3",
    "category": "china_deily",
    "views": 4287,
    "update_time":"2025-02-18"
  },
  {
    "title": "新年招聘火热开启",
    "url": "http://readingstuday.top/tingli/china_deily/html/18141-700389.html",
    "index": 8,
   "mp3_url": "https://774663576.github.io/br_media/tingli/china_deily/mp3/18141-700389.mp3",
    "category": "china_deily",
    "views": 4672,
    "update_time":"2025-02-17"
  },
  {
    "title": "特朗普得知拜登与好莱坞主要经纪公司签约",
    "url": "http://readingstuday.top/tingli/china_deily/html/18141-700387.html",
    "index": 7,
   "mp3_url": "https://774663576.github.io/br_media/tingli/china_deily/mp3/18141-700387.mp3",
    "category": "china_deily",
    "views": 1544,
    "update_time":"2025-02-16"
  },
  {
    "title": "春节期间国内景点游客爆满",
    "url": "http://readingstuday.top/tingli/china_deily/html/18141-700385.html",
    "index": 6,
   "mp3_url": "https://774663576.github.io/br_media/tingli/china_deily/mp3/18141-700385.mp3",
    "category": "china_deily",
    "views": 2519,
    "update_time":"2025-02-15"
  },
  {
    "title": "春节档票房创纪录！总票房超北美全球第一",
    "url": "http://readingstuday.top/tingli/china_deily/html/18141-700383.html",
    "index": 5,
   "mp3_url": "https://774663576.github.io/br_media/tingli/china_deily/mp3/18141-700383.mp3",
    "category": "china_deily",
    "views": 3553,
    "update_time":"2025-02-14"
  },
  {
    "title": "中国计划对美国产品加征关税",
    "url": "http://readingstuday.top/tingli/china_deily/html/18141-700115.html",
    "index": 4,
   "mp3_url": "https://774663576.github.io/br_media/tingli/china_deily/mp3/18141-700115.mp3",
    "category": "china_deily",
    "views": 5000,
    "update_time":"2025-02-13"
  },
  {
    "title": "小红书登顶美国下载榜，关联股票迎来强劲上涨",
    "url": "http://readingstuday.top/tingli/china_deily/html/18141-700114.html",
    "index": 3,
   "mp3_url": "https://774663576.github.io/br_media/tingli/china_deily/mp3/18141-700114.mp3",
    "category": "china_deily",
    "views": 1164,
    "update_time":"2025-02-12"
  },
  {
    "title": "星巴克撤销其门店开放政策",
    "url": "http://readingstuday.top/tingli/china_deily/html/18141-700113.html",
    "index": 2,
   "mp3_url": "https://774663576.github.io/br_media/tingli/china_deily/mp3/18141-700113.mp3",
    "category": "china_deily",
    "views": 1151,
    "update_time":"2025-02-11"
  },
  {
    "title": "春节期间国内景点游客爆满",
    "url": "http://readingstuday.top/tingli/china_deily/html/18141-700112.html",
    "index": 1,
    "mp3_url": "https://774663576.github.io/br_media/tingli/china_deily/mp3/18141-700112.mp3",
    "category": "china_deily",
    "views": 1251,
    "update_time":"2025-02-10"
  }
]
# 插入数据的 SQL 语句
insert_query = """
INSERT INTO tingli (url, `index`, title, view_count, category, mp3_url,update_time)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# 插入数据
for item in data:
    cursor.execute(insert_query, (
        item['url'],
        item['index'],
        item['title'],
        item['views'],
        item['category'],
        item['mp3_url'],
        item['update_time']
    ))

# 提交事务
conn.commit()

# 关闭连接
cursor.close()
conn.close()

print("数据插入成功！")
