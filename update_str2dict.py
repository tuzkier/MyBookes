from pymongo import MongoClient
from bson.objectid import ObjectId

def do_update():
    conn = MongoClient("127.0.0.1",5566)
    db = conn.mybook
    all_book = db.book.find()

    for b in all_book:
        try:
            if b == None:
                continue
            print b['book_id']
            if b['book_info'] == None:
                continue
            dic = eval(b['book_info'])
            db.douban_book.insert({"book_id":b['book_id'],"book_info":dic})
        except:
            pass

if __name__ == "__main__":
    do_update();
