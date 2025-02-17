import os
import re

# 设置要遍历的文件夹路径
folder_path = './book'  # 替换为你的文件夹路径

# 匹配需要删除的标签的正则表达式
pattern = re.compile(r'<li><a href="page_1\.html">双语小说</a></li>')

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    if filename.endswith(".html"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 删除匹配的标签
        modified_content = pattern.sub('', content)
        
        # 将修改后的内容写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)

print("处理完成。")
