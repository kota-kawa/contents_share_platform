# ログインなどユーザーに関する処理をまとめた
from flask import Flask, session, redirect
from functools import wraps
import os
import uuid
import MySQLdb
from werkzeug.security import  check_password_hash

UPLOAD_FOLDER = 'static/upload/'

# データベースへの接続とカーソルの生成
connection = MySQLdb.connect(
    host='*****',
    user='*****',
    passwd='*****',
    db='*****',
    # テーブル内部で日本語を扱うために追加
    charset='utf8'
)
cursor = connection.cursor(MySQLdb.cursors.DictCursor)

# ログインしているかの確認
def is_login():
    return 'user_name' in session

# ユーザー名を得る
def get_id():
    return session['user_name'] if is_login() else None


# ログイン必須を処理するデコレーターを定義
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_login():
            return redirect('/login_form')
        return func(*args, **kwargs)
    return wrapper

# メースアドレス、パスワード認証
def email_login(email, password):

    cursor.execute(
        " SELECT * FROM id WHERE mail_address = %s ", (email,))
    result = cursor.fetchall()

    # パスワードが検索に引っ掛からなかったときのためにNULLを入れておく
    pas = None

    if not result:
        return None
    
    # pythonで使えるデータを取得
    for s in result:
        pas = s['password']
    
    hash_pas=check_password_hash(pas,password)
    
    if hash_pas:
        cursor.execute(
            " SELECT * FROM id WHERE password = %s", (pas,))
        result = cursor.fetchall()

        return result 

    elif not hash_pas:
        return None
    
#　Google,Facebook情報の挿入、更新
def database_google_facebook(name, service_name, unique_id, users_picture, users_email):
    
    result_user_name = None

    unique_id = service_name + unique_id

    cursor.execute(
        " SELECT user_name,name,icon,mail_address FROM id WHERE unique_id = %s ", (unique_id,))
    result = cursor.fetchall()
    for i in result:
        result_user_name=i["user_name"]
        result_name=i["name"]
        result_icon=i["icon"]
        result_mail_address=i["mail_address"]
        

    #既に登録されている場合
    if result_user_name is not None:
        session['user_name'] = result_user_name
        return result_user_name
    
    #新規登録データの追加
    user_uuid=uuid.uuid4().hex
    user_name=users_email[:5]+unique_id
    password=str(uuid.uuid4().hex[:10])

    for_username=None
    #ユーザー名が使われていないものになるまで生成
    while(for_username is None):
        cursor.execute(
            " SELECT user_name FROM id WHERE user_name = %s ", (user_name,))
        for_username = cursor.fetchall()
    
    #データベースに登録されていないアカウントだった場合(通常)
    folder = user_name + '-' + user_uuid
    # フォルダーを作成
    os.mkdir(UPLOAD_FOLDER+folder)
    # データベースに送信するファイル名を指定
    folder_name = 'static/upload/'+folder

    cursor.execute(
    " INSERT INTO id  (time,name,user_name,unique_id,mail_address,password,folder,uuid) VALUES (NOW(),%s,%s,%s,%s,%s,%s,%s)", (name, user_name, unique_id, users_email, password,folder_name, user_uuid))

    cursor.execute(
    "UPDATE id SET icon = %s WHERE user_name = %s", (users_picture, user_name))
    connection.commit()
    session['user_name'] = user_name

    return user_name
    