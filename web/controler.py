# -*- utf-8 -*-

from bookdata import  data_handler
import threading, time

class book_controler():

    book_data_obj = data_handler()
    def get_categories(self):
        return self.cursor2list(self.book_data_obj.get_categories())

    def get_top_books(self):
       return self.cursor2list(self.book_data_obj.get_top_books())

    def get_books_with_category(self, category_name):
        return self.book_data_obj.get_books_with_category(category_name)

    def cursor2list(self, db_cur):
        result_list = []
        for cur in db_cur:
            result_list.append(cur)
        return result_list


class book_timer():

    def start_timer(self):
        th = threading.Thread(target=self.set_top_book)
        th.start()

    book_data_obj = data_handler()
    def set_top_book(self):
        while True:
            self.book_data_obj.set_top_book()
            time.sleep(1800)
