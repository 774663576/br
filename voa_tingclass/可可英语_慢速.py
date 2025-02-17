import os
import logging
from dataclasses import dataclass
from typing import Optional, Tuple, Dict
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

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 配置信息
TOMORROW_DATE = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

DB_CONFIG = {
    'host': '59.110.149.111',
    'user': 'root',
    'password': 'SP123456!',
    'db': 'reading'
}

SERVER_CONFIG = {
    'hostname': '59.110.149.111',
    'username': 'root',
    'password': '<172.reading>',
    'remote_path': '/home/book/voa/kk'
}

class ArticleProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def download_and_save_image(self, image_url: str, article_id: str) -> Optional[str]:
        """下载图片并保存到服务器"""
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            ext = image_url.split('.')[-1]
            if '?' in ext:
                ext = ext.split('?')[0]
            filename = f"{article_id}.{ext}"
            
            local_img_dir = os.path.join('10_minute_english', 'img')
            os.makedirs(local_img_dir, exist_ok=True)
            
            local_path = os.path.join(local_img_dir, filename)
            with open(local_path, 'wb') as f:
                f.write(response.content)

            self._upload_to_server(local_path, f"img/{filename}")
            
            return f"http://readingstuday.top/voa/kk/img/{filename}"
            
        except Exception as e:
            self.logger.error(f"下载和保存图片失败: {e}")
            return None

    def search_pixabay_image(self, query: str, article_id: str) -> Optional[str]:
        """从Pixabay搜索相关图片"""
        try:
            api_key = "48439108-45c403e837503d7b07b791295"
            search_url = "https://pixabay.com/api/"
            
            search_term = query.split('=')[-1].strip()
            
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
            
            self.logger.info(f"搜索图片关键词: {search_term}")
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            
            results = response.json()
            if results["totalHits"] > 0:
                image_url = results["hits"][0]["largeImageURL"]
                image_url = image_url.replace("_1280", "_480")
                return self.download_and_save_image(image_url, article_id)
                
            self.logger.info("尝试使用中文搜索...")
            chinese_term = query.split('=')[0].strip()
            params["q"] = chinese_term
            params["lang"] = "zh"
            
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            
            results = response.json()
            if results["totalHits"] > 0:
                image_url = results["hits"][0]["largeImageURL"]
                image_url = image_url.replace("_1280", "_480")
                return self.download_and_save_image(image_url, article_id)
                
        except Exception as e:
            self.logger.error(f"搜索图片失败: {e}")
        return None

    def translate_text(self, text: str) -> str:
        """翻译文本"""
        if not text:
            return ''
            
        try:
            encoded_text = quote(text)
            url = f'https://api.mymemory.translated.net/get?q={encoded_text}&langpair=zh|en'
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            translated_text = data.get('responseData', {}).get('translatedText', '')
            if translated_text:
                translated_text = translated_text.strip()
                translated_text = re.sub(r'&[a-zA-Z]+;', '', translated_text)
                return translated_text
                
        except Exception as e:
            self.logger.error(f"翻译失败: {e}")
            
        return ''

    def get_web_content(self, url: str) -> Optional[str]:
        """获取网页内容"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        
        service = Service(ChromeDriverManager().install())
        
        try:
            with webdriver.Chrome(service=service, options=chrome_options) as driver:
                driver.get(url)
                driver.implicitly_wait(10)
                
                total_height = driver.execute_script("return document.body.scrollHeight")
                for i in range(0, total_height, 500):
                    driver.execute_script(f"window.scrollTo(0, {i});")
                    time.sleep(0.5)
                
                return driver.page_source
                
        except Exception as e:
            self.logger.error(f"获取网页内容失败: {e}")
            return None

    def clean_article_content(self, content_div: BeautifulSoup) -> BeautifulSoup:
        """清理文章内容"""
        if not content_div:
            return content_div
            
        try:
            content_box = content_div.find('div', class_='caption-box')
            if not content_box:
                return content_div
                
            paragraphs = content_box.find_all('p')
            if paragraphs:
                last_p = paragraphs[-1]
                if last_p and '以上便是' in last_p.text:
                    last_p.decompose()
            
            first_img = content_box.find('img')
            if first_img:
                img_p = first_img.find_parent('p')
                if img_p:
                    for p in img_p.find_previous_siblings('p'):
                        p.decompose()
                        
            for p in content_box.find_all('p'):
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
                    
                for span in p.find_all('span'):
                    if 'style' not in span.attrs:
                        span['style'] = 'font-size: 14px; font-family: 宋体, SimSun;'
                    
        except Exception as e:
            self.logger.error(f"清理文章内容失败: {e}")
            
        return content_div

    def save_article_html(self, article_id: str, content: str) -> None:
        """保存文章HTML内容"""
        try:
            os.makedirs('可可英语', exist_ok=True)
            
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
            
            file_path = f'可可英语/{article_id}.html'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_template)
            self.logger.info(f"HTML内容已保存到: {os.path.abspath(file_path)}")
            
        except Exception as e:
            self.logger.error(f"保存HTML内容失败: {e}")

    def _upload_to_server(self, local_path: str, remote_filename: str) -> bool:
        """上传文件到服务器"""
        try:
            transport = paramiko.Transport((SERVER_CONFIG['hostname'], 22))
            transport.connect(
                username=SERVER_CONFIG['username'],
                password=SERVER_CONFIG['password']
            )
            
            sftp = paramiko.SFTPClient.from_transport(transport)
            remote_path = f"{SERVER_CONFIG['remote_path']}/{remote_filename}"
            
            # 确保远程目录存在
            remote_dir = os.path.dirname(remote_path)
            try:
                sftp.stat(remote_dir)
            except FileNotFoundError:
                sftp.mkdir(remote_dir)
            
            sftp.put(local_path, remote_path)
            sftp.close()
            transport.close()
            return True
            
        except Exception as e:
            self.logger.error(f"上传文件失败: {e}")
            return False

    def change_permissions(self) -> None:
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
                self.logger.error(f"修改权限失败: {error}")
            else:
                self.logger.info("文件权限修改成功")
            
            ssh.close()
            
        except Exception as e:
            self.logger.error(f"修改文件权限失败: {e}")

    def save_to_database(self, article_data: Dict) -> bool:
        """保存文章到数据库"""
        try:
            with pymysql.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    check_sql = "SELECT id FROM voa_cj WHERE id = %s"
                    cursor.execute(check_sql, (article_data['id'],))
                    exists = cursor.fetchone()
                    
                    if exists:
                        self.logger.info(f"文章 {article_data['id']} 已存在")
                        return False
                        
                    views = random.randint(5000, 10000)
                    
                    sql = """
                    INSERT INTO voa_cj (
                        id, title, url, date, audio, image, category, 
                        update_time, views, vocabulary_count, voa_type
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    """
                    cursor.execute(sql, (
                        article_data['id'],
                        article_data['title'],
                        article_data['url'],
                        TOMORROW_DATE,
                        article_data['audio'],
                        article_data['image'],
                        '',
                        TOMORROW_DATE,
                        views,
                        0,
                        'voa_mansu'
                    ))
                    
                conn.commit()
                self.logger.info(f"文章 {article_data['id']} 已保存到数据库")
                return True
                
        except Exception as e:
            self.logger.error(f"保存到数据库失败: {e}")
            return False

    def extract_article_info(self, html_content: str) -> Tuple[Optional[Dict], Optional[str]]:
        """提取文章信息"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            title = ''
            title_div = soup.find('div', class_='player-title')
            if title_div:
                title = title_div.text.strip()
            self.logger.info(f"提取到标题: {title}")
            
            english_title = self.translate_text(title)
            if english_title:
                self.logger.info(f"翻译后的标题: {english_title}")
                full_title = f"{title} = {english_title}"
            else:
                full_title = title
                
            article_id = url.split('/')[-1]
            
            audio_element = soup.find('audio', id='xplayer_audio')
            audio_url = audio_element['src'] if audio_element else ''
            
            content_div = soup.find('div', class_='caption-box')
            image_url = self.search_pixabay_image(title, article_id)
            
            article_data = {
                'id': article_id,
                'title': full_title,
                'url': f'http://readingstuday.top/voa/kk/{article_id}.html',
                'date': TOMORROW_DATE,
                'audio': audio_url,
                'image': image_url,
                'category': '',
                'vocabulary_count': 0,
                'voa_type': 'voa_mansu'
            }
            
            self.logger.info("文章数据:")
            self.logger.info(json.dumps(article_data, ensure_ascii=False, indent=4))
            
            return article_data, str(content_div) if content_
            return article_data, str(content_div) if content_div else ''
            
        except Exception as e:
            self.logger.error(f"提取文章信息失败: {e}")
            return None, None

    def process_article(self, url: str) -> Optional[Dict]:
        """处理文章的主流程"""
        try:
            self.logger.info(f"开始处理文章: {url}")
            
            html_content = self.get_web_content(url)
            if not html_content:
                self.logger.error("获取网页内容失败")
                return None
                
            article_data, cleaned_html = self.extract_article_info(html_content)
            if article_data and cleaned_html:
                self.logger.info("文章信息提取完成")
                
                self.save_article_html(article_data['id'], cleaned_html)
                
                # 上传文件
                file_path = f"可可英语/{article_data['id']}.html"
                if os.path.exists(file_path):
                    if self._upload_to_server(file_path, f"{article_data['id']}.html"):
                        self.logger.info("文件上传成功")
                        self.change_permissions()
                        
                        # 保存到数据库
                        if self.save_to_database(article_data):
                            self.logger.info("文章处理完成!")
                            return article_data
                        else:
                            self.logger.error("保存到数据库失败")
                    else:
                        self.logger.error("上传文件失败")
                else:
                    self.logger.error(f"文件不存在: {file_path}")
                    
            return None
            
        except Exception as e:
            self.logger.error(f"处理文章时出错: {e}")
            traceback.print_exc()
            return None

def main():
    """主函数"""
    print("=" * 50)
    print("VOA文章处理程序")
    print("=" * 50)
    
    # 这里填入文章URL
    article_url = "https://kekenet.com/lesson/96-700156"
    
    processor = ArticleProcessor()
    article_data = processor.process_article(article_url)
    
    if article_data:
        print("\n处理结果:")
        print("=" * 50)
        print("文章数据:")
        print(json.dumps(article_data, ensure_ascii=False, indent=4))
    else:
        print("\n处理失败!")

if __name__ == "__main__":
    main()