import os
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import json
import traceback
import pymysql
import paramiko
import random
import time
from urllib.parse import quote
from html import unescape

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
    'remote_path': '/home/book/10_minute_english'
}

def download_and_save_image(image_url, article_id):
    """下载图片并保存到服务器"""
    try:
        # 下载图片
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # 获取文件扩展名
        ext = image_url.split('.')[-1]
        if '?' in ext:
            ext = ext.split('?')[0]
        filename = f"{article_id}.{ext}"
        
        # 本地临时保存
        local_img_dir = os.path.join('10_minute_english', 'img')
        if not os.path.exists(local_img_dir):
            os.makedirs(local_img_dir)
            
        local_path = os.path.join(local_img_dir, filename)
        with open(local_path, 'wb') as f:
            f.write(response.content)
            
        # 上传到服务器
        transport = paramiko.Transport((SERVER_CONFIG['hostname'], 22))
        transport.connect(username=SERVER_CONFIG['username'], password=SERVER_CONFIG['password'])
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # 确保远程目录存在
        remote_img_dir = SERVER_CONFIG['remote_path'] + '/img'
        try:
            sftp.stat(remote_img_dir)
        except IOError:
            sftp.mkdir(remote_img_dir)
            
        remote_path = f"{remote_img_dir}/{filename}"
        sftp.put(local_path, remote_path)
        
        sftp.close()
        transport.close()
        
        # 返回图片的URL
        return f"http://readingstuday.top/10_minute_english/img/{filename}"
        
    except Exception as e:
        print(f"下载和保存图片失败: {e}")
        traceback.print_exc()
        return None

def search_pixabay_image(query, article_id):
    """从Pixabay搜索相关图片并保存"""
    try:
        # Pixabay API配置
        api_key = "48439108-45c403e837503d7b07b791295"
        search_url = "https://pixabay.com/api/"
        
        # 优先使用英文搜索
        search_term = query.split('=')[-1].strip()  # 提取英文标题
        
        # 构建参数
        params = {
            "key": api_key,
            "q": search_term,
            "lang": "en",
            "image_type": "photo",
            "orientation": "horizontal",
            "per_page": 3,
            "min_width": 800,
            "min_height": 600,
            "safesearch": "true",
        }
        
        print(f"使用英文关键词搜索图片: {search_term}")
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        results = response.json()
        if results["totalHits"] > 0:
            image_url = results["hits"][0]["largeImageURL"]
            image_url = image_url.replace("_1280", "_480")
            return download_and_save_image(image_url, article_id)
            
        # 如果英文搜索没结果，尝试使用中文
        print("英文搜索无结果，尝试中文搜索...")
        chinese_term = query.split('=')[0].strip()
        params["q"] = chinese_term
        params["lang"] = "zh"
        
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        results = response.json()
        if results["totalHits"] > 0:
            image_url = results["hits"][0]["largeImageURL"]
            image_url = image_url.replace("_1280", "_480")
            return download_and_save_image(image_url, article_id)
            
    except Exception as e:
        print(f"搜索图片失败: {e}")
        traceback.print_exc()
    return None
def get_web_content(url, max_retries=3):
    """获取网页内容，增加重试机制"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for attempt in range(max_retries):
        try:
            print(f"正在获取页面内容: {url} (尝试 {attempt + 1}/{max_retries})")
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            print("页面内容获取成功")
            return response.text
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"获取页面失败: {e}")
                traceback.print_exc()
                return None
            print(f"尝试失败，等待重试... ({e})")
            time.sleep(2)

def extract_article_info(html_content, url):
    """从HTML中提取文章信息"""
    try:
        print("\n开始解析文章内容...")
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 提取ID
        article_id = ''
        url_match = re.search(r'show-\d+-(\d+)-1\.html', url)
        if url_match:
            article_id = url_match.group(1)
        print(f"提取到文章ID: {article_id}")
        
        # 提取音频URL
        audio_url = ''
        audio_element = soup.find('audio', id='mediaPlayId')
        if audio_element:
            audio_url = audio_element.get('m-src', '')
        print(f"提取到音频URL: {audio_url}")
        
        # 提取文章内容
        content_div = soup.new_tag('div')
        content_div['class'] = 'article-content'
        
        # 找到内容区域
        content_box = soup.find('div', class_='Contentbox2')
        
        # 初始化图片URL
        image_url = ''
        
        # 提取标题
        title = ''
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            content = meta_desc.get('content', '')
            chinese_start = -1
            for i, char in enumerate(content):
                if '\u4e00' <= char <= '\u9fff':
                    chinese_start = i
                    break
            
            if chinese_start > 0:
                english_title = content[:chinese_start].strip()
                # 解码HTML实体
                english_title = unescape(english_title)
                english_start = -1
                for i in range(chinese_start, len(content)):
                    if content[i].isascii() and content[i].isalpha():
                        english_start = i
                        break
                
                if english_start > chinese_start:
                    chinese_title = content[chinese_start:english_start].strip()
                    chinese_title = unescape(chinese_title)  # 同样解码中文部分
                    title = f"{chinese_title} = {english_title}"
                    print(f"从meta description提取到标题: {title}")
        
        if content_box:
            # 处理所有段落
            has_image = False
            # 先处理直接的strong标签内容
            direct_strong = content_box.find('strong', recursive=False)
            if direct_strong:
                text = direct_strong.text.strip()
                if text:
                    new_p = soup.new_tag('p')
                    new_p['style'] = 'text-indent: 2em; line-height: 1.75em; margin-bottom: 15px; margin-top: 15px;'
                    span = soup.new_tag('span')
                    span['style'] = 'font-size: 14px; font-family: 宋体, SimSun;'
                    span.string = text
                    new_p.append(span)
                    content_div.append(new_p)

            # 处理其他段落
            for p in content_box.find_all(['p', 'div']):
                text = p.get_text().strip()
                if text:  # 只处理非空内容
                    new_p = soup.new_tag('p')
                    new_p['style'] = 'text-indent: 2em; line-height: 1.75em; margin-bottom: 15px; margin-top: 15px;'
                    span = soup.new_tag('span')
                    span['style'] = 'font-size: 14px; font-family: 宋体, SimSun;'
                    span.string = text
                    new_p.append(span)
                    content_div.append(new_p)
                                    # 处理图片
                img = p.find('img')
                if img and img.get('src'):
                    has_image = True
                    img_url = img['src']
                    if not img_url.startswith('http'):
                        img_url = 'https:' + img_url if img_url.startswith('//') else 'https://' + img_url
                    
                    # 保存第一张图片URL作为文章封面
                    if not image_url:
                        # 下载并保存图片
                        saved_image_url = download_and_save_image(img_url, article_id)
                        if saved_image_url:
                            image_url = saved_image_url
                            print(f"提取到封面图片: {image_url}")
                    
                    new_p = soup.new_tag('p')
                    new_p['style'] = 'text-align: center;'
                    new_img = soup.new_tag('img')
                    new_img['src'] = image_url  # 使用保存后的图片URL
                    new_img['style'] = 'max-width: 100%; height: auto; margin: 10px 0;'
                    new_p.append(new_img)
                    content_div.append(new_p)
            
            # 如果文章没有图片，尝试搜索相关图片
            if not has_image and title:
                print("文章没有图片，尝试搜索相关图片...")
                image_url = search_pixabay_image(title, article_id)
                
                if image_url:
                    print(f"找到相关图片: {image_url}")
                    # 添加找到的图片到文章内容
                    new_p = soup.new_tag('p')
                    new_p['style'] = 'text-align: center;'
                    new_img = soup.new_tag('img')
                    new_img['src'] = image_url
                    new_img['style'] = 'max-width: 100%; height: auto; margin: 10px 0;'
                    new_p.append(new_img)
                    # 将图片插入到标题后面
                    content_div.insert(2, new_p)
                else:
                    print("未找到相关图片")
        
        # 生成随机访问量
        views = random.randint(1000, 10000)
        
        # 构建文章数据
        article_data = {
            'id': article_id,
            'title': title,
            'url': f'http://readingstuday.top/10_minute_english/{article_id}.html',
            'date': '2025-02-02',
            'audio': audio_url,
            'image': image_url,
            'update_time': '2025-02-02',
            'views': views
        }
        
        return article_data, str(content_div)
        
    except Exception as e:
        print(f"提取文章信息时出错: {e}")
        traceback.print_exc()
        return None, None

def save_article_html(article_id, content):
    """保存文章HTML内容到文件"""
    try:
        if not os.path.exists('10_minute_english'):
            os.makedirs('10_minute_english')
            print("创建10_minute_english目录成功")
            
        html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>10 Minute English {article_id}</title>
        <link rel="stylesheet" href="./style.css">
    </head>
    <body>
        {content}
        <script src="./script.js"></script>
    </body>
</html>'''
            
        file_path = f'10_minute_english/{article_id}.html'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"\nHTML内容已保存到: {os.path.abspath(file_path)}")
        
    except Exception as e:
        print(f"保存HTML内容失败: {e}")
        traceback.print_exc()
def upload_to_server(local_dir, filename):
    """上传文件到服务器"""
    try:
        transport = paramiko.Transport((SERVER_CONFIG['hostname'], 22))
        transport.connect(username=SERVER_CONFIG['username'], password=SERVER_CONFIG['password'])
        
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # 确保远程目录存在
        try:
            sftp.stat(SERVER_CONFIG['remote_path'])
        except IOError:
            sftp.mkdir(SERVER_CONFIG['remote_path'])
        
        # 上传文件
        local_path = os.path.join(local_dir, filename)
        remote_path = os.path.join(SERVER_CONFIG['remote_path'], filename)
        
        sftp.put(local_path, remote_path)
        
        sftp.close()
        transport.close()
        return True
        
    except Exception as e:
        print(f"上传文件失败: {e}")
        traceback.print_exc()
        return False

def change_permissions():
    """修改服务器上文件的权限"""
    try:
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

def save_to_database(article_data):
    """保存文章到数据库"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            # 检查文章是否已存在
            check_sql = "SELECT id FROM 10_minute_english WHERE id = %s"
            print(f"\n执行检查SQL: {check_sql}")
            print(f"参数: {article_data['id']}")
            
            cursor.execute(check_sql, (article_data['id'],))
            exists = cursor.fetchone()
            
            if exists:
                print(f"文章 {article_data['id']} 已存在，跳过保存")
                return False
                
            sql = """
            INSERT INTO 10_minute_english (
                id, title, url, date, audio, image, 
                update_time, views
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
            params = (
                article_data['id'],
                article_data['title'],
                article_data['url'],
                article_data['date'],
                article_data['audio'],
                article_data['image'],
                article_data['update_time'],
                article_data['views']
            )
            
            print("\n执行插入SQL:")
            print(sql)
            print("\n参数值:")
            print(json.dumps({
                'id': article_data['id'],
                'title': article_data['title'],
                'url': article_data['url'],
                'date': article_data['date'],
                'audio': article_data['audio'],
                'image': article_data['image'],
                'update_time': article_data['update_time'],
                'views': article_data['views']
            }, ensure_ascii=False, indent=4))
            
            cursor.execute(sql, params)
            
        conn.commit()
        print(f"\n文章 {article_data['id']} 已成功保存到数据库")
        return True
        
    except Exception as e:
        print(f"保存到数据库失败: {e}")
        traceback.print_exc()
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def upload_files(article_data):
    """上传文件到服务器并更新权限"""
    try:
        print("\n开始上传文件到服务器...")
        
        filename = f"{article_data['id']}.html"
        if os.path.exists(f"10_minute_english/{filename}"):
            if upload_to_server('10_minute_english', filename):
                print(f"成功上传: {filename}")
                change_permissions()
                return True
            else:
                print(f"上传失败: {filename}")
                return False
        else:
            print(f"文件不存在: 10_minute_english/{filename}")
            return False
            
    except Exception as e:
        print(f"上传过程出错: {e}")
        traceback.print_exc()
        return False

def main(url):
    """主函数"""
    try:
        print(f"\n开始处理文章...")
        print(f"URL: {url}")
        
        html_content = get_web_content(url)
        if not html_content:
            print("获取网页内容失败")
            return None
            
        article_data, cleaned_html = extract_article_info(html_content, url)
        if article_data and cleaned_html:
            print("\n文章信息提取完成!")
            
            save_article_html(article_data['id'], cleaned_html)
            
            if upload_files(article_data):
                if save_to_database(article_data):
                    print("\n文章处理完成!")
                    return article_data
                else:
                    print("\n保存到数据库失败!")
            else:
                print("\n上传文件失败!")
                
        return None
            
    except Exception as e:
        print(f"处理文章时出错: {e}")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    article_url = "https://m.tingclass.net/show-8754-291457-1.html"
    
    print("=" * 50)
    print("10分钟英语文章处理程序")
    print("=" * 50)
    
    article_data = main(article_url)
    
    if article_data:
        print("\n处理结果:")
        print("=" * 50)
        print("文章数据:")
        print(json.dumps(article_data, ensure_ascii=False, indent=4))
    else:
        print("\n处理失败!")