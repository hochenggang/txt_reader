# coding=utf-8
import os
import functools

from tools import timestamp, to_md5, str_uuid1

# 建立数据模型

MODULE_PATH = os.path.split(__file__)[0]
from sqlalchemy import Column, String, Integer, create_engine, func, desc, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
DB_PATH = os.path.join(MODULE_PATH, "book.db")
ENGINE = create_engine("sqlite:///" + DB_PATH, connect_args={'check_same_thread': False})
SESSION = sessionmaker(bind=ENGINE)
Base = declarative_base()
class Book_info(Base):
    """
    书籍模型
    
    """
    __tablename__ = "book_info"
    book_id = Column(String(32), primary_key=True)
    book_name = Column(String(320), index=True)
    book_size = Column(Integer)
    book_status = Column(Integer)
    book_upload_time = Column(Integer)
    user_id = Column(String(32), index=True)

class Book_chapter(Base):
    """
    章节模型
    
    """
    __tablename__ = "book_chapter"
    chapter_id = Column(Integer, autoincrement=True, primary_key=True)
    chapter_content = Column(String(32000))
    chapter_title = Column(String(320))
    chapter_index = Column(Integer)
    book_id = Column(String(32), index=True)


# 尝试创建所有表
try:
    Base.metadata.create_all(ENGINE)
except:
    pass

#使用 SESSION 调用一個实例 session = SESSION(bind=ENGINE.connect())




class Book:
    """书籍操作类"""

    def new_book(self,user_id=None,book_id=None,book_name=None,book_size=None,book_status=None,book_upload_time=None):
        '''
        描述：新建书籍
        参数：
            

        返回：
            {"code": 200}
            {"code": 4**, "errmsg":...}

        '''
        session = SESSION(bind=ENGINE.connect())
        new_book = Book_info(
            user_id = user_id,
            book_id = book_id,
            book_name = book_name,
            book_status = book_status,
            book_size = book_size,
            book_upload_time = book_upload_time
        )
        session.add(new_book)
        session.commit()
        session.close()
        return {"code": 200}

    def update_book(self,book_id=None,book_status=None):
        '''
        描述：更新书籍
        参数：

        返回：
            {"code": 200}
            {"code": 4**, "errmsg":...}

        '''
        session = SESSION(bind=ENGINE.connect())
        query = session.query(Book_info).filter(Book_info.book_id == book_id).first()
        if query:
            if book_status:
                query.book_status = book_status

        session.commit()
        session.close()
        return {"code": 200}

    def books(self,user_id=None):
        '''
        描述：查询用户的书籍
        参数：
            user_id String(32)

        返回：
            {"code": 200,"query":query}
            {"code": 4**, "errmsg":...}

        '''
        
        session = SESSION(bind=ENGINE.connect())
        query = session.query(Book_info).filter(Book_info.user_id == user_id).all()
        session.close()
        if not query:
            return {"code": 404, "errmsg":"未找到书籍"}
        else:
            return {"code": 200,"query":query}

    def new_chapter(self,book_id=None,chapter_index=None,chapter_title=None,chapter_content=None):
        '''
        描述：新建章节
        参数：
            

        返回：
            {"code": 200}
            {"code": 4**, "errmsg":...}

        '''
        session = SESSION(bind=ENGINE.connect())
        new_c = Book_chapter(
            book_id = book_id,
            chapter_index = chapter_index,
            chapter_title = chapter_title,
            chapter_content = chapter_content
        )
        session.add(new_c)
        session.commit()
        session.close()
        return {"code": 200}

    def catalogue(self,book_id=None):
        '''
        描述：查询用户的书籍
        参数：
            user_id String(32)

        返回：
            {"code": 200,"query":query}
            {"code": 4**, "errmsg":...}

        '''
        
        session = SESSION(bind=ENGINE.connect())
        query = session.query(Book_chapter.chapter_index,Book_chapter.chapter_title).filter(Book_chapter.book_id == book_id).all()
        session.close()
        if not query:
            return {"code": 404, "errmsg":"未找到书籍"}
        else:
            return {"code": 200,"query":query}

    def get_chapter(self,book_id=None,chapter_index=None):
        '''
        描述：查询某章
        参数：

        返回：
            {"code": 200,"query":query}
            {"code": 4**, "errmsg":...}

        '''
        
        session = SESSION(bind=ENGINE.connect())
        query = session.query(Book_chapter.chapter_title,Book_chapter.chapter_content).filter(and_(Book_chapter.book_id == book_id,Book_chapter.chapter_index == chapter_index)).first()
        session.close()
        if not query:
            return {"code": 404, "errmsg":"未找到书籍"}
        else:
            return {"code": 200,"query":query}

    # def delete(self,id=None):
    #     '''
    #     描述：删除文章
    #     参数：
    #         id Integer 文章唯一标识
    #     返回：
    #         {"code": 200}
    #         {"code": 4**, "errmsg":...}

    #     '''
    #     if not bool(id):
    #         return {"code": 400, "errmsg": "缺少文章唯一标识"}

    #     session = SESSION(bind=ENGINE.connect())
    #     record = session.query(DB).filter(DB.id == id).first()
    #     if not record:
    #         return {"code": 404, "errmsg": "文章不存在"}
    #     else:
    #         session.delete(record)
    #         session.commit()
    #         session.close()
    #         return {"code": 200}


    # def all(self,limit=1000,offset=0):
    #     '''
    #     描述：所有文章
    #     参数：
    #         limit Integer 需要数量
    #         offset Integer 需要数量

    #     返回：
    #         {"code": 200,"records":records}
    #         {"code": 4**, "errmsg":...}

    #     '''

    #     session = SESSION(bind=ENGINE.connect())
    #     records = (
    #         session.query(DB)
    #         .order_by(desc(DB.id))
    #         .limit(limit)
    #         .offset(offset)
    #         .all()
    #     )
    #     session.close()
    #     return {"code": 200,"records":records}

    # def one(self,id=None):
    #     '''
    #     描述：根据 id 查询一篇文章
    #     参数：
    #         id Integer 文章唯一标识

    #     返回：
    #         {"code": 200,"record":record}
    #         {"code": 4**, "errmsg":...}

    #     '''

    #     session = SESSION(bind=ENGINE.connect())
    #     record = session.query(DB).filter(DB.id == id).first()
    #     session.close()
    #     if record:
    #         return {"code": 200,"record":record}
    #     else:
    #         return {"code": 404,"errmsg":"未找到该文章"}

    # def update(self,id=None,title=None,brief=None,content=None):
    #     '''
    #     描述：更新文章
    #     参数：
    #         id Integer  文章唯一标识
    #         title String 0<len<50 文章标题
    #         brief String 0<len<500 文章摘要
    #         content String 0<len<5000 文章正文

    #     返回：
    #         {"code": 200}
    #         {"code": 4**, "errmsg":...}

    #     '''

    #     # 检查输入
    #     if not bool(title):
    #         return {"code": 400, "errmsg": "缺少标题"}
    #     elif not bool(brief):
    #         return {"code": 400, "errmsg": "缺少摘要"}
    #     elif not bool(content):
    #         return {"code": 400, "errmsg": "缺少正文"}
    #     elif not bool(id):
    #         return {"code": 400, "errmsg": "缺少唯一标识"}
    #     else:
    #         pass

    #     if not(0 < len(title) < 50):
    #         return {"code": 400, "errmsg": "标题长度应小于50个字符"}
    #     elif not(0 < len(brief) < 500):
    #         return {"code": 400, "errmsg": "摘要长度应小于500个字符"}
    #     elif not(0 < len(content) < 50000):
    #         return {"code": 400, "errmsg": "正文长度应小于5000个字符"}
    #     else:
    #         pass

    #     session = SESSION(bind=ENGINE.connect())
    #     a = session.query(DB).filter(DB.id == id).first()
    #     if a:
    #         a.title = title
    #         a.brief = brief
    #         a.content = content
    #         session.add(a)
    #         session.commit()
    #         session.close()
    #         return {"code": 200}

    #     else:
    #         session.close()
    #         return {"code": 500,"errmsg":"内部错误"}


