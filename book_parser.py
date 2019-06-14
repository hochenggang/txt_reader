#coding:utf-8
import re
import time
import queue
import threading

from model.book.book import Book

class Book_parser(object):
    def __init__(self):
        # 读取文件, user_id=None, book_path=None
        # 创建队列
        self.Q = queue.Queue()
        def loop():
            while True:
                if self.Q.empty():
                    time.sleep(5)
                else:
                    self.parser(book_info=self.Q.get())
                    time.sleep(1)
        threading.Thread(target=loop).start()
        

    def parser(self,book_info=None):
        # 检查文本中的章卷节等结构
        print("开始解析")
        print(book_info)
        user_id = book_info["user_id"]
        book_id = book_info["book_id"]
        book_path = book_info["book_path"]
        # 打开文件
        with open(book_path,"r",encoding="gb2312",errors="ignore")as f:
            lines = "".join(f.readlines())
            c = re.compile(r'\S{1,7}[卷章节]\s+.{1,30}\n?')
            m = c.findall(lines)
            l = c.split(lines)
            del l[0]
            if m and l:
                for i in range(len(m)):
                    title = m[i].replace("\n","")
                    content = l[i]
                    r = Book().new_chapter(book_id=book_id,chapter_index=i,chapter_title=title,chapter_content=content)
                    if not r["code"] == 200:
                        print("失败，{}，{}".format(i,title))
                        break
                    else:
                        print(i)
                Book().update_book(book_id=book_id,book_status=1)
                print("解析完成")
            else:
                print("正则匹配失败")