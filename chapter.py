import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import os

# 基础URL和书籍页面URL的格式
base_url = "http://readingstuday.top"
book_page_url_format = base_url + "/page_{}.html"  # 使用格式化字符串来处理多个页面

# 存储所有章节信息的列表
chapter_data = []

# 遍历所有的页面，从1到32
for page_num in range(1, 2):
    # 构建当前页面的URL
    # book_page_url = book_page_url_format.format(page_num)
    book_page_url = 'https://www.shubang.net/book/?q=冰与火之歌'
    # 获取当前页面的内容并设置编码为utf-8
    response = requests.get(book_page_url)
    response.encoding = 'utf-8'  # 确保使用UTF-8编码

    # 解析页面内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找书籍链接（根据实际页面的结构，选择正确的class）
    book_links = soup.find_all('a', class_='book')

    # 遍历每个书籍链接，抓取章节信息
    for book_link in book_links:
        book_url = book_link.get('href')  # 获取书籍页面的URL
        
        # 使用urljoin合并基准URL和相对URL，生成完整的URL
        full_book_url = urljoin(book_page_url, book_url) 
        
        book_title = book_link.find('h3').get_text()  # 获取书籍标题
        
        # 提取bookid为书籍的HTML文件名（去掉文件扩展名）
        book_id = os.path.splitext(os.path.basename(book_url))[0]
        
        # 获取书籍页面内容并设置编码为utf-8
        book_page = requests.get(full_book_url)
        book_page.encoding = 'utf-8'  # 确保使用UTF-8编码
        book_soup = BeautifulSoup(book_page.text, 'html.parser')
        
        # 查找页面中的 <table> 标签（假设章节链接在表格内）
        chapter_table = book_soup.find('table', class_='cy wkbx')
        
        # 如果没有找到章节表格，跳过该书籍
        if not chapter_table:
            print(f"未找到章节表格，跳过书籍: {book_title}")
            continue
        
        # 在该表格内查找所有 <a> 标签，并提取 href 属性
        chapter_links = chapter_table.find_all('a', href=True)
        
        # 存储该书籍的所有章节信息
        for index, chapter in enumerate(chapter_links, start=1):  # 从1开始计数
            chapter_title = chapter.get_text().strip()  # 获取章节标题
            chapter_url = urljoin(full_book_url, chapter['href'])  # 获取章节的完整URL
            chapter_data.append({
                'chapter_number': index,  # 添加章节序号
                'bookid': book_id,  # 添加bookid字段
                'chapter_title': chapter_title,  # 修改字段名为chapter_title
                'chapter_url': chapter_url  # 修改字段名为chapter_url
            })

# 将所有章节信息写入 JSON 文件
with open('book_chapters.json', 'w', encoding='utf-8') as f:
    json.dump(chapter_data, f, ensure_ascii=False, indent=4)

print("章节信息已保存到 book_chapters.json 文件中。")
