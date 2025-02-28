import os
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime, timedelta
import json
import traceback
import pymysql
import paramiko
import random
import time
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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
    'remote_path': '/home/book/tingli/bbc-news'
}
base_dir='可可英语/BBC-每日新闻'
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
        local_img_dir = os.path.join(base_dir, 'img')
        if not os.path.exists(local_img_dir):
            os.makedirs(local_img_dir)
            
        local_path = os.path.join(local_img_dir, filename)
        with open(local_path, 'wb') as f:
            f.write(response.content)
            
        # # 上传到服务器
        # transport = paramiko.Transport((SERVER_CONFIG['hostname'], 22))
        # transport.connect(username=SERVER_CONFIG['username'], password=SERVER_CONFIG['password'])
        # sftp = paramiko.SFTPClient.from_transport(transport)
        
        # # 确保远程目录存在
        # remote_img_dir = SERVER_CONFIG['remote_path'] + '/img'
        # try:
        #     sftp.stat(remote_img_dir)
        # except IOError:
        #     sftp.mkdir(remote_img_dir)
            
        # remote_path = f"{remote_img_dir}/{filename}"
        # sftp.put(local_path, remote_path)
        
        # sftp.close()
        # transport.close()
        
        # 返回图片的URL
        return f"https://774663576.github.io/br_media/tingli/bbc-news/img/{filename}"
        
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

def translate_text(text):
    """使用MyMemory API翻译文本"""
    if not text:
        return ''
        
    try:
        # 对文本进行URL编码
        encoded_text = quote(text)
        url = f'https://api.mymemory.translated.net/get?q={encoded_text}&langpair=zh|en'
        
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # 获取翻译结果
        translated_text = data.get('responseData', {}).get('translatedText', '')
        if translated_text:
            # 清理翻译结果
            translated_text = translated_text.strip()
            # 移除可能的HTML实体
            translated_text = re.sub(r'&[a-zA-Z]+;', '', translated_text)
            return translated_text
            
    except Exception as e:
        print(f"翻译失败: {e}")
        
    return ''

def get_web_content(url):
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # 自动管理ChromeDriver
    service = Service(ChromeDriverManager().install())
    
    # 创建浏览器驱动
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # 打开网页
        driver.get(url)
        
        # 等待页面完全加载
        driver.implicitly_wait(10)
        
        # 滚动页面，触发懒加载
        total_height = driver.execute_script("return document.body.scrollHeight")
        for i in range(0, total_height, 500):
            driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(0.5)  # 短暂停顿，让内容加载
        
        # 获取完整页面源码
        full_content = driver.page_source
        
        return full_content
    
    except Exception as e:
        print(f"获取完整页面内容失败: {e}")
        return None
    finally:
        driver.quit()

def clean_article_content(content_div):
    """清理文章内容，去掉不需要的部分"""
    if not content_div:
        return content_div
        
    try:
        # 找到 Contentbox2 div
        content_box = content_div.find('div', class_='caption-box')
        if not content_box:
            return content_div
            
        # 删除最后一段"以上便是..."的内容
        paragraphs = content_box.find_all('p')
        if paragraphs:
            last_p = paragraphs[-1]
            if last_p and '以上便是' in last_p.text:
                last_p.decompose()
        
        # 删除图片上面的内容
        first_img = content_box.find('img')
        if first_img:
            # 找到包含图片的p标签
            img_p = first_img.find_parent('p')
            if img_p:
                # 删除图片之前的所有段落
                for p in img_p.find_previous_siblings('p'):
                    p.decompose()
                    
        # 确保所有段落都有正确的样式
        for p in content_box.find_all('p'):
            # 确保段落有正确的缩进和行高
            style = p.get('style', '')
            styles = []
            if 'text-indent' not in style:
                styles.append('text-indent: 2em')
            if 'line-height' not in style:
                styles.append('line-height: 1.75em')
            if 'margin-bottom' not in style:
                styles.append('margin-bottom: 15px')
            if 'margin-top' not in style:
                styles.append('margin-top: 15px')
            
            if styles:
                if style:
                    style = style.rstrip(';') + '; ' + '; '.join(styles)
                else:
                    style = '; '.join(styles)
                p['style'] = style
                
            # 确保span标签有正确的字体和大小
            for span in p.find_all('span'):
                if 'style' not in span.attrs:
                    span['style'] = 'font-size: 14px; font-family: 宋体, SimSun;'
                    
    except Exception as e:
        print(f"清理文章内容时出错: {e}")
        traceback.print_exc()
        
    return content_div

def save_article_html(article_id, content):
    """保存文章HTML内容到文件"""
    try:
        # 确保voa目录存在
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
            print("创建可可英语目录成功")
            
        # HTML模板
        html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VOA Article {article_id}</title>
        <link rel="stylesheet" href="./style.css">
    </head>
    <body>
        <div class="article-content">
            {content}
        </div>
        <script src="./script.js"></script>
    </body>
</html>'''
            
        # 保存文件
        file_path = f'{base_dir}/{article_id}.html'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"\nHTML内容已保存到: {os.path.abspath(file_path)}")
        
    except Exception as e:
        print(f"保存HTML内容失败: {e}")
        traceback.print_exc()

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

def save_to_database(article_data, publish_date):
    """保存文章到数据库"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            # 检查文章是否已存在
            check_sql = "SELECT article_id FROM bbc_news WHERE article_id = %s"
            cursor.execute(check_sql, (article_data['id'],))
            exists = cursor.fetchone()
            
            if exists:
                print(f"文章 {article_data['id']} 已存在，跳过保存")
                return True
                
            # 生成随机views数值
            views = random.randint(5000, 10000)
            
            # 插入新文章
            sql = """
            INSERT INTO bbc_news (
                article_id, title, url, date, audio, image, views
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s
            )
            """
            cursor.execute(sql, (
                article_data['id'],
                article_data['title'],
                article_data['url'],
                publish_date,  # 使用用户输入的日期
                article_data['audio'],
                article_data['image'], 
                views
            ))
            
        conn.commit()
        print(f"文章 {article_data['id']} 已保存到数据库")
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
        if os.path.exists(f"{base_dir}/{filename}"):
            if upload_to_server(base_dir, filename):
                print(f"成功上传: {filename}")
                # 修改文件权限
                change_permissions()
                return True
            else:
                print(f"上传失败: {filename}")
                return False
        else:
            print(f"文件不存在: {base_dir}/{filename}")
            return False
            
    except Exception as e:
        print(f"上传过程出错: {e}")
        traceback.print_exc()
        return False
        
def download_mp3(audio_url, article_id):
    """下载MP3文件并保存"""
    try:
        if not audio_url:
            print("没有找到音频URL")
            return None
            
        # 创建音频目录
        audio_dir = os.path.join(base_dir, 'mp3')
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
            
        # 下载音频文件
        response = requests.get(audio_url, timeout=10)
        response.raise_for_status()
        
        # 保存文件
        filename = f"{article_id}.mp3"
        local_path = os.path.join(audio_dir, filename)
        
        with open(local_path, 'wb') as f:
            f.write(response.content)
            
        print(f"音频文件已保存到: {os.path.abspath(local_path)}")
        
        return f"https://774663576.github.io/br_media/tingli/bbc-news/mp3/{filename}"
        
    except Exception as e:
        print(f"下载音频文件失败: {e}")
        traceback.print_exc()
        return None

def extract_article_info(html_content, article_url):
    """从HTML中提取文章信息"""
    try:
        print("\n开始解析文章内容...")
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 提取标题并打印每一步
        title = ''
        title_div = soup.find('div', class_='player-title')
        if title_div:
            print(f"原始标题文本: {title_div.text}")  # 打印原始文本
            title = title_div.text.strip()
        print(f"提取到标题: {title}")
        
        # 翻译标题
        english_title = translate_text(title)
        if english_title:
            print(f"翻译后的标题: {english_title}")
            # 组合标题格式：中文 = 英文
            full_title = f"{title} = {english_title}"
        else:
            print("标题翻译失败，使用原标题")
            full_title = title
            
        print(f"最终标题: {full_title}")
        
        # 提取ID
        article_id = article_url.split('/')[-1]

        print(f"提取到文章ID: {article_id}")
        
        # 提取音频URL
        audio_element = soup.find('audio', id='xplayer_audio')
        audio_url = audio_element['src'] if audio_element else ''

        mp3_url = download_mp3(audio_url, article_id)
        if mp3_url:
            audio_url = mp3_url
        print(f"提取到音频URL: {audio_url}")
        
        # 提取文章内容和图片
        content_div = soup.find('div', class_='caption-box')
        
        image_url = search_pixabay_image(title, article_id)
                
        print(f"提取到图片URL: {image_url}")
        
        # 构建文章数据
        article_data = {
            'id': article_id,
            'title': full_title,  # 使用组合后的标题
            'url': f'http://readingstuday.top/tingli/bbc-news/{article_id}.html',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'audio': audio_url,
            'image': image_url
        }
        print("article_data:")
        print(json.dumps(article_data, ensure_ascii=False, indent=4))  # 格式化输出 article_data

        return article_data, str(content_div) if content_div else ''
        
    except Exception as e:
        print(f"提取文章信息时出错: {e}")
        traceback.print_exc()
        return None, None

def validate_date_format(date_string):
    """验证日期格式是否为YYYY-MM-DD"""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def main(url, publish_date):
    """主函数"""
    try:
        print(f"\n开始处理文章...")
        print(f"URL: {url}")
        print(f"发布日期: {publish_date}")
        
        # 获取网页内容
        html_content = get_web_content(url)
        if not html_content:
            print("获取网页内容失败")
            return None
            
        # 提取文章信息
        article_data, cleaned_html = extract_article_info(html_content, url)
        # print("cleaned_html:")
        # print(cleaned_html)
        if article_data and cleaned_html:
            print("\n文章信息提取完成!")
            
            # 保存HTML内容
            save_article_html(article_data['id'], cleaned_html)

            # 上传文件到服务器
            if upload_files(article_data):
                # 保存到数据库
                if save_to_database(article_data, publish_date):
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
    print("=" * 50)
    print("BBC-每日新闻")
    print("=" * 50)
    
    # 提示用户输入文章URL
    article_url = input("请输入要抓取的文章URL (例如: https://kekenet.com/lesson/18141-700641): ")
    
    # 验证输入的URL格式
    if not article_url.startswith("https://kekenet.com/"):
        print("错误: URL格式不正确，请输入有效的kekenet.com文章URL")
        exit(1)
    
    # 提示用户输入发布日期
    while True:
        publish_date = input("请输入文章发布日期 (格式: YYYY-MM-DD, 例如: 2025-02-21): ")
        if validate_date_format(publish_date):
            break
        else:
            print("错误: 日期格式不正确，请使用YYYY-MM-DD格式")
    
    article_data = main(article_url, publish_date)
    
    if article_data:
        print("\n处理结果:")
        print("=" * 50)
        print("文章数据:")
        print(json.dumps(article_data, ensure_ascii=False, indent=4))
    else:
        print("\n处理失败!")