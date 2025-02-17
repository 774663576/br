import os

# 指定包含 HTML 文件的目录
html_dir = './book'

# 要添加的 <script> 标签
script_tag = '<script src="https://code.responsivevoice.org/responsivevoice.js?key=TxZHpgMM"></script>'

# 遍历目录中的所有 HTML 文件
for filename in os.listdir(html_dir):
    # 如果是 HTML 文件
    if filename.endswith('.html'):
        file_path = os.path.join(html_dir, filename)
        
        # 打开并读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 找到 </body> 标签，并将 <script> 标签插入到其上方
        if '</body>' in content:
            content = content.replace('</body>', f'    {script_tag}\n</body>')
        
        # 如果没有 </body> 标签，假设文件结尾并添加脚本
        else:
            content = content + f'\n{script_tag}'
        
        # 将修改后的内容写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"Added script to: {filename}")

print("Script injection completed for all HTML files.")
