import os
import json
import mysql.connector

# 连接到 MySQL 数据库
conn = mysql.connector.connect(
    host='59.110.149.111',
    user='root',
    password='SP123456!',
    database='reading'
)
cursor = conn.cursor()

# 你的 JSON 文件所在的文件夹路径
json_folder_path = '/Users/songbinbin/Downloads/reading_app/book/read_book/voa_tingclass/情景对话/crawler_data'

# 使用 os.walk() 遍历文件夹及其子文件夹
for root, dirs, files in os.walk(json_folder_path):
    for filename in files:
        if filename.endswith(".json"):
            file_path = os.path.join(root, filename)
            print(f"正在处理文件: {file_path}")  # 打印处理的文件路径

            # 读取 JSON 文件
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"成功读取文件: {file_path}")  # 文件读取成功的日志
            except Exception as e:
                print(f"读取文件 {file_path} 时出错: {e}")  # 读取文件出错的日志
                continue

            # 遍历每个 JSON 对象并插入到数据库
            for item in data:
                for conversation in item.get('conversations', []):
                    try:
                        cursor.execute('''
                            INSERT INTO situational_conversation 
                            (parent_category, category, category_title, cid, title, conversation_english, conversation_chinese, reply_english, reply_chinese)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ''', (
                            item['parent_category'],
                            item['category'],
                            item['category_title'],
                            item['cid'],
                            item['title'],
                            conversation['english'],
                            conversation['chinese'],
                            conversation['reply_english'],
                            conversation['reply_chinese']
                        ))
                        print(f"成功插入数据: {item['title']}-----{ conversation['english']}")  # 打印插入成功的日志
                    except Exception as e:
                        print(f"插入数据时出错: {e}")  # 插入数据出错的日志

# 提交并关闭连接
conn.commit()
print("数据提交成功。")  # 数据提交成功的日志

cursor.close()
conn.close()
print("数据库连接已关闭。")  # 数据库连接关闭的日志
