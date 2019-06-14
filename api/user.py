# coding:utf-8
import functools

from flask import Blueprint, make_response, current_app, render_template, request, session, redirect, jsonify, url_for
from tools import timestamp, is_mail_address, to_md5
from model.user.user import User

api_of_user = Blueprint("api_of_user", __name__)


def cross(function):
    @functools.wraps(function)
    def decoration(*args, **kwargs):
        if request.method == "OPTIONS":
            resp = make_response("")
        else:
            resp = make_response(function(*args, **kwargs))
        if "Origin" in request.headers:
            resp.headers["Access-Control-Allow-Origin"] = request.headers["Origin"]
        else:
            resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type,x-user-id,x-user-key"
        
        return resp

    return decoration



def authorize(function):
    '''
    装饰一个视图方法，
    基于 headers 进行鉴权，
    根据鉴权结果决定是否返回被装饰的视图的结果。
    '''
    @functools.wraps(function)
    def decoration(*args, **kwargs):
        if request.method == "OPTIONS":
            return make_response("")
            
        if "x-user-id" in request.headers:
            if "x-user-key" in request.headers:
                input_user_id = request.headers["x-user-id"]
                input_user_key = request.headers["x-user-key"]
                if len(input_user_id) != 32:  return "",400
                if len(input_user_key) != 32:  return "",400
                
                q = User().info(user_id=input_user_id)
                if q["code"] == 200:
                    r = q["query"]
                    if r.user_key == input_user_key:
                        return function(user_id=r.user_id,user_key=r.user_key,*args, **kwargs)
        
        return "",403

    return decoration


@api_of_user.route("/new", methods=["POST","OPTIONS"])
@cross
def api_new_user():
    '''新建用户'''
    
    # 验证表单
    data = {'m':None,'p1':None,'p2':None}
    for key in data.keys():
        if key not in request.form:
            if key == "m":  message = "邮箱地址"
            elif key == "p1": message = "第一次密码"
            elif key == "p2": message = "第二次密码"
            else: pass
            return jsonify({'code':'400','type':'错误','body':'{}需要被填写'.format(message)}),400
        else:
            data[key] = request.form[key]
    
    # 验证邮箱
    if not is_mail_address(raw=data["m"]): return jsonify({'code':'400','type':'错误','body':'错误的邮箱地址'}),400
    # 验证密码
    elif not data["p1"] == data["p2"]: return jsonify({'code':'400','type':'错误','body':'两次密码不一致'}),400
    else: pass
    
    # 新建用户
    r = User().new(mail=data["m"],password=data["p1"])
    if r["code"] == 200:
        return "",200
    else:
        return jsonify({'code':r["code"],'type':'错误','body':r["errmsg"]}),r["code"]


@api_of_user.route("/login", methods=["POST","OPTIONS"])
@cross
def api_login_user():
    '''用户登录'''
    
    # 验证表单
    data = {'m':None,'p':None}
    for key in data.keys():
        if key not in request.form:
            if key == "m":  message = "邮箱地址"
            elif key == "p": message = "密码"
            else: pass
            return jsonify({'code':'400','type':'错误','body':'{}需要被填写'.format(message)}),400
        else:
            data[key] = request.form[key]
    
    # 验证邮箱
    if not is_mail_address(raw=data["m"]): return jsonify({'code':'400','type':'错误','body':'错误的邮箱地址'}),400
    # 验证密码
    else: pass
    mail = data['m']
    password = data['p']
    # 查询用户
    q = User().info(user_id=to_md5(raw=mail))
    if q["code"] == 200:
        r = q["query"]
        if r.user_key == to_md5(raw=password,mix_text=r.user_salt):
            return jsonify({
                "user_id":r.user_id,
                "user_key":r.user_key
            })
        else:
            return jsonify({'code':403,'type':'错误','body':'邮箱与密码不匹配'}),403
    else:
        return jsonify({'code':q["code"],'type':'错误','body':q["errmsg"]}),q["code"]
