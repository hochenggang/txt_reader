#coding:utf-8
import re
import time
import queue
import threading

import chardet

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

        threading.Thread(target=loop).start()
        

    def parser(self,book_info=None):
        # 检查文本中的章卷节等结构
        user_id = book_info["user_id"]
        book_id = book_info["book_id"]
        book_path = book_info["book_path"]
        # 打开文件
        with open(book_path,"rb")as f:
            # 读取少量字节做编码测试
            b = f.read(1024)
            encoding = chardet.detect(b)["encoding"]
            if not encoding:
                # 不支持的编码类型
                Book().update_book(book_id=book_id,book_status=-2)

            else:
                b = b + f.read()
                lines = b.decode(encoding,'ignore')
                c = re.compile(r'\S{1,10}?[章节卷回篇册集话]\s+.{1,31}?\n')
                m = c.findall(lines)
                l = c.split(lines)
                if m and l:
                    del l[0]
                    for i in range(len(m)):
                        title = m[i].replace("\n","")
                        content = l[i]
                        Book().new_chapter(book_id=book_id,chapter_index=i,chapter_title=title,chapter_content=content)
                    # 解析完成
                    Book().update_book(book_id=book_id,book_status=1)
                else:
                    # 正则匹配失败
                    Book().update_book(book_id=book_id,book_status=-1)