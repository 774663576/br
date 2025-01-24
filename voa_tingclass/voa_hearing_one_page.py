import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime
import os
import pymysql
from pymysql.cursors import DictCursor
import paramiko
import random

# 全局变量
translation_available = True

# 数据库配置
DB_CONFIG = {
   'host': '59.110.149.111',
    'user': 'root',
    'password': 'SP123456!',
    'db': 'reading'
}

# 服务器配置
SERVER_CONFIG = {
    'hostname': '59.110.149.111',
    'username': 'root',
    'password': '<172.reading>',
    'remote_path': '/home/book/voa'
}

def get_translation(text):
    """获取文本的英文翻译"""
    global translation_available
    
    # 如果翻译服务已标记为不可用，直接返回空字符串
    if not translation_available:
        return ''
        
    try:
        url = f'https://api.mymemory.translated.net/get?q={text}&langpair=zh|en'
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # 获取翻译结果
        translated_text = data.get('responseData', {}).get('translatedText', '')
        
        # 检查是否包含错误信息关键词
        error_keywords = ['MYMEMORY WARNING', 'YOU USED ALL', 'AVAILABLE FREE TRANSLATIONS']
        if any(keyword in translated_text.upper() for keyword in error_keywords):
            print("翻译服务配额已用尽，停止后续翻译")
            translation_available = False
            return ''
            
        # 只有在没有警告信息的情况下才返回翻译结果
        if data.get('responseStatus') == 200 and translated_text:
            return translated_text
        else:
            return ''
            
    except Exception as e:
        print(f"获取翻译失败: {e}")
        return ''

def get_web_content(url, retry_times=3):
    """获取网页内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for i in range(retry_times):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            print(f"第{i+1}次获取失败: {e}")
            if i < retry_times - 1:
                print("等待2秒后重试...")
                time.sleep(2)
            else:
                print(f"获取页面 {url} 失败")
    return None

def save_to_database(articles):
    """保存文章到数据库"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            # 获取当前时间
            current_time = datetime.now().strftime('%Y-%m-%d')
            
            for article in articles:
                # 生成随机views数值
                views = random.randint(5000, 10000)

                # 检查文章是否已存在
                check_sql = "SELECT id FROM articles WHERE id = %s"
                cursor.execute(check_sql, (article['id'],))
                exists = cursor.fetchone()
                
                if exists:
                    continue
                else:
                    # 插入新文章
                    sql = """
                    INSERT INTO articles (
                        id, title, url, date, audio, image, category, 
                        update_time, views, vocabulary_count, voa_type
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    """
                    cursor.execute(sql, (
                        article['id'],
                        article['title'],
                        article['url'],
                        article['date'],
                        article['audio'],
                        article['image'],
                        '',  # category 默认为空
                        current_time,
                        views,
                        0,   # vocabulary_count 默认为0
                        'voa_changsu'  # voa_type 固定值
                    ))
        conn.commit()
        conn.close()
        print(f"成功保存 {len(articles)} 篇文章到数据库")
    except Exception as e:
        print(f"保存到数据库失败: {e}")
        if 'conn' in locals():
            conn.close()

def upload_to_server(local_path, filename):
    """上传文件到服务器"""
    try:
        transport = paramiko.Transport((SERVER_CONFIG['hostname'], 22))
        transport.connect(username=SERVER_CONFIG['username'], password=SERVER_CONFIG['password'])
        
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # 确保远程目录存在
        try:
            sftp.stat(SERVER_CONFIG['remote_path'])
        except FileNotFoundError:
            print(f"创建远程目录: {SERVER_CONFIG['remote_path']}")
            sftp.mkdir(SERVER_CONFIG['remote_path'])
        
        # 上传文件
        remote_file = f"{SERVER_CONFIG['remote_path']}/{filename}"
        sftp.put(f"{local_path}/{filename}", remote_file)
        
        sftp.close()
        transport.close()
        return True
    except Exception as e:
        print(f"上传文件 {filename} 失败: {e}")
        return False

def change_permissions():
    """修改服务器上文件的权限"""
    try:
        print("\n正在修改文件权限...")
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh.connect(
            hostname=SERVER_CONFIG['hostname'],
            username=SERVER_CONFIG['username'],
            password=SERVER_CONFIG['password']
        )
        
        command = f"chmod -R 755 {SERVER_CONFIG['remote_path']}"
        stdin, stdout, stderr = ssh.exec_command(command)
        
        error = stderr.read().decode()
        if error and 'password' not in error.lower():
            print(f"修改权限时出错: {error}")
        else:
            print("文件权限修改成功")
        
        ssh.close()
        
    except Exception as e:
        print(f"修改文件权限失败: {e}")

def upload_files(latest_articles):
    """只上传最新文章的HTML文件到服务器"""
    try:
        print("\n开始上传最新文章到服务器...")
        
        success_count = 0
        fail_count = 0
        
        for article in latest_articles:
            filename = f"{article['id']}.html"
            if os.path.exists(f"voa/{filename}"):
                if upload_to_server('voa', filename):
                    success_count += 1
                    print(f"成功上传: {article['title']}")
                else:
                    fail_count += 1
                    print(f"上传失败: {article['title']}")
        
        print(f"\n文件上传完成:")
        print(f"成功: {success_count} 个文件")
        print(f"失败: {fail_count} 个文件")
        
        if success_count > 0:
            change_permissions()
        
    except Exception as e:
        print(f"上传过程出错: {e}")

def clean_article_content(content_div):
    """清理文章内容，去掉不需要的部分"""
    if not content_div:
        return content_div
        
    try:
        # 找到第一张图片
        first_img = content_div.find('img')
        if first_img:
            # 获取包含图片的p标签
            img_p = first_img.find_parent('p')
            if img_p:
                # 删除图片之前的所有内容
                for tag in img_p.previous_siblings:
                    tag.decompose()
        
        # 找到所有段落
        paragraphs = content_div.find_all('p')
        if paragraphs:
            # 找到最后一个段落
            last_p = paragraphs[-1]
            if last_p and '以上便是' in last_p.text:
                last_p.decompose()
                
        # 清理所有段落的样式
        for p in content_div.find_all('p'):
            # 保留text-indent和text-align
            style = p.get('style', '')
            new_style = []
            if 'text-indent' in style:
                new_style.append('text-indent: 2em')
            if 'text-align: center' in style:
                new_style.append('text-align: center')
            if new_style:
                p['style'] = '; '.join(new_style)
            else:
                del p['style']
                
    except Exception as e:
        print(f"清理文章内容时出错: {e}")
        
    return content_div

def save_article_html(article_id, content):
    """保存文章HTML内容"""
    if not content:
        print(f"文章 {article_id} 内容为空，跳过保存")
        return
        
    html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VOA Article {article_id}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="article-content">
        {content}
    </div>
<script src="script.js" ></script>
</body>
</html>'''
    
    try:
        with open(f'voa/{article_id}.html', 'w', encoding='utf-8') as f:
            f.write(html_template)
    except Exception as e:
        print(f"保存文章 {article_id} HTML内容失败: {e}")

def parse_article_content(article_url, article_id):
    """解析文章详情页，获取音频、图片和HTML内容"""
    try:
        html_content = get_web_content(article_url)
        if not html_content:
            return None, None
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 获取音频地址
        audio = soup.find('audio')
        audio_url = audio.get('m-src') if audio else ''
        
        # 获取第一张图片地址
        image_url = ''
        content_div = soup.find('div', class_='tabbody')
        if content_div:
            img = content_div.find('img')
            if img and img.get('src'):
                image_url = img['src']
            
            # 清理和保存文章内容
            try:
                cleaned_content = clean_article_content(content_div)
                if cleaned_content:
                    save_article_html(article_id, str(cleaned_content))
            except Exception as e:
                print(f"处理文章 {article_id} 内容时出错: {e}")
        
        return audio_url, image_url
    except Exception as e:
        print(f"解析文章 {article_id} 时出错: {e}")
        return None, None

def parse_voa_list(url):
    """解析VOA文章列表 - 只抓取第一页"""
    start_time = time.time()
    
    if not os.path.exists('voa'):
        os.makedirs('voa')
    
    print("正在获取首页内容...")
    html_content = get_web_content(url)
    if not html_content:
        print("获取首页失败，程序退出")
        return []
    
    all_articles = []
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        articles_on_page = 0
        for li in soup.find_all('li'):
            link = li.find('a', class_='tittle')
            if not link:
                continue
                
            article_url = link.get('href', '')
            title = link.text.strip()
            
            date_span = li.find('span', class_='num')
            date = date_span.text.strip('()') if date_span else ''
            
            # 提取文章ID
            article_id = ''
            id_param = re.search(r'[?&]id=(\d+)', article_url)
            if id_param:
                article_id = id_param.group(1)
            else:
                id_path = re.search(r'show-\d+-(\d+)-\d+\.html', article_url)
                if id_path:
                    article_id = id_path.group(1)
            
            if not article_id:
                print(f"无法获取文章ID，跳过: {article_url}")
                continue
            
            # 处理标题
            title = re.sub(r'\([0-9-]+\)', '', title).strip()
            title = title.split('：')[-1].strip()
            
            # 获取英文翻译
            english_title = get_translation(title)
            # 组合标题格式：中文 = 英文
            full_title = f"{title} = {english_title}" if english_title else title
            
            print(f"正在获取文章 {article_id} - {full_title} 的内容...")
            audio_url, image_url = parse_article_content(article_url, article_id)
            
            article_data = {
                'id': article_id,
                'url': f'http://readingstuday.top/voa/{article_id}.html',
                'title': full_title,
                'date': date,
                'audio': audio_url,
                'image': image_url
            }
            
            all_articles.append(article_data)
            articles_on_page += 1
            
            # 添加随机延迟，避免请求过快
            time.sleep(random.uniform(1, 3))
        
        print(f"完成，获取到 {articles_on_page} 篇文章")
        
    except Exception as e:
        print(f"处理文章列表时出错: {e}")
    
    total_time = time.time() - start_time
    print(f"\n抓取完成！")
    print(f"总用时: {total_time:.2f} 秒")
    print(f"总文章数: {len(all_articles)} 篇")
    
    return all_articles

def main():
    """主函数"""
    try:
        if not os.path.exists('voa'):
            os.makedirs('voa')
            
        url = "https://m.tingclass.net/list-10616-1.html"
        results = parse_voa_list(url)
        
        if results:
            print("\n保存统计:")
            print(f"HTML文件保存在: voa/ 目录")
            print(f"总文章数: {len(results)}")
            
            # 首先检查哪些是新文章
            conn = pymysql.connect(**DB_CONFIG)
            with conn.cursor() as cursor:
                new_articles = []
                for article in results:
                    sql = "SELECT id FROM articles WHERE id = %s"
                    cursor.execute(sql, (article['id'],))
                    exists = cursor.fetchone()
                    if not exists:
                        new_articles.append(article)
            conn.close()
            
            # 如果有新文章，先上传文件，再保存到数据库
            if new_articles:
                print(f"\n发现 {len(new_articles)} 篇新文章")
                upload_files(new_articles)
                # 上传完成后再保存到数据库
                save_to_database(results)
                print("新文章已保存到数据库")
            else:
                print("\n没有发现新文章，无需上传")
            
            print("\n最新5篇文章预览:")
            sorted_articles = sorted(results, key=lambda x: x['date'], reverse=True)
            for article in sorted_articles[:5]:
                print(f"日期: {article['date']}")
                print(f"标题: {article['title']}")
                print(f"ID: {article['id']}")
                print(f"URL: {article['url']}")
                print(f"音频: {article['audio']}")
                print(f"图片: {article['image']}")
                print("-" * 50)
                
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序执行出错: {e}")

if __name__ == "__main__":
    main()