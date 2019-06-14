# coding=utf-8
import os
import functools

from tools import timestamp, to_md5, str_uuid1

# 建立数据模型
try:
    MODULE_PATH = os.path.split(__file__)[0]
    from sqlalchemy import Column, String, Integer, create_engine, func, desc
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.declarative import declarative_base
    DB_PATH = os.path.join(MODULE_PATH, "user.db")
    ENGINE = create_engine("sqlite:///" + DB_PATH, connect_args={'check_same_thread': False})
    SESSION = sessionmaker(bind=ENGINE)
    Base = declarative_base()
    class User_account(Base):
        """
        用户模型
        user_id 邮箱 md5(不混淆)
        user_key 密码 md5(使用 user_salt 混淆)
        user_salt 盐值 uuid
        user_mail 邮箱地址 String(64)
        """
        __tablename__ = "user"
        user_id = Column(String(32), primary_key=True, index=True)
        user_key = Column(String(32))
        user_salt = Column(String(32))
        user_mail = Column(String(64), index=True)

    class User_config(Base):
        """
        用户配置
        id 自增，主键
        key 用户配置犍 
        value 用户配置值 
        user_id 用户唯一标识

        key          value
        size         容量
        when_join    加入的时间
        when_forget  上一次忘记密码的时间
        when_reset   上一次重置密码的时间
        """
        __tablename__ = "user_config"
        
        id = Column(Integer, autoincrement=True, primary_key=True)
        key = Column(String(32), index=True)
        value = Column(Integer)
        user_id = Column(String(32), index=True)
    
    # 尝试创建所有表
    try:
        Base.metadata.create_all(ENGINE)
    except:
        pass
    
    #使用 SESSION 调用一個实例 session = SESSION(bind=ENGINE.connect())

except:
    print("数据模型初始化失败")
    



class User:
    """用户操作类"""

    def new(self,mail=None,password=None):
        '''
        描述：新建用户
        参数：
            mail String 0<len<64 用户邮箱地址
            password String 0<len<64 用户密码

        返回：
            {"code": 200}
            {"code": 4**, "errmsg":...}

        '''

        # 检查输入
        if not bool(mail):
            return {"code": 400, "errmsg": "缺少用户邮箱地址"}
        elif not bool(password):
            return {"code": 400, "errmsg": "缺少用户密码"}
        elif not 0 < len(mail) <= 64:
            return {"code": 400, "errmsg": "用户邮箱地址长度不正确"}
        elif not 0 < len(password) <= 64:
            return {"code": 400, "errmsg": "用户密码长度不正确"}
        else:
            pass

        try:
            salt = str_uuid1()
            user_key = to_md5(raw=password,mix_text=salt)
            user_id = to_md5(raw=mail)
            q = self.info(user_id=user_id)
            if not q["code"] == 404: return {"code": 400, "errmsg": "用户已存在"}

            session = SESSION(bind=ENGINE.connect())
            new_user = User_account(
                user_id = user_id,
                user_key = user_key,
                user_salt = salt,
                user_mail = mail
            )
            session.add(new_user)
            session.commit()
            session.close()
            return {"code": 200}
        except:
            return {"code": 500, "errmsg":"系统内部错误"}

    def info(self,user_id=None):
        '''
        描述：查询用户信息
        参数：
            user_id String(32)

        返回：
            {"code": 200,"query":query}
            {"code": 4**, "errmsg":...}

        '''
        
        session = SESSION(bind=ENGINE.connect())
        query = session.query(User_account).filter(User_account.user_id == user_id).first()
        session.close()
        if not query:
            return {"code": 404, "errmsg":"未找到用户"}
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


