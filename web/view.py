#-*- coding:utf-8 -*-
import web
from controler import book_controler

render = web.template.render("templates/")


class index:
    def GET(self):
        param = param_handler()
        if param.has_param("name"):
            return self.param_index(param.get_params())
        return self.normal_index()


    def normal_index(self):
        book = book_controler()
        title = "小书库"
        category_list = book.get_categories()
        has_param = False
        top_books = book.get_top_books()
        print "Get normal index page success"
        return render.index(title,category_list,has_param,top_books)

    def param_index(self, params):
        param = param_handler()
        book = book_controler()
        title = "小书库"
        category_name = params["name"]
        category_list = book.get_categories()
        tags = None
        for cate in category_list:
            if cate["name"] == category_name:
                cate["class_name"] = "category-selected"
                tags = cate["tags"]
            else:
                cate["class_name"] = ""
        has_param = True
        books = book.get_books_with_category(param.get_category_name())

        return render.index_category(title,category_list, has_param, books, tags)

class book_detail:
    def GET(self,name):
        return name

class book_detail:
    book = book_controler()
    def GET(self, name):
        detail = self.book.book_detail(name)
        result = ""
        for d in detail:
            result += str(detail[d]) + "\n"
        return "<html><head><meta http-equiv='Content-Type' content='text/html; charset=utf-8'></head><body>" + result + "</body></html>"


class favicon:
    def GET(self):
        return web.seeother('static/image/favicon.ico')

class param_handler:

    def has_param(self, name):
        return web.input().has_key(name)


    def get_params(self):
        return web.input()

    def get_category_name(self):
        try:
            return web.input().name
        except:
            return ""