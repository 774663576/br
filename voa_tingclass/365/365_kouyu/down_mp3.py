import requests
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import time

# 定义下载链接
base_url = "https://online2.tingclass.net/lesson/shi0529/0001/1242/"
urls = [f"{base_url}{i}.mp3" for i in range(1, 73)]

def download_mp3(url, index):
    """下载单个MP3文件"""
    try:
        # 创建文件名
        filename = f"{index:02d}.mp3"
        
        # 如果文件已存在则跳过
        if os.path.exists(filename):
            print(f"文件已存在，跳过: {filename}")
            return
        
        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 下载文件
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        # 获取文件大小
        total_size = int(response.headers.get('content-length', 0))
        
        # 使用tqdm创建进度条
        with open(filename, 'wb') as f, tqdm(
            desc=filename,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                pbar.update(size)
        
        print(f"下载完成: {filename}")
        
    except requests.RequestException as e:
        print(f"下载失败 {filename}: {str(e)}")
        # 如果文件下载失败，删除可能部分下载的文件
        if os.path.exists(filename):
            os.remove(filename)
        return False
    except Exception as e:
        print(f"未知错误 {filename}: {str(e)}")
        if os.path.exists(filename):
            os.remove(filename)
        return False
    
    return True

def main():
    # 创建下载目录
    download_dir = "mp3_downloads"
    os.makedirs(download_dir, exist_ok=True)
    os.chdir(download_dir)
    
    print(f"开始下载MP3文件到目录: {os.path.abspath(download_dir)}")
    
    # 记录开始时间
    start_time = time.time()
    
    # 失败的下载列表
    failed_downloads = []
    
    # 使用线程池并发下载
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 创建下载任务
        future_to_url = {executor.submit(download_mp3, url, i): (url, i) 
                        for i, url in enumerate(urls, 1)}
        
        # 处理完成的任务
        for future in future_to_url:
            url, index = future_to_url[future]
            try:
                if not future.result():
                    failed_downloads.append((url, index))
            except Exception as e:
                print(f'任务产生异常: {str(e)}')
                failed_downloads.append((url, index))
    
    # 计算总用时
    duration = time.time() - start_time
    
    # 打印下载统计
    print("\n下载统计:")
    print(f"总用时: {duration:.2f} 秒")
    print(f"成功下载: {len(urls) - len(failed_downloads)} 个文件")
    print(f"失败下载: {len(failed_downloads)} 个文件")
    
    # 如果有失败的下载，打印失败列表
    if failed_downloads:
        print("\n失败的下载列表:")
        for url, index in failed_downloads:
            print(f"文件 {index:02d}.mp3: {url}")
        
        # 保存失败列表到文件
        with open("failed_downloads.txt", "w", encoding="utf-8") as f:
            for url, index in failed_downloads:
                f.write(f"{index:02d}.mp3,{url}\n")
        print("\n失败的下载列表已保存到 failed_downloads.txt")

if __name__ == "__main__":
    try:
        main()
        print("\n下载任务已完成！")
    except KeyboardInterrupt:
        print("\n下载被用户中断！")
    except Exception as e:
        print(f"\n程序发生错误: {str(e)}")