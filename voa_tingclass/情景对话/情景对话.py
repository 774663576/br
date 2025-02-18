import requests
import time
from bs4 import BeautifulSoup
from pathlib import Path
import json

def parse_dialog_content(html, parent_category, current_cid, current_category, category_title):
    """解析对话内容，包含完整分类信息并打印进度"""
    soup = BeautifulSoup(html, 'html.parser')
    dialogs = []
    
    dialog_divs = soup.select('.clear_div.green_bj.h_jing')
    print(f"找到 {len(dialog_divs)} 条对话内容")
    
    for dialog_div in dialog_divs:
        dialog_data = {
            'parent_category': parent_category,
            'category': current_category,
            'category_title': category_title,
            'cid': current_cid
        }
        
        # 解析标题
        title_block = dialog_div.select_one('.jing_th')
        if title_block:
            title_link = title_block.select_one('.blue_link a')
            dialog_data['title'] = title_link.text if title_link else ''
            print(f"正在处理对话：{dialog_data['title']}")
        
        # 解析对话内容
        content_box = dialog_div.select_one('.h_jing_box')
        if content_box:
            conversations = []
            for dl in content_box.select('.h_jing'):
                eng_text = dl.select_one('dt').get_text(strip=True).replace('a', '', 1)
                chn_text = dl.select_one('dt p').text if dl.select_one('dt p') else ''
                
                reply_eng = dl.select_one('dd').get_text(strip=True).replace('b', '', 1) if dl.select_one('dd') else ''
                reply_chn = dl.select_one('dd p').text if dl.select_one('dd p') else ''
                
                conversations.append({
                    'english': eng_text,
                    'chinese': chn_text,
                    'reply_english': reply_eng,
                    'reply_chinese': reply_chn
                })
            dialog_data['conversations'] = conversations
        
        dialogs.append(dialog_data)
    
    return dialogs

def get_page_content(cid, page):
    """获取页面内容"""
    url = f"https://talk.kekenet.com/index.php/main/article_list.html?cid={cid}&page={page}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        print(f"成功获取页面: {url}")
        return response.text
    except Exception as e:
        print(f"获取页面失败: {url}, 错误: {e}")
        return None

def has_content(html):
    """检查页面是否包含内容"""
    if not html:
        return False
    soup = BeautifulSoup(html, 'html.parser')
    has_content = bool(soup.select('.jing_th'))
    print(f"页面内容检查: {'有内容' if has_content else '无内容'}")
    return has_content

def save_category_json(all_dialogs, save_path, category_name):
    """保存整个分类的对话到一个JSON文件"""
    file_path = save_path / f"{category_name}.json"
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(all_dialogs, f, ensure_ascii=False, indent=2)
        print(f"保存分类文件成功: {file_path}")
    except Exception as e:
        print(f"保存分类文件失败: {file_path}, 错误: {e}")

def create_folder(base_path, category, subcategory):
    """创建保存文件的目录结构"""
    path = Path(base_path) / category / subcategory
    path.mkdir(parents=True, exist_ok=True)
    print(f"创建目录: {path}")
    return path

def main():
    print("开始运行爬虫程序...")
    
    # 基础保存路径
    base_path = Path("crawler_data")
    
    try:
        with open('categories.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            print("成功加载分类配置")
    except Exception as e:
        print(f"加载分类配置失败: {e}")
        return
    
    for main_category in data['categories']:
        category_name = main_category['category']
        
        for item in main_category['items']:
            cid = item['cid']
            subcategory = item['category']
            category_title = item['title']
            
            print(f"\n开始抓取: {category_name} - {category_title} (CID: {cid})")
            
            # 创建保存目录
            save_path = create_folder(base_path, category_name, subcategory)
            
            # 用于存储该分类的所有对话
            all_category_dialogs = []
            
            # 抓取页面
            page = 1
            while page <= 100:
                print(f"\n正在抓取第 {page} 页...")
                
                content = get_page_content(cid, page)
                if not content or not has_content(content):
                    print(f"CID {cid} 已到最后一页: {page-1}")
                    break
                
                # 解析内容并添加到分类列表中
                dialogs = parse_dialog_content(content, category_name, cid, subcategory, category_title)
                all_category_dialogs.extend(dialogs)
                
                print(f"暂停2秒后继续...")
                time.sleep(2)
                page += 1
            
            # 保存整个分类的对话到一个文件
            save_category_json(all_category_dialogs, save_path, subcategory)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"程序执行出错: {e}")