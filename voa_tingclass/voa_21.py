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
    'remote_path': '/home/book/voa_21'
}

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

def get_translation(text):
    """获取文本的中文翻译"""
    global translation_available
    
    # 如果翻译服务已标记为不可用，直接返回空字符串
    if not translation_available:
        return ''
        
    try:
        url = f'https://api.mymemory.translated.net/get?q={text}&langpair=en|zh'
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # 获取翻译结果
        translated_text = data.get('responseData', {}).get('translatedText', '')
        
        # 检查是否包含错误信息关键词
        error_keywords = ['MYMEMORY WARNING', 'YOU USED ALL', 'AVAILABLE FREE TRANSLATIONS']
        if any(keyword in translated_text.upper() for keyword in error_keywords):
            print("翻译服务配额已用尽，停止后续翻译")
            translation_available = False  # 标记翻译服务不可用
            return ''
            
        # 只有在没有警告信息的情况下才返回翻译结果
        if data.get('responseStatus') == 200 and translated_text:
            return translated_text
        else:
            translation_available = False  # 标记翻译服务不可用
            return ''
            
    except Exception as e:
        print(f"获取翻译失败: {e}")
        return ''

def split_and_translate(text):
    """将长文本分段翻译"""
    global translation_available
    if not translation_available:
        return ''
        
    try:
        if len(text) <= 450:
            return get_translation(text)
            
        sentences = re.split('([.!?]+)', text)
        sentences = [''.join(i) for i in zip(sentences[::2], sentences[1::2] + [''])]
        
        current_chunk = ''
        translated_chunks = []
        
        for sentence in sentences:
            if len(current_chunk + sentence) <= 450:
                current_chunk += sentence
            else:
                if current_chunk:
                    trans = get_translation(current_chunk.strip())
                    if trans:
                        translated_chunks.append(trans)
                current_chunk = sentence
        
        if current_chunk:
            trans = get_translation(current_chunk.strip())
            if trans:
                translated_chunks.append(trans)
        
        return ' '.join(translated_chunks)
        
    except Exception as e:
        print(f"分段翻译出错: {e}")
        return ''
def count_vocabulary_words(content_div):
    """统计 Words in This Story 中的单词数量"""
    try:
        words_section = None
        for h2 in content_div.find_all('h2'):
            if 'Words in This Story' in h2.text:
                words_section = h2.find_next_siblings()
                break
        
        if words_section:
            word_count = sum(1 for p in words_section if p.find('strong'))
            return word_count
    except Exception as e:
        print(f"统计单词数量时出错: {e}")
    return 0

def clean_article_content(content_div, soup):
    """清理文章内容，移动图片到开头，添加翻译"""
    global translation_available
    if not content_div:
        return content_div
    
    try:
        # 删除byline和datetime
        for tag in content_div.find_all(['span']):
            if 'byline' in tag.get('class', []) or 'datetime' in tag.get('class', []):
                tag.decompose()
        
        # 处理图片
        img_div = content_div.find('div', class_='contentImage')
        if img_div:
            img_content = str(img_div)
            img_div.decompose()
            content_div.insert(0, BeautifulSoup(img_content, 'html.parser'))
        
        # 找到 Words in This Story 部分
        words_section_start = None
        for h2 in content_div.find_all('h2'):
            if 'Words in This Story' in h2.text:
                words_section_start = h2
                break
        
        # 处理段落
        for p in content_div.find_all('p'):
            if not translation_available:
                break
                
            if p.find('em') or (words_section_start and p.sourceline > words_section_start.sourceline):
                continue
                
            for a in p.find_all('a'):
                a.unwrap()
            
            p['class'] = 'english-content'
            
            text = p.get_text().strip()
            if text and not text.startswith('___') and len(text) > 10:
                translation = split_and_translate(text)
                if translation:
                    trans_p = soup.new_tag('p')
                    trans_p.string = translation
                    trans_p['class'] = 'chinese-translation'
                    p.insert_after(trans_p)
                
    except Exception as e:
        print(f"清理文章内容时出错: {e}")
        
    return content_div
def save_to_database(articles):
    """保存文章到数据库"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            current_time = datetime.now().strftime('%Y-%m-%d')
            
            for article in articles:
                views = random.randint(5000, 10000)

                check_sql = "SELECT id FROM articles WHERE id = %s"
                cursor.execute(check_sql, (article['id'],))
                exists = cursor.fetchone()
                
                if exists:
                    continue
                else:
                    title = article['title'][:255]
                    
                    sql = """
                    INSERT INTO articles (id, title, url, date, audio, image, category, update_time, views, vocabulary_count, voa_type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        article['id'],
                        title,
                        f'http://readingstuday.top/voa_21/{article["id"]}.html',
                        article['date'],
                        article['audio'],
                        article['image'],
                        article['category'],
                        current_time,
                        views,
                        article['vocabulary_count'],
                        'voa_21_mansu'
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
        
        try:
            sftp.stat(SERVER_CONFIG['remote_path'])
        except FileNotFoundError:
            print(f"创建远程目录: {SERVER_CONFIG['remote_path']}")
            sftp.mkdir(SERVER_CONFIG['remote_path'])
        
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
        ssh.connect(**{k: v for k, v in SERVER_CONFIG.items() if k != 'remote_path'})
        
        command = f"chmod -R 755 {SERVER_CONFIG['remote_path']}"
        stdin, stdout, stderr = ssh.exec_command(command)
        
        error = stderr.read().decode()
        if error:
            print(f"修改权限时出错: {error}")
        else:
            print("文件权限修改成功")
        
        ssh.close()
        
    except Exception as e:
        print(f"修改文件权限失败: {e}")

def upload_files(latest_articles):
    """上传最新文章到服务器"""
    try:
        print("\n开始上传最新文章到服务器...")

        # 检查并执行remove_br.py
        remove_br_path = os.path.join('21_voa_mansu', 'remove_br.py')
        if os.path.exists(remove_br_path):
            try:
                print("执行remove_br.py脚本...")
                # 获取脚本的绝对路径
                abs_script_path = os.path.abspath(remove_br_path)
                print(f"脚本路径: {abs_script_path}")  # 调试输出
                
                import subprocess
                result = subprocess.run(['python', abs_script_path], 
                                     capture_output=True, 
                                     text=True)
                if result.returncode == 0:
                    print("成功执行remove_br.py")
                else:
                    print(f"执行remove_br.py失败: {result.stderr}")
            except Exception as e:
                print(f"执行remove_br.py时出错: {e}")
        else:
            print(f"remove_br.py文件不存在，跳过执行 (检查路径: {remove_br_path})")

        success_count = 0
        fail_count = 0
        
        for article in latest_articles:
            filename = f"{article['id']}.html"
            if os.path.exists(f"21_voa_mansu/{filename}"):
                if upload_to_server('21_voa_mansu', filename):
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
    <script src="script.js"></script>
</body>
</html>'''
    
    try:
        if not os.path.exists('21_voa_mansu'):
            os.makedirs('21_voa_mansu')
            
        with open(f'21_voa_mansu/{article_id}.html', 'w', encoding='utf-8') as f:
            f.write(html_template)
    except Exception as e:
        print(f"保存文章 {article_id} HTML内容失败: {e}")

def parse_article_content(article_url, article_id):
    """解析文章详情页，获取音频和HTML内容"""
    try:
        html_content = get_web_content(article_url)
        if not html_content:
            return None, 0
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        audio_url = None
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'mp3:' in script.string:
                match = re.search(r'mp3:"(.*?)"', script.string)
                if match:
                    audio_url = match.group(1)
                    break
        
        content_div = soup.find('div', id='ShowEN')
        word_count = 0
        if content_div:
            word_count = count_vocabulary_words(content_div)
            content_div = clean_article_content(content_div, soup)
            if content_div:
                save_article_html(article_id, str(content_div))
            
        return audio_url, word_count
            
    except Exception as e:
        print(f"解析文章详情页出错: {e}")
        return None, 0

def parse_voa_list(url):
    """解析VOA文章列表"""
    start_time = time.time()
    
    if not os.path.exists('21_voa_mansu'):
        os.makedirs('21_voa_mansu')
    
    html_content = get_web_content(url)
    if not html_content:
        print("获取文章列表失败")
        return []
    
    all_articles = []
    new_articles = []  # 用于记录新文章
    
    try:
        # 先检查数据库中已存在的文章
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            articles_on_page = 0
            for li in soup.select('div.article-feed li'):
                if not li.find('div', class_='rt-box'):
                    continue
                    
                title_link = li.find('h3').find('a')
                if not title_link:
                    continue
                
                article_id = title_link.get('href').split('-')[-1].replace('.html', '')
                
                # 检查文章是否已存在
                sql = "SELECT id FROM articles WHERE id = %s"
                cursor.execute(sql, (article_id,))
                exists = cursor.fetchone()
                
                if exists:
                    print(f"文章ID {article_id} 已存在，跳过")
                    continue
                
                # 处理新文章
                article_url = 'http://m.21voa.com' + title_link.get('href', '')
                title = title_link.text.strip()
                
                title_zh = get_translation(title)
                full_title = f"{title} = {title_zh}" if title_zh else title
                
                category = ''
                category_link = li.select_one('div.vice span a')
                if category_link:
                    category = category_link.text.strip()
                
                date_span = li.select_one('div.vice span')
                date = date_span.text.strip() if date_span else ''
                
                img = li.find('img')
                image = img.get('src') if img else ''
                
                print(f"正在获取文章 {article_id} - {title} 的内容...")
                audio_url, word_count = parse_article_content(article_url, article_id)
                
                article_data = {
                    'id': article_id,
                    'title': full_title,
                    'date': date,
                    'audio': audio_url,
                    'image': image,
                    'category': category,
                    'vocabulary_count': word_count
                }
                
                all_articles.append(article_data)
                new_articles.append(article_data)  # 记录新文章
                articles_on_page += 1
                
                print(f"完成文章: {full_title}")
                time.sleep(random.uniform(1, 3))
        
        conn.close()
        print(f"完成，获取到 {articles_on_page} 篇新文章")
        
    except Exception as e:
        print(f"处理文章列表时出错: {e}")
        if 'conn' in locals():
            conn.close()
    
    total_time = time.time() - start_time
    print(f"\n抓取完成！")
    print(f"总用时: {total_time:.2f} 秒")
    print(f"总文章数: {len(all_articles)} 篇")
    
    return all_articles, new_articles  # 返回所有文章和新文章

def main():
    """主函数"""
    try:
        global translation_available
        translation_available = True
        
        if not os.path.exists('21_voa_mansu'):
            os.makedirs('21_voa_mansu')
            
        url = "http://m.21voa.com/voa_special_english"
        all_articles, new_articles = parse_voa_list(url)
        
        if new_articles:  # 如果有新文章
            # 保存到数据库
            save_to_database(new_articles)
            
            # 上传新文章
            print(f"\n发现 {len(new_articles)} 篇新文章，开始上传...")
            upload_files(new_articles)
        else:
            print("\n没有发现新文章，无需上传")
            
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序执行出错: {e}")

if __name__ == "__main__":
    main()