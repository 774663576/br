import requests
from bs4 import BeautifulSoup
import re
import json
import os
import time

# 定义全局变量
CATEGORY = 'changyongkouyu'

def convert_to_mobile_url(url):
    """
    将课程详情页URL转换为移动版URL
    """
    if 'show-' in url and 'www.tingclass.net' in url:
        return url.replace('www.tingclass.net', 'm.tingclass.net')
    return url

def create_mobile_html(content, title):
    """
    创建适配移动端的HTML文档
    """
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{title}</title>
    <link rel="stylesheet" href="./style.css">
</head>
<body>
    <div class="content">
        {content}
    </div>
    <script src="./script.js"></script>
</body>
</html>'''

def extract_lesson_info(li_tag):
    """
    从li标签中提取课程信息
    """
    try:
        views = li_tag.find('em', class_='fr').text.replace('浏览：', '')
        
        a_tag = li_tag.find('a', class_='ell')
        if not a_tag:
            return None
            
        text = a_tag.get_text(strip=True)
        
        match = re.match(r'英语常用口语每天学\s+第(\d+)课[:：](.+)', text)


        if match:
            index, title = match.groups()
            # 构造新的URL格式
            new_url = f'http://readingstuday.top/kouyu/{CATEGORY}/{index}.html'
            return {
                'url': new_url,
                'index': index,
                'title': title,
                'views': int(views),
                'category': CATEGORY
            }
        
        return None
        
    except Exception as e:
        print(f"处理课程信息时出错: {e}")
        return None

def save_lesson_content(url, lesson_info):
    """
    获取并保存课程内容
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.tingclass.net/'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"获取课程内容失败，状态码: {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 从audio标签提取MP3地址
        audio_tag = soup.find('audio', {'id': 'mediaPlayId'})
        mp3_url = audio_tag.get('m-src') if audio_tag else None
        
        # 提取指定标签内容
        content_div = soup.find('div', {'id': 'con_ona_1'})
        if content_div:
            # 使用index作为文件名
            html_path = os.path.join(CATEGORY, f'{lesson_info["index"]}.html')
            
            # 创建移动端适配的HTML
            full_html = create_mobile_html(str(content_div), f'365天英语口语大全{lesson_info["index"]}.{lesson_info["title"]}')
            
            # 保存内容
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            return {
                'mp3_url': mp3_url
            }
        else:
            print(f"未找到内容标签: {lesson_info['index']}")
            return None
        
    except Exception as e:
        print(f"保存课程内容时出错: {e}")
        return None

def scrape_lessons(base_url):
    """
    抓取所有课程链接和内容
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.tingclass.net/'
    }
    
    all_lessons = []
    page = 1
    
    # 创建保存目录
    os.makedirs('365_kouyu', exist_ok=True)
    
    while True:
        url = f"{base_url}-{page}.html"
            
        try:
            print(f"正在抓取第 {page} 页... URL: {url}")
            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"请求失败，状态码: {response.status_code}")
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.select('#share_con .list-unit-1.list-qz li.clearfix')
            
            if not links:
                print(f"第 {page} 页没有找到链接，结束抓取")
                break
            
            valid_lessons = 0
            for link in links:
                lesson = extract_lesson_info(link)
                if lesson:
                    # 获取详情页内容
                    detail_url = convert_to_mobile_url(link.find('a', class_='ell').get('href'))
                    content_info = save_lesson_content(detail_url, lesson)
                    if content_info:
                        lesson.update(content_info)
                    
                    print(f"处理课程: {lesson['index']}.{lesson['title']}")
                    all_lessons.append(lesson)
                    valid_lessons += 1
            
            print(f'第 {page} 页抓取完成，找到 {valid_lessons} 个有效课程')
            
            if valid_lessons < 20:
                print("课程数量不足20，可能是最后一页，结束抓取")
                break
                
            page += 1
            time.sleep(2)
            
        except Exception as e:
            print(f'抓取第 {page} 页时出错: {e}')
            break
    
    # 保存课程信息到JSON
    if all_lessons:
        all_lessons.sort(key=lambda x: int(x['index']))
        with open('英语常用口语每天学.json', 'w', encoding='utf-8') as f:
            json.dump(all_lessons, f, ensure_ascii=False, indent=2)
        print(f"成功保存 {len(all_lessons)} 个课程信息")
    
    return all_lessons

def main():
    base_url = 'https://www.tingclass.net/list-8533'
    lessons = scrape_lessons(base_url)
    print(f"总共抓取到 {len(lessons)} 个课程")
    
    if not lessons:
        print("未能成功抓取任何课程，请检查网站地址是否正确或网站结构是否发生变化。")

if __name__ == '__main__':
    main()