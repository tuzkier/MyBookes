# -*- utf-8 -*-

from pymongo import MongoClient
import random

class data_handler():
    conn  = MongoClient("127.0.0.1", 5566)
    mybook = conn.mybook
    def __init__(self):
        pass

    def get_categories(self):
        return self.mybook.category.find()

    def get_top_books(self):
        return self.mybook.top_book.find()

    def get_books_with_category(self,category_name):
        category = self.mybook.category.find_one({"name":category_name})
        if category == None:
            return None
        books = []
        for tag in category["tags"]:
            books.append(self.mybook.douban_book.find_one({"book_tag.name":tag["name"]}))
        return books

    def set_top_book(self):
        try:
            cates = self.get_categories()
            for cate in cates:
                tag_len = len(cate["tags"])
                tag_names = []
                for i in range(5):
                    tag_names.append(cate["tags"][random.randint(0,  tag_len - 1)]["name"])
                books = self.mybook.douban_book.find({"book_tag.name":{"$in":tag_names}}).limit(5)
                tb = self.mybook.top_book.find_one({"name":cate["name"]})
                cate["top_books"] = []
                for book in books:
                    cate["top_books"].append(book)
                if tb == None:
                    self.mybook.top_book.insert(cate)
                    print "Insert top book success,category:%s" %(cate["name"])
                else:
                    self.mybook.top_book.update({"name":cate["name"]},{"$set":{"top_books":cate["top_books"]}})
                    print "Update top book success,category:%s" %(cate["name"])
        except:
            print "Set top book fail"

    def insert_top_book(self, books):
        db = self.conn.mybook
        db.top_book.insert(books)