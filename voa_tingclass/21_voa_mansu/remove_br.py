import os
from bs4 import BeautifulSoup

def remove_br_tags_in_directory():
    # 获取脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Processing directory: {current_dir}")  # 调试输出
    
    # 遍历目录下的所有 HTML 文件
    for filename in os.listdir(current_dir):
        if filename.endswith(".html"):
            filepath = os.path.join(current_dir, filename)
            
            # 打开并读取 HTML 文件
            with open(filepath, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
            
            # 查找所有 .contentImage 元素
            content_images = soup.find_all('div', class_='contentImage')
            
            # 对每个 contentImage 删除后面的两个 <br/>
            for content_image in content_images:
                # 获取 contentImage后面紧跟的所有 <br/> 标签
                br_tags = content_image.find_next_siblings('br', limit=2)
                for br_tag in br_tags:
                    br_tag.decompose()  # 删除 <br/> 标签

            # 将修改后的 HTML 写回文件
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(str(soup))

            print(f"Processed: {filename}")

if __name__ == "__main__":
    remove_br_tags_in_directory()