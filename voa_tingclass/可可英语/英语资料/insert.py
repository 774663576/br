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
    "title": "2024年6月英语六级听力真题(第2套) 录音(3)",
    "url": "http://readingstuday.top/yyrm/2024_liuji_tingli/18440-692829.html",
    "index": 14,
    "mp3_url": "https://774663576.github.io/br_media/tingli/2024_liuji_tingli/mp3/18440-692829.mp3",
    "category": "2024_liuji_tingli",
    "view_count": 4451
  },
  {
    "title": "2024年6月英语六级听力真题(第2套) 录音(2)",
    "url": "http://readingstuday.top/yyrm/2024_liuji_tingli/18440-692828.html",
    "index": 13,
    "mp3_url": "https://774663576.github.io/br_media/tingli/2024_liuji_tingli/mp3/18440-692828.mp3",
    "category": "2024_liuji_tingli",
    "view_count": 3139
  },
  {
    "title": "2024年6月英语六级听力真题(第2套) 录音(1)",
    "url": "http://readingstuday.top/yyrm/2024_liuji_tingli/18440-692827.html",
    "index": 12,
    "mp3_url": "https://774663576.github.io/br_media/tingli/2024_liuji_tingli/mp3/18440-692827.mp3",
    "category": "2024_liuji_tingli",
    "view_count": 8965
  },
  {
    "title": "2024年6月英语六级听力真题(第2套) 短文(2)",
    "url": "http://readingstuday.top/yyrm/2024_liuji_tingli/18440-692826.html",
    "index": 11,
    "mp3_url": "https://774663576.github.io/br_media/tingli/2024_liuji_tingli/mp3/18440-692826.mp3",
    "category": "2024_liuji_tingli",
    "view_count": 6695
  },
  {
    "title": "2024年6月英语六级听力真题(第2套) 短文(1)",
    "url": "http://readingstuday.top/yyrm/2024_liuji_tingli/18440-692825.html",
    "index": 10,
    "mp3_url": "https://774663576.github.io/br_media/tingli/2024_liuji_tingli/mp3/18440-692825.mp3",
    "category": "2024_liuji_tingli",
    "view_count": 2037
  },
  {
    "title": "2024年6月英语六级听力真题(第2套) 长对话(2)",
    "url": "http://readingstuday.top/yyrm/2024_liuji_tingli/18440-692824.html",
    "index": 9,
    "mp3_url": "https://774663576.github.io/br_media/tingli/2024_liuji_tingli/mp3/18440-692824.mp3",
    "category": "2024_liuji_tingli",
    "view_count": 2662
  },
  {
    "title": "2024年6月英语六级听力真题(第2套) 长对话(1)",
    "url": "http://readingstuday.top/yyrm/2024_liuji_tingli/18440-692823.html",
    "index": 8,
    "mp3_url": "https://774663576.github.io/br_media/tingli/2024_liuji_tingli/mp3/18440-692823.mp3",
    "category": "2024_liuji_tingli",
    "view_count": 1142
  },
  {
    "title": "2024年6月英语六级听力真题(第1套) 录音(3)",
    "url": "http://readingstuday.top/yyrm/2024_liuji_tingli/18440-692822.html",
    "index": 7,
    "mp3_url": "https://774663576.github.io/br_media/tingli/2024_liuji_tingli/mp3/18440-692822.mp3",
    "category": "2024_liuji_tingli",
    "view_count": 3802
  },
  {
    "title": "2024年6月英语六级听力真题(第1套) 录音(2)",
    "url": "http://readingstuday.top/yyrm/2024_liuji_tingli/18440-692821.html",
    "index": 6,
    "mp3_url": "https://774663576.github.io/br_media/tingli/2024_liuji_tingli/mp3/18440-692821.mp3",
    "category": "2024_liuji_tingli",
    "view_count": 9454
  },
  {
    "title": "2024年6月英语六级听力真题(第1套) 录音(1)",
    "url": "http://readingstuday.top/yyrm/2024_liuji_tingli/18440-692820.html",
    "index": 5,
    "mp3_url": "https://774663576.github.io/br_media/tingli/2024_liuji_tingli/mp3/18440-692820.mp3",
    "category": "2024_liuji_tingli",
    "view_count": 1806
  },
  {
    "title": "2024年6月英语六级听力真题(第1套) 短文(2)",
    "url": "http://readingstuday.top/yyrm/2024_liuji_tingli/18440-692819.html",
    "index": 4,
    "mp3_url": "https://774663576.github.io/br_media/tingli/2024_liuji_tingli/mp3/18440-692819.mp3",
    "category": "2024_liuji_tingli",
    "view_count": 2657
  },
  {
    "title": "2024年6月英语六级听力真题(第1套) 短文(1)",
    "url": "http://readingstuday.top/yyrm/2024_liuji_tingli/18440-692817.html",
    "index": 3,
    "mp3_url": "https://774663576.github.io/br_media/tingli/2024_liuji_tingli/mp3/18440-692817.mp3",
    "category": "2024_liuji_tingli",
    "view_count": 8066
  },
  {
    "title": "2024年6月英语六级听力真题(第1套) 长对话(2)",
    "url": "http://readingstuday.top/yyrm/2024_liuji_tingli/18440-692816.html",
    "index": 2,
    "mp3_url": "https://774663576.github.io/br_media/tingli/2024_liuji_tingli/mp3/18440-692816.mp3",
    "category": "2024_liuji_tingli",
    "view_count": 9217
  },
  {
    "title": "2024年6月英语六级听力真题(第1套) 长对话(1)",
    "url": "http://readingstuday.top/yyrm/2024_liuji_tingli/18440-692815.html",
    "index": 1,
    "mp3_url": "https://774663576.github.io/br_media/tingli/2024_liuji_tingli/mp3/18440-692815.mp3",
    "category": "2024_liuji_tingli",
    "view_count": 1731
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
