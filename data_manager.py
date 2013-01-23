# -*- coding:utf-8 -*-

from pymongo import MongoClient
from bson import ObjectId
import sys


def set_book_info():
    conn = MongoClient("127.0.0.1",27017)
    mybook = conn.mybook
    books = mybook.douban_book.find()
    count = 0
    for book in books:
        try:
            print book["book_id"] + "-----" + str(count)
            count += 1
            if not book.has_key("book_info"):
                if book["images"]["small"].find("\\/") != -1:
                    book["images"]["small"] = book["images"]["small"].replace("\\/","\\")
                    book["images"]["large"] = book["images"]["large"].replace("\\/","\\")
                    book["images"]["medium"] = book["images"]["medium"].replace("\\/","\\")
                    mybook.douban_book.update({"book_id":book["book_id"]}, book)
                continue
            bi = book["book_info"]
            #print bi.keys()
            bi_keys = bi.keys()
            for key in bi_keys:
                book[key] = book["book_info"][key]
            book["image"] = book["book_info"]["image"].replace("\\/","\\")
            book["url"] = book["book_info"]["url"].replace("\\/","\\")
            book["alt"] = book["book_info"]["alt"].replace("\\/","\\")
            book["images"]["small"] = book["book_info"]["images"]["small"].replace("\\/","\\")
            book["images"]["large"] = book["book_info"]["images"]["large"].replace("\\/","\\")
            book["images"]["medium"] = book["book_info"]["images"]["medium"].replace("\\/","\\")
            del book["book_info"]
            mybook.douban_book.update({"book_id":book["book_id"]}, book)
        except:
            bc = mybook.douban_book.find({"book_id":book["book_id"]}).count()
            print "repeat:" + book["book_id"]
            if bc > 1:
                mybook.douban_book.remove({"_id":ObjectId(book["_id"])})
                print "delete success"


def cmd_run():
    args = sys.argv[1:]
    for arg in args:
        if arg == '-bi':
            set_book_info()

if __name__ == "__main__":
    cmd_run()