# -*- coding: utf-8 -*-
#filename:web_spider.py

import urllib2,cookielib
import re
from pymongo import MongoClient
from bson.objectid import ObjectId
import time


tag_arr = [
    {u"文学":[u"小说",u"外国文学",u"文学",u"随笔",u"中国文学",u"经典",u"散文",u"日本文学",u"村上春树",u"童话",u"诗歌",u"王小波",u" 张爱玲",u"杂文",u"名著",u"儿童文学",u"古典文学",u"余华",u"钱钟书",u"当代文学",u"鲁迅",u"外国名著",u"诗词",u"杜拉斯",u"茨威格",u"米兰·昆德拉",u"港台"]},
    {u"流行":[u"漫画",u"绘本",u"推理",u"青春",u"言情",u"科幻",u"韩寒",u"武侠",u"亦舒",u"耽美",u"悬疑",u"日本漫画",u"奇幻",u"东野圭吾",u"安妮宝贝",u"三毛",u"郭敬明",u"网络小说",u"穿越",u"几米",u"金庸",u"轻小说",u"推理小说",u"幾米",u"阿加莎·克里斯蒂",u"张小娴",u"魔幻",u"高木直子",u"青春文学",u"张悦然",u"沧月",u"落落",u"J.K.罗琳",u"古龙",u"蔡康永",u"余秋雨"]},
    {u"文化":[u"历史",u"心理学",u"哲学",u"传记",u"文化",u"社会学",u"设计",u"艺术",u"政治",u"社会",u"建筑",u"宗教",u"电影",u"数学",u"政治学",u"思想",u"回忆录",u"国学",u"中国历史",u"人文",u"音乐",u"戏剧",u"人物传记",u"绘画",u"佛教",u"艺术史",u"军事",u"西方哲学",u"自由主义",u"二战",u"近代史",u"考古",u"美术"]},
    {u"生活":[u"爱情",u"旅行",u"生活",u"励志",u"摄影",u"成长",u"心理",u"职场",u"女性",u"游记",u"美食",u"教育",u"灵修",u"情感",u"健康",u"手工",u"养生",u"两性",u"家居",u"人际关系",u"自助游"]},
    {u"经管":[u"经济学",u"管理",u"经济",u"金融",u"商业",u"投资",u"营销",u"理财",u"广告",u"创业",u"股票",u"企业史",u"策划"]},
    {u"科技":[u"科普",u"互联网",u"编程",u"科学",u"交互设计",u"用户体验",u"算法",u"web",u"科技",u"UE",u"UCD",u"通信",u"交互",u"神经网络",u"程序"]}
]

douban_cookie = None
def douban_request(url, fa=False):
    global  douban_cookie

    try:
        cj = cookielib.CookieJar()
        cookie = 'bid="88mRMhtUwU8"; ll="118172"; viewed="4146512_3718493_10573438_2132932_11499033_11506062_11502889_1465799_4301662"; dbcl2="47629080:urf9C+6RZxE"; ct=y; ck="RcLy"; __utma=30149280.695353401.1356359684.1357742370.1357827450.14; __utmb=30149280.9.9.1357829363041; __utmc=30149280; __utmz=30149280.1356754044.4.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=30149280.4762'
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        #if douban_cookie != None:
        opener.addheaders.append(('Cookie',cookie))
        html = opener.open(url, timeout=10).read()
        if fa:
            print html
        #print html
        if html == None:
            print "ReRequest"
            raise Exception
        #if cj._cookies != None:
        #    cs = ['%s=%s' %(c.name, c.value) for c in cj._cookies[".douban.com"]['/']['bid']]
        #    douban_cookie = ';'.join(cs)
       # print douban_cookie
        print "Request %s Success %s" %(url.decode("utf-8"), time.strftime("%Y-%m-%d %H:%M%S", time.localtime()))
        return html
    except Exception:
        print "Request %s Fail,Waiting to retry %s" %(url.decode("utf-8"),  time.strftime("%Y-%m-%d %H:%M%S", time.localtime()))
        time.sleep(30)
        return douban_request(url, True)

def get_all_book_tag():
    global conn
    base_url = "http://book.douban.com/tag"
    html = douban_request(base_url)
    r = re.compile(r'<td><a href=".(.+?)">(.+?)</a><b>\((.+?)\)</b></td>')
    tag_list = r.findall(html)
    db = conn.mybook
    table_tag = db.tag
    tags = []
    for tag in tag_list:
        if db.tag.find_one({"name":tag[1]}) != None:
            continue
        tags.append({"url":base_url + tag[0], "name":tag[1]})
        print "url:" + base_url + tag[0].decode("utf-8")
        print "name:" + tag[1].decode("utf-8")
    if len(tags) > 0:
        table_tag.insert(tags)

#def get_douban_book_info():


def get_book_info(url):
    start = 0
    request_url = url
    ids = []
    global  conn
    db = conn.mybook
    api_url = "https://api.douban.com/v2/book/"
    while(True):
        print "request_url:" + request_url
        html = douban_request(request_url.encode('utf-8'))
        rt = re.compile(r'<a href="http://book.douban.com/subject/(.*)/".*')
        if html != None:
            ids.extend(rt.findall(html))
        books = []
        for id in ids:
            if db.book.find({"book_id":id}).count() != 0:
                continue
            rurl = api_url + str(id)
            book_info = douban_request(rurl.encode('utf-8'))

            books.append({"book_id":id,"book_info":book_info})
            print rurl + " Success " + time.strftime("%Y-%m-%d %H:%M%S", time.localtime())
        if len(books) != 0:
            try:
                db.book.insert(books)
                print "Insert Success! " + time.strftime("%Y-%m-%d %H:%M%S", time.localtime())
            except:
                print "Error" +  time.strftime("%Y-%m-%d %H:%M%S", time.localtime())

        np = re.compile(r'<a href="/tag/.*(\?start=.*)" >后页.*</a>')
        try:
            request_url = url +np.findall(html)[0]
            ids = []
        except:
            print "Tag End\n" +  time.strftime("%Y-%m-%d %H:%M%S", time.localtime())
            break


def get_books():
    global  conn
    db = conn.mybook
    tags_cur = db.tag.find({"_id":{"$gt":ObjectId("50f420617d0fe51a2c179a33")}})

    for tag in tags_cur:
        try:
            url = tag["url"]
            get_book_info(url)
        except:
            continue

conn = MongoClient('127.0.0.1',5566)

def set_cate_tag():
    global  conn
    db = conn.mybook
    for t in tag_arr:
        cate = t.keys()[0]
        print cate
        cat_cur = db.category.find_one({"name":cate})
        tag_list = []
        for tag in t[cate]:
            tt = db.tag.find_one({"name": tag})
            if tt != None:
                print tt["name"]
                tag_list.append(tt)

        cat_cur["tags"] = tag_list
        db.category.update({"name":cate},cat_cur)
if __name__ == "__main__":
    get_books()
    #set_cate_tag()
    #get_book_tags()
