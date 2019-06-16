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
    1. 以文件 MD5 做文件名保存文件。
    2. 将文件信息写入数据库。
    3. 将文件 id 和文件绝对路径传入解析队列。

    要处理以下情况：
        1. 数据库中已存在书籍 MD5 ，就不写入文件
        2. 数据库中已存在书籍 MD5 ，但用户 id 不匹配时，需要为该用户新建一条书籍记录，并检查是否存在已成功解析的记录，如果有，直接修改书籍记录为已完成解析。

    已知问题 已修复：
        但某用户上传一本书且正在解析，而另一用户上传同一书籍时将导致解析重复，产生重复章节数据。
        可以通过修改状态码机制来修复
        目前 状态码机制
             -2 编码错误 
             -1 无法匹配章节
             0 正在解析
             1 解析成功
        可以增加 
            2 表示正在解析
        原有 
            0 修正为 已上传

    '''
    user_id = kwargs["user_id"]
    # 暂时只接受单个文件，如果上传了多个文件，则取其第一项
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

        # 准备存储目录
        if not os.path.isdir(FILE_PATH):
            os.makedirs(FILE_PATH)
        file_to = os.path.join(FILE_PATH,file_md5)

        # 查询该用户的上传量
        # 暂时不限制

        # 查询书籍是否已经入库
        is_book = Book().is_book(book_id=file_md5)
        if is_book["code"] == 200:
            # 跳过文件写入
            pass
        elif is_book["code"] == 404:
            # 只有但全库查不到书记记录时才写入
            if os.path.isfile(file_to):
                pass
            else:
                with open(file_to,'wb')as f:
                    f.write(file_stream)

        # 查询该用户是否已有本书记录
        is_book = Book().is_book(book_id=file_md5,user_id=user_id)
        if is_book["code"] == 404:
            # 只有当 user_id + book_id 无记录时才新建记录
            q = Book().new_book(user_id=user_id,book_id=file_md5,book_name=file_pure_name,book_size=file_size,book_status=0,book_upload_time=timestamp())
            if q["code"] != 200:
                return "",500
        
        # 只有已存在书记记录且状态码为 0 \ 1 \ 2的情况下直接返回 200
        elif is_book["code"] == 200:
            if is_book["query"].book_status == 0:
                return "",200
            if is_book["query"].book_status == 1:
                return "",200
            if is_book["query"].book_status == 2:
                return "",200

        # 查询所有书籍数据是否已有本书 status 为 1 的记录
        is_book = Book().is_book(book_id=file_md5,book_status=1)
        if is_book["code"] == 404:
            # 查不到已经解析的书时才推送到解析队列
            # 还需要检查是否存在正在解析的该书
            is_book = Book().is_book(book_id=file_md5,book_status=2)
            # 当不存在正在解析的书籍时,才加入解析队列
            if is_book["code"] == 404:
                # 更新书籍状态为 2 正在解析
                Book().update_book_status(user_id=user_id,book_id=file_md5,book_status=2)
                BOOK_PARSER.Q.put({
                    "user_id":user_id,
                    "book_id":file_md5,
                    "book_path":file_to
                })
            else:
                Book().update_book_status(user_id=user_id,book_id=file_md5,book_status=2)
        else:
            Book().update_book_status(user_id=user_id,book_id=file_md5,book_status=1)
        
        return "",200



@api_of_book.route("/books", methods=["GET","OPTIONS"])
@cross
@authorize
def get_books(*args,**kwargs):
    '''
    返回用户的书籍列表
    '''
    user_id = kwargs["user_id"]
    
    q = Book().get_book_list(user_id=user_id)
    
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
    
    q = Book().get_catalogue(book_id=book_id)
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
    
    q = Book().get_chapter(book_id=book_id,chapter_index=chapter_index)
    if q["code"] == 200:
        return jsonify(q["query"])
    else:
        return "",500
