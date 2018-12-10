# -*- coding:utf-8 -*-
import requests
from lxml import etree
import os
import urllib
import re
import pymysql
import time, datetime
import shutil

def mains():
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Mobile Safari/537.36"
    }
    # 工作简报的URL
    url = "https://mp.weixin.qq.com/s?__biz=MzUyNjg3NTY3NQ==&mid=2247484936&idx=1&sn=3089d49582421de6b3db0fe66aeb469b&scene=19#wechat_redirect"
    sn = "3089d49582421de6b3db0fe66aeb469b"
    r = requests.get(url, headers=headers)
    content = r.content.decode("utf-8")

    html = etree.HTML(content)
    img = html.xpath('//*[@data-s="300,640"]/@data-src')
    toimg = []
    for imgsrc in img:
        if imgsrc == "https://mmbiz.qpic.cn/mmbiz_png/c9WDohZYeusIKA48QwJkXsnhnjo4VLSVLzZia0V6FamdgLfpRh3iaEn69jlVXrLBmaSUsUzXzWLvt4KHGiaYFyiaCw/640?wx_fmt=png" or imgsrc == "https://mmbiz.qpic.cn/mmbiz_jpg/c9WDohZYeuuahWbWibWX02ZN1peEfn8AIBf4GP9kAGBsHCmD7Kx3sPpIMsbPzzQugmbVeyDvSyyDTXUF57c94PA/640?wx_fmt=jpeg":
            pass
        else:
            toimg.append(imgsrc)

    title = re.findall(r"msg_title = \"(.*)\";", content)
    print("标题：{}".format(title[0]))
    description = re.findall(r"msg_desc = \"(.*)\";", content)
    print("简介：{}".format(description[0]))

    # 下载图片
    pics = []
    pic_dir = 'report/images'

    os.mkdir(os.path.join(pic_dir, sn))
    pic_dir = 'report/images/' + sn

    for index, pic_path in enumerate(toimg):
        print(pic_path)
        response = urllib.request.urlopen(pic_path)  # 打开这个链接
        print('in get_pic_code:', response.code)  # 显示状态码
        urllib.request.urlretrieve(pic_path, os.path.join(pic_dir, str(index) + '.jpg'))  # 保存图片
        print("load ok")
        pics.append("/" + pic_dir + "/" + str(index) + '.jpg')

    # 插入数据库
    strs = ""
    for p in pics:
        imgs = "<img src = '{}'>".format(p)
        print(imgs)
        strs += imgs
    print(strs)

    i = int(time.time())
    print(i)
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='table')
    cursor = conn.cursor()

    sql = "INSERT INTO `content` (`title`, `cid`, `description`, `updatetime`, `inputtime`, `status`) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (title, 2, description, i, i, 1))
    contid = cursor.lastrowid
    print(contid)



    sql2 = "INSERT INTO `content_data` (`aid`, `content`) VALUES (%s, %s)"
    cursor.execute(sql2, (contid, strs))
    conn.commit()
    cursor.close()
    conn.close()

    #文件夹复制到另一个目的文件夹里面
    # 复制文件夹：
    olddir = "H:/yizhouguandian/report/images/" + sn
    newdir = "H:/phpstudy/WWW/rgdf/report/images/" + sn
    shutil.copytree(olddir, newdir)  # olddir和newdir都只能是目录，且newdir必须不存在

def getcontent(url):
    # 工作简报的URL
    r = requests.get(url)
    content = r.content.decode("utf-8")
    return content

def gettext(content):
    title = re.findall(r"msg_title = \"(.*)\";", content)
    description = re.findall(r"msg_desc = \"(.*)\";", content)
    print("标题：{}".format(title[0]))
    print("简介：{}".format(description[0]))
    return title,description

def download(content,sn):
    html = etree.HTML(content)
    img = html.xpath('//*[@data-s="300,640"]/@data-src')
    toimg = []
    for imgsrc in img:
        if imgsrc == "https://mmbiz.qpic.cn/mmbiz_png/c9WDohZYeusIKA48QwJkXsnhnjo4VLSVLzZia0V6FamdgLfpRh3iaEn69jlVXrLBmaSUsUzXzWLvt4KHGiaYFyiaCw/640?wx_fmt=png" or imgsrc == "https://mmbiz.qpic.cn/mmbiz_jpg/c9WDohZYeuuahWbWibWX02ZN1peEfn8AIBf4GP9kAGBsHCmD7Kx3sPpIMsbPzzQugmbVeyDvSyyDTXUF57c94PA/640?wx_fmt=jpeg":
            pass
        else:
            toimg.append(imgsrc)
    # 下载图片
    pics = []

    pic_dir = 'report/images'
    os.mkdir(os.path.join(pic_dir, sn))
    pic_dir = 'report/images/' + sn

    for index, pic_path in enumerate(toimg):
        print(pic_path)
        response = urllib.request.urlopen(pic_path)  # 打开这个链接
        print('in get_pic_code:', response.code)  # 显示状态码
        urllib.request.urlretrieve(pic_path, os.path.join(pic_dir, str(index) + '.jpg'))  # 保存图片
        print("load ok")
        pics.append("/" + pic_dir + "/" + str(index) + '.jpg')
    return pics

def getnewcon(pics):
    strs = ""
    for p in pics:
        imgs = "<img src = '{}'>".format(p)
        print(imgs)
        strs += imgs
    print(strs)
    return strs

def main():
    url = input("请输入URL")
    # url = "https://mp.weixin.qq.com/s?__biz=MzUyNjg3NTY3NQ==&mid=2247484813&idx=3&sn=d9ab4562d46c6e88942d0d2c60f32334&scene=19#wechat_redirect"
    sn = input("请输入sn")
    # sn = "d9ab4562d46c6e88942d0d2c60f32334-baks"
    # 获取html
    content = getcontent(url)
    # 获取标题和描述
    title, description = gettext(content)
    # 下载图片
    pics = download(content,sn)
    # 拼接工作简报的详情内容
    content_data = getnewcon(pics)
    # 插入数据库
    i = int(time.time())
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='rungu')
    cursor = conn.cursor()

    sql = "INSERT INTO `gd_content` (`title`, `cid`, `description`, `updatetime`, `inputtime`, `status`) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (title, 2, description, i, i, 1))
    contid = cursor.lastrowid
    print(contid)

    sql2 = "INSERT INTO `gd_content_data` (`aid`, `content`) VALUES (%s, %s)"
    cursor.execute(sql2, (contid, content_data))
    conn.commit()
    cursor.close()
    conn.close()
    # 移动目标图片
    # 复制文件夹：
    olddir = "H:/aa/report/images/" + sn
    newdir = "H:/phpstudy/WWW/report/images/" + sn
    shutil.copytree(olddir, newdir)  # olddir和newdir都只能是目录，且newdir必须不存在



if __name__ == '__main__':
    main()