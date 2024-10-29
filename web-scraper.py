import requests
import os
from time import sleep
import logging
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import concurrent.futures
import re
import sys
from datetime import datetime

class BookScraper:
    def __init__(self, base_url="/book/", output_dir="downloaded_pages"):
        """
        初始化爬虫
        :param base_url: 基础URL路径
        :param output_dir: 下载文件保存目录
        """
        self.base_url = "https://www.shubang.net" + base_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 创建日志目录
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # 设置日志文件名（包含时间戳）
        log_filename = f"logs/scraping_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        # 初始化计数器
        self.downloaded_pages = 0
        self.failed_pages = 0
        
        # 设置请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Referer': 'https://www.shubang.net/'
        }
        
        # 创建session以复用连接
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def fetch_page(self, url, retries=3, delay=1):
        """
        获取页面内容，带重试机制
        """
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                if delay:
                    sleep(delay)
                return response.text
            except requests.RequestException as e:
                if attempt == retries - 1:  # 最后一次重试
                    logging.error(f'获取 {url} 失败 (尝试 {attempt + 1}/{retries}): {e}')
                    self.failed_pages += 1
                    return None
                logging.warning(f'获取 {url} 失败 (尝试 {attempt + 1}/{retries}): {e}，准备重试...')
                sleep(delay * (attempt + 1))  # 指数退避
        return None

    def save_html(self, content, filename):
        """
        保存HTML内容到文件
        """
        try:
            filepath = self.output_dir / "book" / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)

            # 修改HTML内容
            modified_content = self.modify_html_links(content)

            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(modified_content)
            
            self.downloaded_pages += 1
            logging.info(f'已保存HTML到 {filepath}')
            
        except Exception as e:
            self.failed_pages += 1
            logging.error(f'保存HTML文件 {filename} 时出错: {e}')

    def modify_html_links(self, html_content):
        """
        修改HTML内容中的链接和移除不需要的元素
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

           

            # 删除不需要的元素
            elements_to_remove = {
                'nav': {'class_': 'navbar'},
                'footer': {'class_': 'footer'},
                'div': {'class_': 'c-bottom'},
                'div': {'class_': 'cha'}
            }

            for tag, attrs in elements_to_remove.items():
                element = soup.find(tag, **attrs)
                if element:
                    element.decompose()

            # 删除特定的h3和ul
            for elem in soup.find_all(['h3', 'ul']):
                if elem.get('class') in [['zbt'], ['lst6']]:
                    elem.decompose()

            # 修改分页链接
            pagelink_div = soup.find('div', class_='pagelink')
            if pagelink_div:
               for a_tag in pagelink_div.find_all('a'):
                if 'href' in a_tag.attrs:
                    href = a_tag['href']
                    if href.startswith('/book/'):
                        # 提取数字
                        page_number = href.split('/')[-1]
                        # 检查是否为纯数字
                        if page_number.isdigit():
                            # 更改为page_X.html格式
                            a_tag['href'] = f'page_{page_number}.html'


            # 修改所有href属性中的/book/链接
            for a_tag in soup.find_all('a'):
                if 'href' in a_tag.attrs:
                    href = a_tag['href']
                    if href.startswith('/book/'):
                        a_tag['href'] = href.split('/')[-1]



             # 找到并修改"双语小说"链接
            bilingual_novel_link = soup.find('a', text='双语小说')
            if bilingual_novel_link :
                bilingual_novel_link['href'] = 'page_1.html'
                logging.info('已修改双语小说链接为 page_1.html')
                

            # 修改资源链接
            resource_tags = {
                'link': 'href',
                'script': 'src',
                'img': 'src'
            }

            for tag_name, attr_name in resource_tags.items():
                for tag in soup.find_all(tag_name):
                    if attr_name in tag.attrs:
                        tag[attr_name] = '..' + tag[attr_name]

            return str(soup)
            
        except Exception as e:
            logging.error(f'修改HTML链接时出错: {e}')
            return html_content

    def extract_and_save_resources(self, html_content, base_url):
        """
        提取并保存页面中的资源文件
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            resources = []
            for tag in soup.find_all(["img", "link", "script"]):
                resource_url = None
                resource_type = None

                if tag.name == "img" and tag.get("src"):
                    resource_url = tag["src"]
                    resource_type = "img"
                elif tag.name == "link" and tag.get("href"):
                    resource_url = tag["href"]
                    resource_type = "css"
                elif tag.name == "script" and tag.get("src"):
                    resource_url = tag["src"]
                    resource_type = "js"

                if resource_url:
                    full_url = urljoin(base_url, resource_url)
                    resources.append((full_url, resource_type))

            # 使用线程池并发下载资源
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = [
                    executor.submit(self.download_resource, url, res_type)
                    for url, res_type in resources
                ]
                concurrent.futures.wait(futures)

        except Exception as e:
            logging.error(f'提取和保存资源时出错: {e}')

    def download_resource(self, url, resource_type):
        """
        下载单个资源文件
        """
        try:
            parsed_url = urlparse(url)
            
            # 确定资源保存路径
            if resource_type == "img":
                path_parts = parsed_url.path.lstrip('/').split('/')
                if path_parts[0] == 'img':
                    path_parts = path_parts[1:]
                resource_path = self.output_dir / "img" / '/'.join(path_parts)
            elif resource_type == "css":
                filename = os.path.basename(parsed_url.path)
                resource_path = self.output_dir / "public/skin/css" / filename
            elif resource_type == "js":
                filename = os.path.basename(parsed_url.path)
                resource_path = self.output_dir / "public/skin/js" / filename
            else:
                return

            # 如果文件已存在，跳过下载
            if resource_path.exists():
                return

            resource_path.parent.mkdir(parents=True, exist_ok=True)

            # 下载资源
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            with open(resource_path, 'wb') as file:
                file.write(response.content)
            logging.info(f'已下载资源 {url} 到 {resource_path}')

        except Exception as e:
            logging.error(f'下载资源 {url} 失败: {e}')

    def scrape_and_save_page(self, page_number):
        """
        爬取并保存单个页面及其相关内容
        """
        try:
            page_path = f"/book?page={page_number}"
            url = urljoin(self.base_url, page_path)
            logging.info(f'开始处理第 {page_number} 页')
            
            html_content = self.fetch_page(url)
            if not html_content:
                return

            # 保存页面
            self.save_html(html_content, f"page_{page_number}.html")
            
            # 处理页面资源
            self.extract_and_save_resources(html_content, url)
            
            # 下载书籍链接
            self.download_book_links(html_content)
            
            logging.info(f'第 {page_number} 页处理完成')

        except Exception as e:
            logging.error(f'处理第 {page_number} 页时出错: {e}')

    def download_book_links(self, html_content):
        """
        下载页面中的所有书籍链接
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            book_links = soup.find_all('a', class_='book')

            for link in book_links:
                book_url = link['href']
                full_book_url = urljoin(self.base_url, book_url)
                book_filename = os.path.basename(book_url)
                
                if not book_filename.endswith('.html'):
                    book_filename += '.html'

                book_content = self.fetch_page(full_book_url)
                if book_content:
                    self.save_html(book_content, book_filename)
                    logging.info(f'已下载书籍页面: {book_filename}')
                    self.download_chapters(book_content, full_book_url)

        except Exception as e:
            logging.error(f'下载书籍链接时出错: {e}')

    def download_chapters(self, book_content, base_url):
        """
        下载书籍的所有章节
        """
        try:
            soup = BeautifulSoup(book_content, 'html.parser')
            chapter_links = soup.find_all('a')

            for chapter in chapter_links:
                if 'href' not in chapter.attrs:
                    continue
                    
                chapter_url = chapter['href']
                if chapter_url.startswith('/book/'):
                    full_chapter_url = urljoin(base_url, chapter_url)
                    chapter_content = self.fetch_page(full_chapter_url)
                    
                    if chapter_content:
                        chapter_filename = os.path.basename(chapter_url)
                        if not chapter_filename.endswith('.html'):
                            chapter_filename += '.html'

                        self.save_html(chapter_content, chapter_filename)
                        logging.info(f'已下载章节页面: {chapter_filename}')
                        self.extract_and_save_resources(chapter_content, full_chapter_url)

        except Exception as e:
            logging.error(f'下载章节时出错: {e}')

    def scrape_multiple_pages(self, start_page=1, end_page=10):
        """
        爬取多个页面
        """
        try:
            logging.info(f'开始爬取页面 {start_page} 到 {end_page}')
            start_time = datetime.now()

            for page_number in range(start_page, end_page + 1):
                self.scrape_and_save_page(page_number)
                sleep(1)  # 防止请求过快

            end_time = datetime.now()
            duration = end_time - start_time
            
            # 打印统计信息
            logging.info('爬取完成！统计信息：')
            logging.info(f'总耗时: {duration}')
            logging.info(f'成功下载页面数: {self.downloaded_pages}')
            logging.info(f'失败页面数: {self.failed_pages}')
            
        except KeyboardInterrupt:
            logging.info('收到中断信号，正在停止爬虫...')
            sys.exit(0)
        except Exception as e:
            logging.error(f'爬取多个页面时出错: {e}')

def main():
    """
    主程序入口
    """
    try:
        # 创建爬虫实例
        scraper = BookScraper()
        
        # 获取用户输入的页面范围
        start_page = int(input("请输入起始页码（默认为1）：") or "1")
        end_page = int(input("请输入结束页码（默认为32）：") or "32")
        
        # 验证输入
        if start_page < 1 or end_page < start_page:
            raise ValueError("页码范围无效")
        
        # 开始爬取
        scraper.scrape_multiple_pages(start_page, end_page)
        
    except ValueError as e:
        logging.error(f'输入错误: {e}')
    except Exception as e:
        logging.error(f'程序运行出错: {e}')
    finally:
        logging.info('程序结束')

if __name__ == "__main__":
    main()