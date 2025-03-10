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
    "url": "http://readingstuday.top/kouyu/abc_kouyu/1.html",
    "index": "1",
    "title": "lesson1",
    "views": 16517,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/1.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/2.html",
    "index": "2",
    "title": "lesson2",
    "views": 6437,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/2.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/3.html",
    "index": "3",
    "title": "lesson3",
    "views": 4368,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/3.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/4.html",
    "index": "4",
    "title": "lesson4",
    "views": 3021,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/4.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/5.html",
    "index": "5",
    "title": "lesson5",
    "views": 3262,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/5.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/6.html",
    "index": "6",
    "title": "lesson6",
    "views": 2842,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/6.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/7.html",
    "index": "7",
    "title": "lesson7",
    "views": 2552,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/7.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/8.html",
    "index": "8",
    "title": "lesson8",
    "views": 2510,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/8.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/9.html",
    "index": "9",
    "title": "lesson9",
    "views": 2599,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/9.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/10.html",
    "index": "10",
    "title": "lesson10",
    "views": 2473,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/10.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/11.html",
    "index": "11",
    "title": "lesson11",
    "views": 2140,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/11.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/12.html",
    "index": "12",
    "title": "lesson12",
    "views": 1990,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/12.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/13.html",
    "index": "13",
    "title": "lesson13",
    "views": 2025,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/13.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/14.html",
    "index": "14",
    "title": "lesson14",
    "views": 1888,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/14.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/15.html",
    "index": "15",
    "title": "lesson15",
    "views": 2006,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/15.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/16.html",
    "index": "16",
    "title": "lesson16",
    "views": 2211,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/16.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/17.html",
    "index": "17",
    "title": "lesson17",
    "views": 2047,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/17.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/18.html",
    "index": "18",
    "title": "lesson18",
    "views": 1863,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/18.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/19.html",
    "index": "19",
    "title": "lesson19",
    "views": 2074,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/19.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/20.html",
    "index": "20",
    "title": "lesson20",
    "views": 2310,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/20.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/21.html",
    "index": "21",
    "title": "lesson21",
    "views": 1925,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/21.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/22.html",
    "index": "22",
    "title": "lesson22",
    "views": 1738,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/22.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/23.html",
    "index": "23",
    "title": "lesson23",
    "views": 1678,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/23.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/24.html",
    "index": "24",
    "title": "lesson24",
    "views": 1760,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/24.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/25.html",
    "index": "25",
    "title": "lesson25",
    "views": 2050,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/25.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/26.html",
    "index": "26",
    "title": "lesson26",
    "views": 2175,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/26.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/27.html",
    "index": "27",
    "title": "lesson27",
    "views": 2085,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/27.mp3"
  },
  {
    "url": "http://readingstuday.top/kouyu/abc_kouyu/28.html",
    "index": "28",
    "title": "lesson28",
    "views": 3816,
    "category": "abc_kouyu",
    "mp3_url": "https://online2.tingclass.net/lesson/shi0529/0001/1297/28.mp3"
  }
]
# 插入数据的 SQL 语句
insert_query = """
INSERT INTO kouyu_365 (url, `index`, title, view_count, category, mp3_url)
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
