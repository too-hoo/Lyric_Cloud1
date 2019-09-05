# -*- coding:utf-8 -*-
# 网易云音乐 通过歌手ID，生成歌手的词云
import requests
import sys
import re
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
from PIL import Image
import numpy as np
from lxml import etree

headers = {
    'Referer':'http://music.163.com',
    'Host':'music.163.com',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent':'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Cookie': 'nts_mail_user=13414851554@163.com:-1:1; mail_psc_fingerprint=5db4a54adc70a193fddb509c993e72ab; usertrack=CrHth1xlt+xyxyHoAxo7Ag==; _iuqxldmzr_=32; _ntes_nnid=ea59669b450888d59e264eb90549bca6,1550170244048; _ntes_nuid=ea59669b450888d59e264eb90549bca6; WM_TID=xyvLOB%2FiOIJEUFBFFRI5lb3mdj3ECpK4; _ga=GA1.2.1550089258.1554027316; UM_distinctid=16a4553820538-0e6ea05efc360e-b781636-100200-16a4553820661e; NTES_CMT_USER_INFO=114038547%7C%E6%9C%89%E6%80%81%E5%BA%A6%E7%BD%91%E5%8F%8B06P1sj%7Chttp%3A%2F%2Fimg5.cache.netease.com%2Ftie%2Fimages%2Fyun%2Fphoto_default_62.png%7Cfalse%7CbTEzNDE0ODUxNTU0QDE2My5jb20%3D; __gads=ID=194bb414e73eefc4:T=1557908153:S=ALNI_MZrozfSvDktbYoCIxj1zlQ38Azfwg; vinfo_n_f_l_n3=684867ba32c56fdb.1.1.1557908195081.1557908263636.1558946745689; P_INFO=m13414851554@163.com|1562202771|1|mail163|00&99|gud&1561015340&mail163#gud&440100#10#0#0|134554&1||13414851554@163.com; hb_MA-9ADA-91BF1A6C9E06_source=www.baidu.com; mp_MA-9ADA-91BF1A6C9E06_hubble=%7B%22sessionReferrer%22%3A%20%22https%3A%2F%2Fcampus.163.com%2F%22%2C%22updatedTime%22%3A%201562830747484%2C%22sessionStartTime%22%3A%201562830747479%2C%22sendNumClass%22%3A%20%7B%22allNum%22%3A%202%2C%22errSendNum%22%3A%200%7D%2C%22deviceUdid%22%3A%20%22f5cc7d7f-7445-41f5-bfd3-0c90ac5b6d1d%22%2C%22persistedTime%22%3A%201562830747473%2C%22LASTEVENT%22%3A%20%7B%22eventId%22%3A%20%22da_screen%22%2C%22time%22%3A%201562830747484%7D%2C%22sessionUuid%22%3A%20%22e390747a-5b89-40a5-8f91-66154aba171b%22%7D; WM_NI=x9Dl1v3VqS9qN8WxY6ae2aNnkC5qK5ufW0VKST%2FKZjD5Ge2rfGjd6fwZgeeehZWYYZ%2Br0XM1Ut7lx9is1kHlrlt4R55e5I7JKTKzoWP9a7tnnTltUFliSRVrsShiIILxU1Q%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee90f767a9ebfe9ad269aee78bb6d15f839a9b85bc3485928bb7d949919ea09bf92af0fea7c3b92abce78c8db47ef18abfb4bc7b8ee89999dc3ea3bbfe82cd66a99dfb92ca3fb7ba99d1d541918ce1acd96288eb8986b17aa699a685b56eb586a986e86fac8699badc52e9ae00b9d03b97acf98dfb33abadff8ccb68b2b4bcd5d13ff7bbfbaab642898c859bee5d94e7afd8f766ae8ca495d84eb0b79db3d57ab18da88acc4390a89bd2d437e2a3; ntes_kaola_ad=1; JSESSIONID-WYYY=Dhg1Vys3AR2xvArl6yPxWk9eaPF2NPy%2FYnjP6ODPU%5C6viOQQKsIj%2FWnZyJ5Cc7zl63F7PsCgC4XJEqDoDSOB%2BhD70zxytAgbi80aOek34svm3YvnPkC%5CJtEpFeWxcNiFjbUyhlgXzzWo4bsqQA9RiZsufRayCOxv1ghfAY4Pd1Aka%2Bv9%3A1564730069489'
}
# headers = {
# 		'Referer'	:'http://music.163.com',
# 		'Host'	 	:'music.163.com',
# 		'Accept' 	:'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 		'User-Agent':'Chrome/10'
# 	}
# 得到某一首歌的歌词
def get_song_lyric(headers, lyric_url):
    res = requests.request('GET', lyric_url, headers=headers)
    # 输出获取到的每一条歌曲数据
    print(res.json())
    if 'lrc' in res.json():
        lyric = res.json()['lrc']['lyric']
        # 使用正则表达式解析变换的歌词信息
        new_lyric = re.sub(r'[\d:.[\]]','',lyric)
        return new_lyric
    else:
        return ''
        print(res.json())

# 去掉停用词
def remove_stop_words(f):
    stop_words = ['作词','作曲','编曲','Arranger','录音','混声','人声','Vocal','弦乐','Keyboard','键盘','编辑','助理','Assistants','Mixing','Editing','Recording','音乐','制作','Producer','发行','produced','and','distributed']
    for stop_word in stop_words:
        f = f.replace(stop_word, '')
    return f

# 生成词云
def create_word_cloud(f):
    print('根据词频，开始生成词云！')
    f = remove_stop_words(f)
    print('输出去掉停用词之后的文本：',f)
    cut_text = " ".join(jieba.cut(f,cut_all=False, HMM=True))
    wc = WordCloud(
        font_path="./simhei.ttf",
        max_words=100,
        width = 2000,
        height = 1200,
    )
    print(cut_text)
    wordcloud = wc.generate(cut_text)
    # 写词云图片
    wordcloud.to_file("wordcloud.jpg")
    # 显示词云文件
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    
# 得到指定的歌手页面 热门前50的歌曲ID，歌曲名
def get_songs(artist_id):
    page_url = 'https://music.163.com/artist?id=' + artist_id
    # 获取网页的HTML
    res = requests.request('GET', page_url, headers=headers)
    # 使用Xpath解析 前50首热门歌曲
    html = etree.HTML(res.text)
    href_xpath = "//*[@id='hotsong-list']//a/@href"
    name_xpath = "//*[@id='hotsong-list']//a/text()"
    hrefs = html.xpath(href_xpath)
    names = html.xpath(name_xpath)
    # 设置热门歌曲的ID，歌曲名称
    song_ids = []
    song_names = []
    for href, name in zip(hrefs, names):
        # 截取第9个字符之后的id就是对应的歌曲的id
        song_ids.append(href[9:])
        song_names.append(name)
        print(href, ' ',name)
    return song_ids, song_names

# 设置歌手ID，毛不易为https://music.163.com/#/artist?id=12138269
artist_id = '12138269'
[song_ids, song_names] = get_songs(artist_id)

# 所有的歌词
all_word = ''
# 获取每一首歌的歌词
for (song_id, song_name) in zip(song_ids, song_names):
    # 歌词API URL
    lyric_url = 'http://music.163.com/api/song/lyric?os=pc&id=' + song_id + '&lv=-1&kv=-1&tv=-1'
    print(lyric_url)
    lyric = get_song_lyric(headers, lyric_url)
    all_word = all_word + ' ' + lyric
    print(song_name)
    
# 根据词频 生成词云
print(all_word)
create_word_cloud(all_word)