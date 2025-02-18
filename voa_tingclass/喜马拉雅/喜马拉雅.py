import execjs
import requests
import pprint

 
def get_timestamp():
    ##获取时间戳
    res = requests.get('https://www.ximalaya.com/revision/time',headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }).text
    return res
 
def get_xm_sign(timestamp):
 
 
    js_Code=open('xmly_jiemi.js').read()
    js_compile = execjs.compile(js_Code)
 
    xm_sign = js_compile.call('get_xmsign',timestamp)
    return xm_sign
 
def get_info(bookName):
    timestamp = get_timestamp()
    xm_sign=get_xm_sign(timestamp)
    print("xm_sign_____"+xm_sign)
    cookies = {
        '_xmLog': 'h5&35b9cf13-8e2c-48eb-9dd4-a6cbe84a8919&process.env.sdkVersion',
        'xm-page-viewid': 'ximalaya-web',
        'impl': 'www.ximalaya.com.login',
        'x_xmly_traffic': 'utm_source%253A%2526utm_medium%253A%2526utm_campaign%253A%2526utm_content%253A%2526utm_term%253A%2526utm_from%253A',
        'wfp': 'ACM4MzFmMjY1NTM5NGY3ZGQ0POuVQ3wgf4B4bXdlYl93d3c',
        'Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070': '1703550655',
        'Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070': '1703567472',
    }
 
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        # 'Cookie': '_xmLog=h5&35b9cf13-8e2c-48eb-9dd4-a6cbe84a8919&process.env.sdkVersion; xm-page-viewid=ximalaya-web; impl=www.ximalaya.com.login; x_xmly_traffic=utm_source%253A%2526utm_medium%253A%2526utm_campaign%253A%2526utm_content%253A%2526utm_term%253A%2526utm_from%253A; wfp=ACM4MzFmMjY1NTM5NGY3ZGQ0POuVQ3wgf4B4bXdlYl93d3c; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1703550655; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1703567472',
        'Pragma': 'no-cache',
        'Referer': 'https://www.ximalaya.com/so/%E6%88%91%E7%9A%84%E8%80%81%E5%8D%83%E7%94%9F%E6%B6%AF',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'xm-sign': xm_sign,
    }
 
    params = {
        'core': 'all',
        'kw': bookName,
        'spellchecker': 'true',
        'device': 'iPhone',
        'live': 'true',
    }
 
    response = requests.get('https://www.ximalaya.com/revision/search/main', params=params, cookies=cookies,
                            headers=headers)

    return response.json()
def download():
    pass
 
 
if __name__ == '__main__':
 
    bookName = input('请输入小说名称：：：')
    res = get_info(bookName)
    pprint.pprint(res)


    books=[]
    for i in res['data']['album']['docs']:
        dic={}
        if i['vipType']!=0 or len(i['priceTypes'])>0:#收费和会员不要 #此处写的比较随意，可以不参考
            pass
        else:
            dic['title']=i['title']
            dic['url'] = 'https://www.ximalaya.com'+i['url']
            dic['priceTypes']=i['priceTypes']
            books.append(dic)
    print(books)
    # url = books[0]['url']
    # title=books[0]['title']
    # albumId = books[0]['url'].split('/')[-1]
 
#后面可以继续扩展，调用download函数，通过名称搜索所有书籍，并进入到书籍明细中，获取每一章节的mp3地址，进行下载。
