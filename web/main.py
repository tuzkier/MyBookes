#-*- utf-8 -*-

import web
from controler import book_timer
urls = (
    '/','view.index',
    '/detail/(.+)','view.book_detail'
)

if __name__ == "__main__":
    try:
        btimer = book_timer()
        btimer.start_timer()
    except:
        print "book timer start fail"
    app = web.application(urls, globals())
    app.run()


