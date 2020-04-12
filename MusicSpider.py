import glob
import json
import os
import re
from lxml import etree
# import jieba
# import pyecharts
# import heapq
# import collections

import requests


class MusicSpider:
    def GetLyric1(self, album, id1):
        urls1 = "http://music.163.com/#/album?id="
        urls2 = str(id1)
        urls3 = urls1 + urls2
        # 将不要需要的符号去掉
        urls = urls3.replace("[", "").replace("]", "").replace("'", "").replace("#/", "")
        headers = {
            'Cookie': '_iuqxldmzr_=32; _ntes_nnid=dc7dbed33626ab3af002944fabe23bc4,1524151830800; _ntes_nuid=dc7dbed33626ab3af002944fabe23bc4; __utmz=94650624.1524151831.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=94650624.1505452853.1524151831.1524176140.1524296365.3; __utmc=94650624; WM_TID=RpKJQQ90pzUSYfuSWgFDY6QEK1Gb4Ulg; JSESSIONID-WYYY=7t6F3r9Uzy8uEXHPnVnWTXRP%5CSXg9U3%5CN8V5AROB6BIe%2B4ie5ch%2FPY8fc0WV%2BIA2ya%5CyY5HUBc6Pzh0D5cgpb6fUbRKMzMA%2BmIzzBcxPcEJE5voa%2FHA8H7TWUzvaIt%2FZnA%5CjVghKzoQXNM0bcm%2FBHkGwaOHAadGDnthIqngoYQsNKQQj%3A1524299905306; __utmb=94650624.21.10.1524296365',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
        }
        html = requests.get(urls, headers=headers)
        html1 = etree.HTML(html.text)
        # soup = BeautifulSoup(html1, 'html.parser', from_encoding='utf-8')
        # tags = soup.find_all('li', class_="have-img")
        html_data = html1.xpath('//ul[@class="f-hide"]//a')
        for i in html_data:
            # 注意这个用法
            html_data1 = i.xpath('string(.)')
            # 获取歌曲的id
            html_data2 = str(html_data1)
            pattern1 = re.compile(r'<li><a href="/song\?id=(\d+?)">%s</a></li>' % (html_data2))
            items = re.findall(pattern1, html.text)
            #          print("歌曲的名称为: %s"%(html_data2))
            #           print("歌曲的id为: %s"%(items))
            with open("专辑歌曲信息.txt", 'a') as f:
                print(len(items))
                if (len(items) > 0):
                    f.write("歌曲的名字是: %s!!歌曲的ID是%s \n" % (html_data2, items))
                    f.close()
                print("获取歌曲 %s 以及歌曲的ID %s写入文件成功" % (html_data2, items))
            # http://music.163.com/#/song?id=185617
            # if(len())

    def GetLyric2(self):
        # 首先删除原来的文件，避免重复写入
        for i in glob.glob("*热评*"):
            os.remove(i)
        for i in glob.glob("*歌曲名*"):
            os.remove(i)
        # 直接读取所有内容
        file_object = open("专辑歌曲信息.txt", )
        list_of_line = file_object.readlines()
        aaa = 1
        namelist = ""
        for i in list_of_line:
            # 歌曲的名字是: 同一种调调!!歌曲的ID是['186020']
            pattern1 = re.compile(r'歌曲的名字是: (.*?)!!歌曲的ID是')
            pattern2 = re.compile(r'歌曲的ID是\[(.*?)\]')
            items1 = str(re.findall(pattern1, i)).replace("[", "").replace("]", "").replace("'", "")
            items2 = str(re.findall(pattern2, i)).replace("[", "").replace("]", "").replace('"', "").replace("'", "")

            headers = {
                'Request URL': 'http://music.163.com/weapi/song/lyric?csrf_token=',
                'Request Method': 'POST',
                'Status Code': '200 OK',
                'Remote Address': '59.111.160.195:80',
                'Referrer Policy': 'no-referrer-when-downgrade'
            }
            #      http://music.163.com/api/song/lyric?id=186017&lv=1&kv=1&tv=-1
            urls = "http://music.163.com/api/song/lyric?" + "id=" + str(items2) + '&lv=1&kv=1&tv=-1'
            #     urls = "http://music.163.com/api/song/lyric?id=186018&lv=1&kv=1&tv=-1"
            # print(urls)
            html = requests.get(urls, headers=headers)
            json_obj = html.text
            j = json.loads(json_obj)
            try:
                lrc = j['lrc']['lyric']
                pat = re.compile(r'\[.*\]')
                lrc = re.sub(pat, "", lrc)
                lrc = lrc.strip()
                print(lrc)
                lrc = str(lrc)
                with open("歌曲名-" + items1 + ".txt", 'w', encoding='utf-8') as f:
                    f.write(lrc)
                aaa += 1
                namelist = namelist + items1 + ".txt" + ","
                # 调用获取评论方法，并且把热评写入文件
                self.GetCmmons(items1, items2)
            except:
                print("歌曲有错误 %s !!" % (items1))
            # 读取所有文件，并且把所有的信息输入到一个文件里面去
        # html1 = etree.HTML(html.text)
        print("歌曲一共爬取了%s首 " % (aaa))
        print(namelist)

    def GetCmmons(self, name, id):
        self.name = name
        self.id = id
        # 删除原来的文件 避免重复爬取
        #  urls="http://music.163.com/weapi/v1/resource/comments/R_SO_4_415792918?csrf_token="
        urls = "http://music.163.com/api/v1/resource/comments/R_SO_4_" + str(id)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': '_iuqxldmzr_=32; _ntes_nnid=dc7dbed33626ab3af002944fabe23bc4,1524151830800; _ntes_nuid=dc7dbed33626ab3af002944fabe23bc4; __utmz=94650624.1524151831.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); WM_TID=RpKJQQ90pzUSYfuSWgFDY6QEK1Gb4Ulg; JSESSIONID-WYYY=BgqSWBti98RpkHddEBZcxnxMIt4IdbCqXGc0SSxKwvRYlqbXDAApbgN%2FQWQ8vScdXfqw7adi2eFbe30tMZ13mIv9XOAv8bhrQYC6KRajksuYWVvTbv%2BOu5oCypc4ylh2Dk5R4TqHgRjjZgqFbaOF73cJlSck3lxcFot9jDmE9KWnF%2BCk%3A1524380724119; __utma=94650624.1505452853.1524151831.1524323163.1524378924.5; __utmc=94650624; __utmb=94650624.8.10.1524378924',
            'Host': 'music.163.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
        }
        html = requests.get(urls, headers=headers)
        html.encoding = 'utf8'
        #  html_data = html1.xpath('//div[@class="u-cover u-cover-alb3"]')[0]
        # pattern = re.compile(r'<div class="u-cover u-cover-alb3" title=(.*?)>')
        # items = re.findall(pattern, html.text)
        # print(html.text)
        # 使用json格式化输出
        json_obj = html.text
        j = json.loads(json_obj)
        i = j['hotComments']
        for uu in i:
            print
            username = uu["user"]['nickname']
            likedCount1 = str(uu['likedCount'])
            comments = uu['content']
            with open(name + "的热评hotComment" + ".txt", 'a+', encoding='utf8') as f:
                f.write("用户名是 " + username + "\n")
                f.write("用户的评论是 " + comments + "\n")
                f.write("被点赞的次数是  " + str(likedCount1) + "\n")
                f.write("----------华丽的的分割线-------------" + "\n")
                f.close()


    def GetAlbum(self):
        urls = "http://music.163.com/artist/album?id=6452&limit=100&offset=0"
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': '_iuqxldmzr_=32; _ntes_nnid=499ef3e49bfef53ee7202f5fb09496ef,1558198370312; _ntes_nuid=499ef3e49bfef53ee7202f5fb09496ef; WM_TID=iA7swAQed0NBAQARVBN42PTPtvRxxfMO; mail_psc_fingerprint=7e6ee2127b168b0568bb4f7f8e9a6911; usertrack=CrH1sl0bb1xNcd0FAwvRAg==; _ga=GA1.2.381740040.1578486407; UM_distinctid=17001630d61b02-0fcd6156a01979-b383f66-151800-17001630d6216b; hb_MA-BFF5-63705950A31C_source=www.baidu.com; nts_mail_user=liguangyao2020@163.com:-1:1; __oc_uuid=0fde7f20-6481-11ea-a424-3fbace330896; P_INFO=liguangyao2020@163.com|1585882501|0|mail163|00&99|shx&1585879663&carddav#shd&370200#10#0#0|&0|mail163&mail163_qrcode&mailmaster_ios|liguangyao2020@163.com; NTES_CMT_USER_INFO=304316915%7C%E6%9C%89%E6%80%81%E5%BA%A6%E7%BD%91%E5%8F%8B0i8U7P%7Chttp%3A%2F%2Fcms-bucket.nosdn.127.net%2F2018%2F08%2F13%2F078ea9f65d954410b62a52ac773875a1.jpeg%7Cfalse%7CbGlndWFuZ3lhbzIwMjBAMTYzLmNvbQ%3D%3D; vinfo_n_f_l_n3=f9a6bfcfdc0df016.1.6.1563366733956.1584356094682.1586449375299; JSESSIONID-WYYY=W5dV%5CO%2Fmka8dpBIHgbDEgCojWgePvrcXJAG3FDZskcTENBRiSYUaYxWWPwuxCMrTgfQqIMPmqXANVQxX7e9dskT044Wo5JzHbwqUGC6dSS01TPoMYt8eygxpohC%5CsC3ip3sJICz3SMly3UPNvg3M%2FTuA1USzhAaEjFAOs8X7%2BYc1Fiaq%3A1586581754502; WM_NI=WTl65vIfTAsFmpjXSG5TA3GCRMV1GVbdsjMlI%2FXl0dEdnpa8hgGUvdRq80gotFcHbJ4wmX3yHhegFq0giNbzqY5XVUDI95C%2FdwmgjtA1EpprxuuIGkCHfiJ2KUlo61p%2BUGg%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb0d45e959996a5b85ab7bc8ab3d55f879b9ebaf14abbb9bed2e75df7aabfa9cc2af0fea7c3b92a958ca4d7b87e8bba9ca2f24eafb0a6b9d24df78c8fd4c64992939ad2c65ea2bcbd8bd0688bf1988db37087bca291e434acb989b6f57092aff8d1e665b89aada9e142f8a9a3b9b2738cb8ab88c57bf4b9a7afe172b387fbb9d55f8897f7d6c225a8a9a388e98083ef8b91f37abcabbbaac6618198aa8ac93a898ba490b53bb4f59ba8e637e2a3; playerid=55616193',
            'Host': 'music.163.com',
            'Referer': 'https://music.163.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
        }
        html = requests.get(urls, headers=headers)
        html1 = etree.HTML(html.text)
        html_data = html1.xpath('//div[@class="u-cover u-cover-alb3"]')[0]
        pattern = re.compile(r'<div class="u-cover u-cover-alb3" title=(.*?)>')
        items = re.findall(pattern, html.text)
        cal = 0
        # 首先删除这个文件，要不然每次都是追加
        if (os.path.exists("专辑信息.txt")):
            os.remove("专辑信息.txt")
        # 删除文件避免每次都要重复写入
        if (os.path.exists("专辑歌曲信息.txt")):
            os.remove("专辑歌曲信息.txt")
        for i in items:
            cal += 1
            # 这里需要注意i是有双引号的，所以需要注意转换下
            p = i.replace('"', '')
            # 这里在匹配里面使用了字符串，注意下
            pattern1 = re.compile(r'<a href="/album\?id=(.*?)" class="tit s-fc0">%s</a>' % (p))
            id1 = re.findall(pattern1, html.text)
            #   print("专辑的名字是:%s!!专辑的ID是%s:"%(i,items1))
            with open("专辑信息.txt", 'a') as f:
                f.write("专辑的名字是:%s!!专辑的ID是%s \n:" % (i, id1))
                f.close()
                self.GetLyric1(i, id1)
        #  print("总数是%d"%(cal))
        print("获取专辑以及专辑ID成功！！！！！")


if __name__ == '__main__':
    c = MusicSpider()
    # c.GetAlbum()
    # c.GetLyric1("不爱我就拉倒", 38721188)
    c.GetCmmons("床边故事",415792916)