import os
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime, timedelta
import json
import traceback
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote
import time
import random

@dataclass
class Article:
    title: str
    index: int
    url: str = ""
    mp3_url: str = ""

class KekenetScraper:
    def __init__(self, headless: bool = True, retry_count: int = 3):
        self.setup_logging()
        self.base_url = "https://www.kekenet.com"
        self.headless = headless
        self.retry_count = retry_count
        self.session_start_time = datetime.now()
        self.base_dir = '可可英语/英语入门/千万别学英语'
        self.mp3_dir = os.path.join(self.base_dir, 'mp3')
        self.html_dir = os.path.join(self.base_dir, 'html')
        self.category = 'qianwanbiexueyingyu'
        self.serverUrl = 'http://readingstuday.top/yyrm/' + self.category + '/'
        self.mp3ServerUrl='https://774663576.github.io/br_media/tingli/'+ self.category + '/'

    def setup_logging(self):
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f"scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_driver(self) -> webdriver.Chrome:
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        return driver

    def download_mp3(self, mp3_url: str, article_id: str) -> bool:
        try:
            if not mp3_url:
                self.logger.warning(f"文章 {article_id} 没有MP3链接")
                return False
            
            mp3_dir = Path(self.mp3_dir)
            mp3_dir.mkdir(parents=True, exist_ok=True)
            file_path = mp3_dir / f"{article_id}.mp3"
            
            response = requests.get(mp3_url, stream=True)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            self.logger.info(f"MP3文件已保存到: {file_path.absolute()}")
            return True
        
        except Exception as e:
            self.logger.error(f"下载MP3文件失败 ({article_id}): {e}")
            traceback.print_exc()
            return False

    def clean_article_content(self, content_div: BeautifulSoup) -> BeautifulSoup:
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
            
            for p in content_box.find_all('p'):
                style = 'text-indent: 2em; line-height: 1.75em; margin-bottom: 15px; margin-top: 15px;'
                p['style'] = style
                
                for span in p.find_all('span'):
                    span['style'] = 'font-size: 14px; font-family: 宋体, SimSun;'
                    
        except Exception as e:
            self.logger.error(f"清理文章内容时出错: {e}")
            traceback.print_exc()
            
        return content_div

    def save_article_html(self, article_id: str, content: str):
        try:
            html_dir = Path(self.html_dir)
            html_dir.mkdir(parents=True, exist_ok=True)
            
            html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Article {article_id}</title>
        <link rel="stylesheet" href="./style.css">
    </head>
    <body>
        <div class="article-content">
            {content}
        </div>
        <script src="./script.js"></script>
    </body>
</html>'''
            
            file_path = html_dir / f'{article_id}.html'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_template)
            self.logger.info(f"HTML内容已保存到: {file_path.absolute()}")
            
        except Exception as e:
            self.logger.error(f"保存HTML内容失败: {e}")
            traceback.print_exc()

    def extract_article_detail(self, url: str) -> Optional[Dict]:
        self.logger.info(f"开始提取文章详细信息: {url}")
        driver = None
        
        try:
            driver = self.get_driver()
            driver.get(url)
            time.sleep(2)
            
            full_content = driver.page_source
            soup = BeautifulSoup(full_content, 'html.parser')
            
            article_id = url.split('/')[-1]
            
            audio_element = soup.find('audio', id='xplayer_audio')
            original_audio_url = audio_element['src'] if audio_element else ''
            
            if not original_audio_url:
                self.logger.error(f"未找到音频链接: {url}")
                return None
                
            if not self.download_mp3(original_audio_url, article_id):
                return None
            
            local_audio_url = f"{self.mp3ServerUrl}mp3/{article_id}.mp3"
            content_div = soup.find('div', class_='caption-box')
            
            if not content_div:
                self.logger.error(f"未找到文章内容: {url}")
                return None
                
            cleaned_content = self.clean_article_content(content_div)
            self.save_article_html(article_id, str(cleaned_content))
            
            return {
                'mp3_url': local_audio_url,
                'url':self.serverUrl+article_id+'.html',
                # 'url': f"{self.serverUrl}html/{article_id}.html",
            }
            
        except Exception as e:
            self.logger.error(f"提取文章详细信息失败: {e}")
            traceback.print_exc()
            return None
            
        finally:
            if driver:
                driver.quit()

    def extract_article_list(self, driver: webdriver.Chrome) -> List[Article]:
        all_articles = []
        page = 1
        valid_articles = []
        
        while True:
            self.logger.info(f"正在处理第 {page} 页")
            
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "news-list-item"))
                )
                
                items = driver.find_elements(By.CLASS_NAME, "news-list-item")
                
                for idx, item in enumerate(items, 1):
                    try:
                        title = item.find_element(By.CLASS_NAME, "news-item-title").text
                        pattern = r"Lesson\d+"
                        match = re.search(pattern, title)
                        if match:
                            title = match.group()
                            
                        current_window = driver.current_window_handle
                        driver.execute_script("arguments[0].click();", item)
                        time.sleep(1)
                        
                        article_details = None
                        if len(driver.window_handles) > 1:
                            for handle in driver.window_handles:
                                if handle != current_window:
                                    driver.switch_to.window(handle)
                                    article_url = driver.current_url
                                    article_details = self.extract_article_detail(article_url)
                                    driver.close()
                                    break
                            driver.switch_to.window(current_window)
                        
                        if article_details:
                            article = Article(
                                title=title,
                                index=len(valid_articles) + 1,
                                mp3_url=article_details['mp3_url'],
                                url=article_details['url']
                            )
                            valid_articles.append(article)
                            
                        self.logger.info(f"第 {page} 页: 已处理 {idx}/{len(items)} 篇文章")
                        
                    except Exception as e:
                        self.logger.error(f"处理文章时出错 (页码: {page}, 索引: {idx}): {str(e)}")
                        continue

                # if page == 1:
                #     break

                try:
                    next_button = driver.find_element(By.CLASS_NAME, "btn-next")
                    if next_button.get_attribute("disabled") == "true":
                        self.logger.info("已到达最后一页")
                        break
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(2)
                    page += 1
                    
                except Exception as e:
                    self.logger.error(f"处理分页时出错: {str(e)}")
                    break
                    
            except Exception as e:
                self.logger.error(f"处理页面 {page} 时出错: {str(e)}")
                break
        
        return valid_articles

    def save_articles(self, articles: List[Article]):
        try:
            base_dir = Path(self.base_dir)
            base_dir.mkdir(parents=True, exist_ok=True)
            
            filename = base_dir / f"{self.category}.json"
            
            valid_articles = [
                {
                    "title": article.title,
                    "url": article.url,
                    "index": len(articles) - idx,
                    "mp3_url": article.mp3_url,
                    "category": self.category,
                    "view_count": random.randint(1000, 10000)
                }
                for idx, article in enumerate(articles)
                if article.url and article.mp3_url
            ]
            
            if not valid_articles:
                self.logger.warning("没有找到完整的文章记录")
                return
                
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(valid_articles, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f"文章信息已保存到: {filename}")
            self.logger.info(f"共保存 {len(valid_articles)} 篇完整文章")
            
        except Exception as e:
            self.logger.error(f"保存文章信息时出错: {str(e)}")
            traceback.print_exc()

    def scrape(self, url: str) -> List[Article]:
        self.logger.info(f"开始抓取: {url}")
        driver = None
        
        try:
            driver = self.get_driver()
            driver.get(url)
            
            for attempt in range(self.retry_count):
                try:
                    articles = self.extract_article_list(driver)
                    if articles:
                        self.save_articles(articles)
                        self.logger.info(f"成功提取所有文章信息，共 {len(articles)} 篇")
                        return articles
                    break
                except Exception as e:
                    self.logger.error(f"第 {attempt + 1} 次尝试失败: {str(e)}")
                    if attempt < self.retry_count - 1:
                        time.sleep(5)
                        continue
                    raise
            
            self.logger.warning("未找到文章信息")
            return []
            
        except Exception as e:
            self.logger.error(f"抓取过程出错: {str(e)}")
            return []
            
        finally:
            if driver:
                driver.quit()

def main():
    course_url = "https://kekenet.com/course/118"
    
    print("=" * 50)
    print("可可英语文章爬虫")
    print("=" * 50)
    
    scraper = KekenetScraper(headless=True, retry_count=3)
    articles = scraper.scrape(course_url)
    
    if articles:
        print("\n爬取完成!")
        print(f"共获取 {len(articles)} 篇文章")
    else:
        print("\n爬取失败!")

if __name__ == "__main__":
    main()