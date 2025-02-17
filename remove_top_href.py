from bs4 import BeautifulSoup
import os

def process_html_file(file_path):
    # 读取HTML文件
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(content, 'html.parser')
    
    # 找到所有class为title_left的div
    title_left_divs = soup.find_all('div', class_='title_left')
    
    for div in title_left_divs:
        # 保存章节标题span
        chapter_span = div.find('span')
        
        # 清空div内容
        div.clear()
        
        # 重新添加章节标题span
        div.append(chapter_span)
    
    # 处理pagebar
    pagebar_divs = soup.find_all('div', class_='pagebar')
    for div in pagebar_divs:
        # 找到所有链接
        links = div.find_all('a')
        for link in links:
            # 如果是"回目录"链接，删除它
            if '回目录' in link.text:
                link.decompose()
    
    # 将修改后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

def process_directory(directory_path):
    # 遍历目录下的所有html文件
    for filename in os.listdir(directory_path):
        if filename.endswith('.html'):
            file_path = os.path.join(directory_path, filename)
            print(f'Processing {filename}...')
            process_html_file(file_path)
            print(f'Finished processing {filename}')

# 使用示例
if __name__ == "__main__":
    # 替换为你的HTML文件所在目录路径
    directory_path = "/Users/songbinbin/Downloads/reading_app/book/read_book/book"
    process_directory(directory_path)