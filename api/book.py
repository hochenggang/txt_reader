# coding:utf-8
import os
import hashlib

from flask import Blueprint, make_response, render_template, current_app, request, jsonify
from tools import timestamp, string_time, FILE_PATH
from .user import cross,authorize
from model.book.book import Book
from book_parser import Book_parser

api_of_book = Blueprint("api_of_book", __name__)
BOOK_PARSER = Book_parser()

@api_of_book.route("/upload", methods=["POST","OPTIONS"])
@cross
@authorize
def upload_book(**kwargs):
    '''
    接收上传的文件
    1. 以用户id 为文件夹，以文件 MD5 为文件 id 保存文件。
    2. 将文件信息写入数据库。
    3. 将文件 id 和文件绝对路径传入解析队列。
    '''
    user_id = kwargs["user_id"]
    all_file = []
    for file in request.files.to_dict(flat=False)['file']:
        file_name = file.filename
        file_extension = "." + os.path.splitext(file_name)[-1].replace('.','').lower()
        file_pure_name = file_name.replace(file_extension,"")
        # 由于只能读一次流，所以不能分块写入和分块求MD5，因此直接读取整个流
        file_stream = file.stream.read()
        hash_md5 = hashlib.md5()
        hash_md5.update(file_stream)
        file_md5 = hash_md5.hexdigest()
        file.seek(0, os.SEEK_END)
        file_size = file.tell()

        # 查询该用户的上传量


        # 写入文件
        save_to = os.path.join(FILE_PATH,user_id)
        if not os.path.isdir(save_to):
            os.makedirs(save_to)
        file_to = os.path.join(save_to,file_md5 + file_extension)

        if os.path.isfile(file_to):
            return "",200
        else:
            with open(file_to,'wb')as f:
                f.write(file_stream)
        
        # 新建文件记录
        new_time = timestamp()
        q = Book().new_book(user_id=user_id,book_id=file_md5,book_name=file_pure_name,book_size=file_size,book_status=0,book_upload_time=new_time)
        BOOK_PARSER.Q.put({
            "user_id":user_id,
            "book_id":file_md5,
            "book_path":file_to
        })
        return "",200



@api_of_book.route("/books", methods=["GET","OPTIONS"])
@cross
@authorize
def get_books(*args,**kwargs):
    '''
    返回用户的书籍列表
    '''
    user_id = kwargs["user_id"]
    
    q = Book().books(user_id=user_id)
    
    if q["code"] == 200:
        r = []
        for i in q["query"]:
            r.append({
                "book_id":i.book_id,
                "book_name":i.book_name,
                "book_size":round(i.book_size/1024/1024,2),
                "book_status":i.book_status,
                "book_upload_time":string_time(ts=i.book_upload_time,style=2)
            })
        return jsonify(r)

    else:
        return "",404


@api_of_book.route("/catalogue/<book_id>", methods=["GET","OPTIONS"])
@cross
@authorize
def get_catalogue(*args,**kwargs):
    '''
    返回用户的书籍列表
    '''
    user_id = kwargs["user_id"]
    book_id = kwargs["book_id"]
    
    q = Book().catalogue(book_id=book_id)
    if q["code"] == 200:
        return jsonify(q["query"])
    else:
        return "",500

@api_of_book.route("/chapter/<book_id>/<chapter_index>", methods=["GET","OPTIONS"])
@cross
@authorize
def get_chapter(*args,**kwargs):
    '''
    返回用户的书籍列表
    '''
    user_id = kwargs["user_id"]
    book_id = kwargs["book_id"]
    chapter_index = kwargs["chapter_index"]
    print(book_id)
    
    q = Book().get_chapter(book_id=book_id,chapter_index=chapter_index)
    if q["code"] == 200:
        return jsonify(q["query"])
    else:
        return "",500
