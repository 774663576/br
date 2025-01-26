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
    """获取网页内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"正在获取页面内容: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        print("页面内容获取成功")
        return response.text
    except Exception as e:
        print(f"获取页面失败: {e}")
        traceback.print_exc()
        return None

def clean_article_content(content_div):
    """清理文章内容，去掉不需要的部分"""
    if not content_div:
        return content_div
        
    try:
        # 找到 Contentbox2 div
        content_box = content_div.find('div', class_='Contentbox2')
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
        if not os.path.exists('voa'):
            os.makedirs('voa')
            print("创建voa目录成功")
            
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
        file_path = f'voa/{article_id}.html'
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

def save_to_database(article_data):
    """保存文章到数据库"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            # 检查文章是否已存在
            check_sql = "SELECT id FROM voa_cj WHERE id = %s"
            cursor.execute(check_sql, (article_data['id'],))
            exists = cursor.fetchone()
            
            if exists:
                print(f"文章 {article_data['id']} 已存在，跳过保存")
                return False
                
            # 生成随机views数值
            views = random.randint(5000, 10000)
            
            # 插入新文章
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
                article_data['date'],
                article_data['audio'],
                article_data['image'],
                '',
                datetime.now().strftime('%Y-%m-%d'),
                views,
                0,
                'voa_changsu'
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
        if os.path.exists(f"voa/{filename}"):
            if upload_to_server('voa', filename):
                print(f"成功上传: {filename}")
                # 修改文件权限
                change_permissions()
                return True
            else:
                print(f"上传失败: {filename}")
                return False
        else:
            print(f"文件不存在: voa/{filename}")
            return False
            
    except Exception as e:
        print(f"上传过程出错: {e}")
        traceback.print_exc()
        return False

def extract_article_info(html_content):
    """从HTML中提取文章信息"""
    try:
        print("\n开始解析文章内容...")
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 提取标题并打印每一步
        title = ''
        title_div = soup.find('div', class_='titl')
        if title_div:
            print(f"原始标题文本: {title_div.text}")  # 打印原始文本
            title = title_div.text.strip()
            print(f"去除空格后: {title}")  # 打印去除空格后的文本
            title = title.split('：')[-1]
            print(f"分割后的标题: {title}")  # 打印最终标题
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
        article_id = ''
        canonical_link = soup.find('link', rel='canonical')
        if canonical_link:
            url_match = re.search(r'show-\d+-(\d+)-1\.html', canonical_link['href'])
            if url_match:
                article_id = url_match.group(1)
        if not article_id:  # 如果link标签中没有找到，尝试从span中获取
            useid_span = soup.find('span', id='useid')
            if useid_span:
                article_id = useid_span.text.strip()
        print(f"提取到文章ID: {article_id}")
        
        # 提取音频URL
        audio_element = soup.find('audio', id='mediaPlayId')
        audio_url = audio_element.get('m-src', '') if audio_element else ''
        print(f"提取到音频URL: {audio_url}")
        
        # 提取文章内容和图片
        content_div = soup.find('div', class_='tabbody')
        image_url = ''
        if content_div:
            # 直接使用原始内容，只清理不需要的部分
            cleaned_content = clean_article_content(content_div)
            if cleaned_content:
                # 提取图片URL
                img = cleaned_content.find('img')
                if img and img.get('src'):
                    image_url = img['src']
                
                # 直接使用清理后的内容
                content_div = cleaned_content
                
        print(f"提取到图片URL: {image_url}")
        
        # 构建文章数据
        article_data = {
            'id': article_id,
            'title': full_title,  # 使用组合后的标题
            'url': f'http://readingstuday.top/voa/{article_id}.html',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'audio': audio_url,
            'image': image_url,
            'category': '',
            'vocabulary_count': 0,
            'voa_type': 'voa_changsu'
        }
        
        return article_data, str(content_div) if content_div else ''
        
    except Exception as e:
        print(f"提取文章信息时出错: {e}")
        traceback.print_exc()
        return None, None

def main(url):
    """主函数"""
    try:
        print(f"\n开始处理文章...")
        print(f"URL: {url}")
        
        # 获取网页内容
        html_content = get_web_content(url)
        if not html_content:
            print("获取网页内容失败")
            return None
            
        # 提取文章信息
        article_data, cleaned_html = extract_article_info(html_content)
        if article_data and cleaned_html:
            print("\n文章信息提取完成!")
            
            # 保存HTML内容
            save_article_html(article_data['id'], cleaned_html)
            
            # 上传文件到服务器
            if upload_files(article_data):
                # 保存到数据库
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
    # 这里填入文章URL
    article_url = "https://m.tingclass.net/show-10616-592695-1.html"
    
    print("=" * 50)
    print("VOA文章处理程序")
    print("=" * 50)
    
    article_data = main(article_url)
    
    if article_data:
        print("\n处理结果:")
        print("=" * 50)
        print("文章数据:")
        print(json.dumps(article_data, ensure_ascii=False, indent=4))
    else:
        print("\n处理失败!")