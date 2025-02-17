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
    # url: str
    index: int
    # category:str
    mp3_url: str = ""


class KekenetScraper:
    def __init__(self, headless: bool = True, retry_count: int = 3):
        self.setup_logging()
        self.base_url = "https://www.kekenet.com"
        self.headless = headless
        self.retry_count = retry_count
        self.session_start_time = datetime.now()
        self.outputDir='可可英语/李阳疯狂英语365句'
        self.category='liyang_fengkuangyingyu365'
        self.serverUrl='http://readingstuday.top/kouyu/'+self.category+'/'

        
    def setup_logging(self):
        """配置日志系统"""
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
        """获取配置好的Chrome WebDriver实例"""
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

   

    

    def clean_article_content(self, content_div: BeautifulSoup) -> BeautifulSoup:
        """清理文章内容"""
        if not content_div:
            return content_div
            
        try:
            content_box = content_div.find('div', class_='caption-box')
            if not content_box:
                return content_div
                
            # 删除最后一段
            paragraphs = content_box.find_all('p')
            if paragraphs:
                last_p = paragraphs[-1]
                if last_p and '以上便是' in last_p.text:
                    last_p.decompose()
            
            # 删除图片上面的内容
            first_img = content_box.find('img')
            if first_img:
                img_p = first_img.find_parent('p')
                if img_p:
                    for p in img_p.find_previous_siblings('p'):
                        p.decompose()
                        
            # 设置段落样式
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
                    
                # 设置span样式
                for span in p.find_all('span'):
                    if 'style' not in span.attrs:
                        span['style'] = 'font-size: 14px; font-family: 宋体, SimSun;'
                        
        except Exception as e:
            self.logger.error(f"清理文章内容时出错: {e}")
            traceback.print_exc()
            
        return content_div

    def save_article_html(self, article_id: str, content: str):
        """保存文章HTML内容"""
        try:
            output_dir = Path(self.outputDir)
            output_dir.mkdir(exist_ok=True)
            
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
            
            file_path = output_dir / f'{article_id}.html'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_template)
            self.logger.info(f"HTML内容已保存到: {file_path.absolute()}")
            
        except Exception as e:
            self.logger.error(f"保存HTML内容失败: {e}")
            traceback.print_exc()

    def extract_article_detail(self, url: str) -> Optional[Dict]:
        """提取文章详细信息"""
        self.logger.info(f"开始提取文章详细信息: {url}")
        driver = None
        
        try:
            driver = self.get_driver()
            driver.get(url)
            driver.implicitly_wait(10)
            total_height = driver.execute_script("return document.body.scrollHeight")
            for i in range(0, total_height, 500):
                driver.execute_script(f"window.scrollTo(0, {i});")
                time.sleep(0.5)  # 短暂停顿，让内容加载
            full_content = driver.page_source
            # self.logger.info(f"full_content: {full_content}")

            # # 等待页面加载
            # WebDriverWait(driver, 20).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, "player-title"))
            # )
            
            soup = BeautifulSoup(full_content, 'html.parser')
            
            # # 提取标题
            # title = ''
            # title_div = soup.find('div', class_='player-title')
            # if title_div:
            #     title = title_div.text.strip()
            
            
            
            # 提取ID
            article_id = url.split('/')[-1]
            self.logger.error(f"article_id------: {article_id}")

            
            # 提取音频URL
            audio_element = soup.find('audio', id='xplayer_audio')
            audio_url = audio_element['src'] if audio_element else ''
            self.logger.error(f"audio_url------: {audio_url}")
            
            # 提取文章内容和获取图片
            content_div = soup.find('div', class_='caption-box')
 
             
            # 清理内容
            cleaned_content = content_div

 
            
            # 保存HTML
            if cleaned_content:
                self.save_article_html(article_id, str(cleaned_content))
            
            return {
                 'mp3_url': audio_url,
                 'url':self.serverUrl+article_id+'.html',

             }
            
        except Exception as e:
            self.logger.error(f"提取文章详细信息失败: {e}")
            traceback.print_exc()
            return None
            
        finally:
            if driver:
                driver.quit()

    def extract_article_list(self, driver: webdriver.Chrome) -> List[Article]:
        """提取文章列表信息"""
        all_articles = []
        page = 1
        
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
                            title=match.group()
                        self.logger.info(f"title----{title}")

 
                        sub_elements = item.find_elements(By.CLASS_NAME, "news-item-sub")
                        difficulty, duration, date = "", "", ""
                        
                        if sub_elements:
                            sub_divs = sub_elements[0].find_elements(By.TAG_NAME, "div")
                            if len(sub_divs) >= 3:
                                difficulty = sub_divs[0].text.strip()
                                duration = sub_divs[1].text.strip()
                                date = sub_divs[2].text.strip()
                        
                        # 获取文章URL
                        current_window = driver.current_window_handle
                        driver.execute_script("arguments[0].click();", item)
                        time.sleep(0.5)
                        
                        article_url = None
                        if len(driver.window_handles) > 1:
                            for handle in driver.window_handles:
                                if handle != current_window:
                                    driver.switch_to.window(handle)
                                    article_url = driver.current_url
                                    # 提取文章详细信息
                                    article_details = self.extract_article_detail(article_url)
                                    driver.close()
                                    break
                            driver.switch_to.window(current_window)
                        
                        article = Article(
                            title=title,
                            index=len(all_articles) + 1
                        )
                        
                        # 添加详细信息
                        if article_details:
                             article.mp3_url = article_details['mp3_url']
                             article.url=article_details['url']
                          
                        all_articles.append(article)
                        self.logger.info(f"第 {page} 页: 已处理 {idx}/{len(items)} 篇文章")
                        
                    except Exception as e:
                        self.logger.error(f"处理文章时出错 (页码: {page}, 索引: {idx}): {str(e)}")
                        continue
                
                # 检查是否有下一页
                try:
                    next_button = driver.find_element(By.CLASS_NAME, "btn-next")
                    if next_button.get_attribute("disabled") == "true" or next_button.get_attribute("aria-disabled") == "true":
                        self.logger.info("已到达最后一页")
                        break
                    # if page==1:
                    #     break;
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(1)  # 等待新页面加载
                    page += 1
                    
                except Exception as e:
                    self.logger.error(f"处理分页时出错: {str(e)}")
                    break
                    
            except Exception as e:
                self.logger.error(f"处理页面 {page} 时出错: {str(e)}")
                break
        
        return all_articles

    def save_articles(self, articles: List[Article]):
        """保存文章信息到JSON文件"""
        try:
            output_dir = Path(self.outputDir)
            output_dir.mkdir(exist_ok=True)
            
            timestamp = self.session_start_time.strftime('%Y%m%d_%H%M%S')
            filename = output_dir / f"{self.category}.json"
            
            articles_data = [
                {
                    "title": article.title,
                    "url": getattr(article, 'url', ""),
                    "index": len(articles) - idx,
                    "mp3_url": article.mp3_url,
                    "category":self.category,
                    "views":random.randint(1000, 10000)
                  }
                for idx,article in enumerate(articles)
            ]
            
           

        



            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(articles_data, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f"文章信息已保存到: {filename}")
            
        except Exception as e:
            self.logger.error(f"保存文章信息时出错: {str(e)}")
            traceback.print_exc()

    def scrape(self, url: str) -> List[Article]:
        """执行爬取操作"""
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
    """主函数"""
    # 课程列表URL
    course_url = "https://kekenet.com/course/1327"
    
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