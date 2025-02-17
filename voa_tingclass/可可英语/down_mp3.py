import requests
import os
from pydub import AudioSegment
from io import BytesIO
from tqdm import tqdm
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

class MP3Downloader:
    def __init__(self, output_folder="mp3"):
        """初始化 MP3 下载器"""
        self.output_folder = Path(output_folder)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self._setup_logging()
        self._setup_output_folder()
    
    def _setup_logging(self):
        """配置日志记录"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('download.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _setup_output_folder(self):
        """创建输出文件夹"""
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"输出文件夹: {self.output_folder}")

    def download_file(self, url, timeout=30):
        """下载文件并返回内容"""
        try:
            response = requests.get(url, headers=self.headers, timeout=timeout)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            self.logger.error(f"下载失败: {url} - {str(e)}")
            raise

    def process_audio(self, audio_content, trim_start=None):
        """处理音频内容，可选择裁剪"""
        try:
            audio = AudioSegment.from_mp3(BytesIO(audio_content))
            if trim_start:
                audio = audio[trim_start * 1000:]
            return audio
        except Exception as e:
            self.logger.error(f"音频处理失败: {str(e)}")
            raise

    def save_audio(self, audio, filepath):
        """保存处理后的音频"""
        try:
            audio.export(filepath, format="mp3")
            self.logger.info(f"已保存: {filepath}")
        except Exception as e:
            self.logger.error(f"保存失败: {filepath} - {str(e)}")
            raise

    def download_and_process(self, item, trim_start=None):
        """下载并处理单个音频文件"""
        try:
            filepath = self.output_folder / f"{item['index']}.mp3"
            
            # 如果文件已存在，跳过
            if filepath.exists():
                self.logger.info(f"文件已存在，跳过: {filepath}")
                return True

            # 下载和处理
            content = self.download_file(item["mp3_url"])
            audio = self.process_audio(content, trim_start)
            self.save_audio(audio, filepath)
            return True

        except Exception as e:
            self.logger.error(f"处理失败 {item['title']}: {str(e)}")
            return False

    def batch_download(self, mp3_list, max_workers=3, trim_start=None):
        """批量下载处理音频文件"""
        total_files = len(mp3_list)
        successful = 0
        failed = 0

        with tqdm(total=total_files, desc="下载进度") as pbar:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                for success in executor.map(
                    lambda item: self.download_and_process(item, trim_start), 
                    mp3_list
                ):
                    if success:
                        successful += 1
                    else:
                        failed += 1
                    pbar.update(1)

        self.logger.info(f"下载完成: 成功 {successful} 个，失败 {failed} 个")
        return successful, failed

def main():
    # MP3 文件列表
    mp3_list = [
  {
    "title": "Lesson21",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331462.html",
    "index": 38,
    "mp3_url": "https://k6.kekenet.com/Sound/2016/07/6160948_3419122dmv.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 6544
  },
  {
    "title": "Lesson20",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331461.html",
    "index": 37,
    "mp3_url": "https://k6.kekenet.com//Sound/2014/09/liyangfengkuang20.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 3958
  },
  {
    "title": "Lesson19",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331460.html",
    "index": 36,
    "mp3_url": "https://k6.kekenet.com//Sound/2014/09/liyangfengkuang19.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 1336
  },
  {
    "title": "Lesson18",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331459.html",
    "index": 35,
    "mp3_url": "https://k6.kekenet.com//Sound/2014/09/liyangfengkuang18.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 6597
  },
  {
    "title": "Lesson17",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331453.html",
    "index": 34,
    "mp3_url": "https://k6.kekenet.com//Sound/2014/09/liyangfengkuang17.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 9667
  },
  {
    "title": "Lesson16",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331377.html",
    "index": 33,
    "mp3_url": "https://k6.kekenet.com//Sound/2014/09/liyangfengkuang16.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 7807
  },
  {
    "title": "Lesson15",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331456.html",
    "index": 32,
    "mp3_url": "https://k6.kekenet.com//Sound/2014/09/liyangfengkuang15.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 5890
  },
  {
    "title": "Lesson14",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331360.html",
    "index": 31,
    "mp3_url": "https://k6.kekenet.com//Sound/2014/09/liyangfengkuang14.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 1855
  },
  {
    "title": "Lesson13",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331352.html",
    "index": 30,
    "mp3_url": "https://k6.kekenet.com//Sound/2014/09/liyangfengkuang13.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 2658
  },
  {
    "title": "Lesson12",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331342.html",
    "index": 29,
    "mp3_url": "https://k6.kekenet.com//Sound/2014/09/liyangfengkuang12.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 7558
  },
  {
    "title": "Lesson11",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331335.html",
    "index": 28,
    "mp3_url": "https://k6.kekenet.com//Sound/2014/09/liyangfengkuang11.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 5933
  },
  {
    "title": "Lesson10",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331332.html",
    "index": 27,
    "mp3_url": "https://k6.kekenet.com//Sound/2014/09/liyangfengkuang10.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 2706
  },
  {
    "title": "Lesson9",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331330.html",
    "index": 26,
    "mp3_url": "https://k6.kekenet.com//Sound/2014/09/liyangfengkuang09.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 3389
  },
  {
    "title": "Lesson8",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331328.html",
    "index": 25,
    "mp3_url": "https://k6.kekenet.com//Sound/2014/09/liyangfengkuang08.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 8124
  },
  {
    "title": "Lesson7",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331327.html",
    "index": 24,
    "mp3_url": "https://k6.kekenet.com//Sound/2014/09/liyangfengkuang07.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 9996
  },
  {
    "title": "Lesson6",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331322.html",
    "index": 23,
    "mp3_url": "https://k6.kekenet.com//Sound/2014/09/liyangfengkuang06.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 3090
  },
  {
    "title": "Lesson5",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331318.html",
    "index": 22,
    "mp3_url": "https://k6.kekenet.com//Sound/2014/09/liyangfengkuang05.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 2333
  },
  {
    "title": "Lesson4",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331315.html",
    "index": 21,
    "mp3_url": "https://k6.kekenet.com//Sound/2014/09/liyangfengkuang04.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 2353
  },
  {
    "title": "Lesson3",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331313.html",
    "index": 20,
    "mp3_url": "https://k6.kekenet.com//Sound/2014/09/liyangfengkuang03.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 9494
  },
  {
    "title": "Lesson2",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-331312.html",
    "index": 19,
    "mp3_url": "https://k6.kekenet.com//Sound/2014/09/liyangfengkuang02.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 1178
  },
  {
    "title": "Lesson1",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-330714.html",
    "index": 18,
    "mp3_url": "https://k6.kekenet.com/Sound/2014/09/liyangfengkuang01_4606281Bej.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 9528
  },
  {
    "title": "Lesson17",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-56248.html",
    "index": 17,
    "mp3_url": "https://k6.kekenet.com/Sound/kouyu/fk365/17.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 6270
  },
  {
    "title": "Lesson16",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-56147.html",
    "index": 16,
    "mp3_url": "https://k6.kekenet.com/Sound/kouyu/fk365/16.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 2634
  },
  {
    "title": "Lesson15",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-56083.html",
    "index": 15,
    "mp3_url": "https://k6.kekenet.com/Sound/kouyu/fk365/15.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 4932
  },
  {
    "title": "Lesson14",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-55953.html",
    "index": 14,
    "mp3_url": "https://k6.kekenet.com/Sound/kouyu/fk365/14.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 9289
  },
  {
    "title": "Lesson13",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-55852.html",
    "index": 13,
    "mp3_url": "https://k6.kekenet.com/Sound/kouyu/fk365/13.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 9679
  },
  {
    "title": "Lesson12",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-55736.html",
    "index": 12,
    "mp3_url": "https://k6.kekenet.com/Sound/kouyu/fk365/12.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 4478
  },
  {
    "title": "Lesson11",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-55649.html",
    "index": 11,
    "mp3_url": "https://k6.kekenet.com/Sound/kouyu/fk365/11.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 9763
  },
  {
    "title": "Lesson10",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-55552.html",
    "index": 10,
    "mp3_url": "https://k6.kekenet.com/Sound/kouyu/fk365/10.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 6898
  },
  {
    "title": "Lesson9",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-55420.html",
    "index": 9,
    "mp3_url": "https://k6.kekenet.com/Sound/kouyu/fk365/09.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 1092
  },
  {
    "title": "Lesson8",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-55296.html",
    "index": 8,
    "mp3_url": "https://k6.kekenet.com/Sound/kouyu/fk365/08.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 1441
  },
  {
    "title": "Lesson7",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-55214.html",
    "index": 7,
    "mp3_url": "https://k6.kekenet.com/Sound/kouyu/fk365/07.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 6587
  },
  {
    "title": "Lesson6",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-55109.html",
    "index": 6,
    "mp3_url": "https://k6.kekenet.com/Sound/kouyu/fk365/06.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 5811
  },
  {
    "title": "Lesson5",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-54955.html",
    "index": 5,
    "mp3_url": "https://k6.kekenet.com/Sound/kouyu/fk365/05.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 6472
  },
  {
    "title": "Lesson4",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-54852.html",
    "index": 4,
    "mp3_url": "https://k6.kekenet.com/Sound/kouyu/fk365/04.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 3659
  },
  {
    "title": "Lesson3",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-54763.html",
    "index": 3,
    "mp3_url": "https://k6.kekenet.com/Sound/kouyu/fk365/03.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 8872
  },
  {
    "title": "Lesson2",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-54680.html",
    "index": 2,
    "mp3_url": "https://k6.kekenet.com/Sound/kouyu/fk365/02.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 6038
  },
  {
    "title": "Lesson1",
    "url": "http://readingstuday.top/kouyu/liyang_fengkuangyingyu365/1327-54679.html",
    "index": 1,
    "mp3_url": "https://k6.kekenet.com/Sound/kouyu/fk365/01.mp3",
    "category": "liyang_fengkuangyingyu365",
    "views": 3921
  }
]
    
    # 创建下载器实例
    downloader = MP3Downloader()
    
    # 开始批量下载
    try:
        successful, failed = downloader.batch_download(
            mp3_list,
            max_workers=3,  # 同时下载的文件数
            trim_start=0  # 可选：裁剪开始时间（秒）
        )
        print(f"\n下载统计:")
        print(f"成功: {successful}")
        print(f"失败: {failed}")
    except KeyboardInterrupt:
        print("\n用户中断下载")
    except Exception as e:
        print(f"\n程序异常: {str(e)}")

if __name__ == "__main__":
    main()