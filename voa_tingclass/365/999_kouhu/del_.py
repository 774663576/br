import os

def remove_timestamps(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for line in lines:
            # 去掉每行前面的时间戳部分
            cleaned_line = line.split(']')[-1].strip()
            outfile.write(cleaned_line + '\n')

def process_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".html"):  # 只处理 HTML 文件
            input_file = os.path.join(directory, filename)
            output_file = os.path.join(directory, filename)
            remove_timestamps(input_file, output_file)
            print(f"处理完成: {filename}")

# 假设文件在当前目录
directory = './'  # 你可以根据需要修改目录
process_files(directory)
