# メール送信に必要
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import time
import random
import shutil
from unicodedata import name
# 自分で作ったモジュール
import fs_data
import user_login
import photo_data
import video_data
import audio_data
import code_data
import image_face
import split_words
import my_text
import contents_search
import follow_data

import os
import uuid
import json

from flask import Flask, render_template, session, request, redirect, url_for

from flask_sslify import SSLify
from werkzeug.middleware.proxy_fix import ProxyFix


from werkzeug.utils import secure_filename

from oauthlib.oauth2 import WebApplicationClient
import requests


import MySQLdb

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "*****")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "*****")
GOOGLE_DISCOVERY_URL = (
    "https://*****"
)
FACEBOOK_CLIENT_ID = os.environ.get("FACEBOOK_CLIENT_ID", "*****")
FACEBOOK_CLIENT_SECRET = os.environ.get("FACEBOOK_CLIENT_SECRET", "*****")



# OAuth2 client setup
google_client = WebApplicationClient(GOOGLE_CLIENT_ID)
facebook_client = WebApplicationClient(FACEBOOK_CLIENT_ID)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
sslify = SSLify(app,permanent=True)

app.config['SECRET_KEY'] = "*****"

# ファイルの保存場所
UPLOAD_FOLDER = 'static/upload/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#メール送信用
sendAddress = '*****'
password = '*****'

# 未登録ので1日以上たったSQLの削除
fs_data.remove_data()

@app.route("/google_login")
def login():

    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = google_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/google_login/callback" , methods=['POST','GET'])
def g_callback():
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    userinfo_response = get_userinfo_response(google_client, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, token_endpoint, userinfo_endpoint)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_name = userinfo_response.json()["given_name"]
        users_email = userinfo_response.json()["email"]
        users_picture = userinfo_response.json()["picture"]

        name = userinfo_response.json()["name"]
        name = "".join(name.split())


        print(unique_id,"\n",users_email,"\n",users_picture,"\n",name)
    else:
        return "User email not available or not verified by Google.", 400
    session.pop('user_name', None)
    service_name="g-"
    user_login.database_google_facebook(name, service_name, unique_id, users_picture, users_email)
    return redirect("/")
    
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/facebook_login")
def f_login():
    authorization_endpoint = "https://www.facebook.com/v11.0/dialog/oauth"
    request_uri = facebook_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
    )
    return redirect(request_uri)

@app.route("/facebook_login/callback")
def f_callback():
    token_endpoint = 'https://graph.facebook.com/v11.0/oauth/access_token'
    userinfo_endpoint = 'https://graph.facebook.com/me?fields=id,name,email,picture'
    userinfo_response = get_userinfo_response(facebook_client, FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET, token_endpoint, userinfo_endpoint)
    if userinfo_response.json().get("id"):
        unique_id = userinfo_response.json()["id"]
        name = userinfo_response.json()["name"]
        name = "".join(name.split())
        users_icon = userinfo_response.json()["picture"]
        users_email = userinfo_response.json()["email"]
        icon=users_icon.get('data').get('url')
        print(unique_id,"\n",name,"\n",users_email,"\n",icon)
    else:
        return "User email not available or not verified by FACEBOOK.", 400
    session.pop('user_name', None)
    service_name="f-"
    user_login.database_google_facebook(name, service_name, unique_id, icon, users_email)
    return redirect("/")

def get_userinfo_response(client, CLIENT_ID,CLIENT_SECRET,token_endpoint,userinfo_endpoint):
    code = request.args.get("code")
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(CLIENT_ID, CLIENT_SECRET),
    )
    client.parse_request_body_response(json.dumps(token_response.json()))
    uri, headers, body = client.add_token(userinfo_endpoint)
    return requests.get(uri, headers=headers, data=body)

#トップページ
@app.route('/')
def index():
    me = user_login.get_id()
    # セッションがないときのトップページを表示
    if me == None:
        data = fs_data.select_all_data()
        return render_template('before_top.html', data=data)
    # セッションがあるときのトップページを表示
    data = fs_data.select_all_data()
    video = video_data.select_all_data()
    audio = audio_data.select_all_data()
    code = code_data.select_all_data()

    return render_template('top.html', user_name=me,data=data ,video_data=video, audio_data=audio, code_data=code)
  
#画像ページ
@app.route('/image')
def image():
    me = user_login.get_id()
    # セッションがないときのトップページを表示
    if me == None:
        data = fs_data.select_all_data()
        return render_template('before_top.html', data=data)
    # セッションがあるときのトップページを表示

    image_data = fs_data.select_all_data()

    return render_template('image.html', user_name=me,data=image_data)
  
#ビデオページ
@app.route('/video')
def video():
    me = user_login.get_id()
    # セッションがないときのトップページを表示
    if me == None:
        data = fs_data.select_all_data()
        return render_template('before_top.html', data=data)
    # セッションがあるときのトップページを表示

    video = video_data.select_all_data()

    return render_template('video.html', user_name=me,video_data=video)
  
#音楽ページa
@app.route('/audio')
def music():
    me = user_login.get_id()
    # セッションがないときのトップページを表示
    if me == None:
        data = fs_data.select_all_data()
        return render_template('before_top.html', data=data)
    # セッションがあるときのトップページを表示

    audio = audio_data.select_all_data()

    return render_template('music.html', user_name=me, audio_data=audio)
  
@app.route('/video_sample')
def side():
    return render_template('video_sample.html')

# トップページから検索
@app.route('/search', methods=['POST'])
def search():
    kensaku = request.form.get('kensaku')
    count,user_name_list,folder_list,file_list,file_id_list,album_id_list=contents_search.search(kensaku=kensaku)
    
    me = user_login.get_id()
    # セッションがないとき
    if me == None:
        return render_template('before_search.html', count=count,folder_list=folder_list,file_list=file_list,file_id_list=file_id_list,album_id_list=album_id_list,user_name_list=user_name_list)
  
    return render_template('search.html', count=count,folder_list=folder_list,file_list=file_list,file_id_list=file_id_list,album_id_list=album_id_list,user_name_list=user_name_list)


# ログイン画面の表示
@app.route('/login_form')
def login_form():
    return render_template('login_form.html')

# ログイン画面の表示
@app.route('/login_again')
def login_again():
    return render_template('login_form.html', mode="again")


@app.route('/login', methods=["GET", "POST"])
def login_try():
    # Eメールとパスワードを入力
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    # Eメールとパスワードを照合のために送信
    user = user_login.email_login(email=email, password=password)
    # Eメールとパスワードが一致しなかったとき
    if not user:
        return redirect('/login_again')
    
    for i in user:
        user_name = i["user_name"]
        name=i["name"]

    session['user_name'] = user_name

    return redirect('/user-photos/'+user_name)




# ログアウト
@ app.route('/logout')
def logout():
    return msg('ログアウトしました')


# 新規登録を表示
@ app.route('/register')
def register():
    return render_template('regist.html')


# 新規登録の情報を取得・処理
@ app.route('/register-upload', methods=['POST'])
def register_upload():
    namae = request.form.get('name', '')
    username = request.form.get('username', '')
    toAddress = request.form.get('email', '')
    login_password = request.form.get('password', '')
    user_uuid = uuid.uuid4().hex
    ok = fs_data.kari_toroku(toAddress=toAddress, login_password=login_password,
                             name=namae, username=username, user_uuid=user_uuid)
    print(user_uuid)
    # ユーザー名が重複していた場合
    if not ok:
        return redirect('/login_again')
    url = request.url+"/confirmation/"+toAddress+"/"+username
    print(user_uuid)
    subject = 'Photo Bookの仮登録'
    bodyText = url+'  にアクセスして登録を完了してください'
    fromAddress = '*****'
    # SMTPサーバに接続
    smtpobj = smtplib.SMTP("smtp.gmail.com", 587)
    smtpobj.starttls()
    smtpobj.login(sendAddress, password)
    # メール作成
    msg = MIMEText(bodyText)
    msg['Subject'] = subject
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Date'] = formatdate()
    # 作成したメールを送信
    smtpobj.send_message(msg)
    smtpobj.close()
    return 'メールを確認してください'


# 新規登録の確認画面
@ app.route('/register-upload/confirmation/<kari_mail>/<user_name>')
def confirmation(kari_mail,user_name):
    already=fs_data.account_existence(kari_mail,user_name)

    if already == "error":
        return msg('エラーが発生しました')
    # 仮登録のメールアドレスとパスワードを取り出す
    data = fs_data.select_uuid(user_name)
    mail = ''
    password = ''
    name = ''
    user_uuid  = ''
    for i in data:
        mail = i["kari_mail"]
        password = i["kari_pass"]
        name = i["user_name"]
        user_uuid = i["uuid"]

    # フォルダー名をユーザー名とuuidで作成
    folder = (name + '-' + user_uuid)
    # フォルダーを作成
    os.mkdir(UPLOAD_FOLDER+'/'+folder)
    # データベースに送信するファイル名を指定
    foldername = 'static/upload/'+folder
    # 本登録
    fs_data.regist_user(mail, password, foldername, user_uuid)
    session['user_name'] = name
    return redirect('/')

# ユーザーごとのアップロードフォーム
@ app.route('/up/<user_name>')
@user_login.login_required
def upform(user_name):
    usname = str(user_name)
    # ファイルのアップロードフォームを表示
    return render_template('upload_form.html',  user_name=usname)

# 画像のアップロード動作
@ app.route('/upload/<user_name>', methods=['POST'])
@user_login.login_required
def user_upload(user_name):
    if request.method == 'POST':
        user_data = fs_data.user_data(user_name)
        album_id=str(uuid.uuid4().hex)

        for i in user_data:
            username = i["user_name"]
            name = i["name"]
            foldername = '/'+i['folder']
            uuid1 = i['uuid']
        upfile = request.files.getlist('upfile', None)
        # アップロードしたファイル説明を取得
        title = str(request.form.get('title', ''))
        setsumei = str(request.form.get('explain', ''))
        tag = str(request.form.get('tag', ''))

        tag=tag.replace('　', ',')

        genre3=my_text.check_genre(setsumei)
        
        genre2=split_words.split_mecab_a(title, setsumei)
        print(upfile)
        print(title)
        x=0

        for file in upfile:
            secure_id = str(uuid.uuid4().hex[:5])
            filename = secure_id+'-'+file.filename
            print(filename)
            file_id=username+'-'+secure_id

            user_name_uuid = str(username + '-' + uuid1)
            x+=1
            photo_id = photo_data.ins(
                file_id, filename=filename, user_name_uuid=user_name_uuid, title=title, setsumei=setsumei, tag=tag, username=username, folder=foldername,genre2=genre2,genre3=genre3, file=file,album_id=album_id)
            if photo_id == 0:
                return msg('アップロード失敗')
            #画像を分析
            path=str(foldername+'/'+filename)
            face=image_face.check(path)
            if not face:
                pass
            else:
                photo_data.genre1(face,file_id)
        photo_data.add_album_count(
                album_count=x,album_id=album_id)
        return redirect('/up/'+username)

# 動画のアップロード動作
@ app.route('/video_upload/<user_name>', methods=['POST'])
@user_login.login_required
def vodeo_upload(user_name):
    if request.method == 'POST':
        user_data = fs_data.user_data(user_name)
        album_id=str(uuid.uuid4().hex)

        for i in user_data:
            username = i["user_name"]
            name = i["name"]
            foldername = '/'+i['folder']
            uuid1 = i['uuid']
        upfile = request.files.getlist('video_file', None)
        # アップロードしたファイル説明を取得
        title = str(request.form.get('video_title', ''))
        setsumei = str(request.form.get('video_explain', ''))
        tag = str(request.form.get('video_tag', ''))

        tag=tag.replace('　', ',')

        genre3=my_text.check_genre(setsumei)
        
        genre2=split_words.split_mecab_a(title, setsumei)
        x=0
        
        for file in upfile:
            secure_id = str(uuid.uuid4().hex[:5])
            filename = secure_id+'-'+file.filename
            file_id=username+'-'+secure_id

            user_name_uuid = str(username + '-' + uuid1)
            x+=1
            photo_id = video_data.ins(
                file_id, filename=filename, user_name_uuid=user_name_uuid, title=title, setsumei=setsumei, tag=tag, username=username, folder=foldername,genre2=genre2,genre3=genre3, file=file,album_id=album_id)
            if photo_id == 0:
                return msg('アップロード失敗')
            
        video_data.add_album_count(
                album_count=x,album_id=album_id)
        return redirect('/up/'+username)

# オーディオのアップロード動作
@ app.route('/audio_upload/<user_name>', methods=['POST'])
@user_login.login_required
def audio_upload(user_name):
    if request.method == 'POST':
        BASE_DIR = os.path.dirname(__file__)
        STATIC = BASE_DIR+'/static/upload'

        user_data = fs_data.user_data(user_name)
        album_id=str(uuid.uuid4().hex)

        for i in user_data:
            username = i["user_name"]
            name = i["name"]
            foldername = '/'+i['folder']
            uuid1 = i['uuid']
        audio_img = request.files.get('audio_img', None)
        upfile = request.files.getlist('audio_file', None)
        # アップロードしたファイル説明を取得
        title = str(request.form.get('audio_title', ''))
        setsumei = str(request.form.get('audio_explain', ''))
        tag = str(request.form.get('audio_tag', ''))
        #空白を「,」に置き換える
        tag=tag.replace('　', ',')

        genre3=my_text.check_genre(setsumei)
        
        genre2=split_words.split_mecab_a(title, setsumei)
        x=0
        secure_id = str(uuid.uuid4().hex[:5])
        audio_img_name = str(secure_id+'-'+audio_img.filename)
        user_name_uuid = str(username + '-' + uuid1)
        audio_img.save(STATIC + '/'+user_name_uuid + '/'+audio_img_name)


        for file in upfile:
            x+=1
            secure_id = str(uuid.uuid4().hex[:5])
            filename = secure_id+'-'+file.filename
            #audio_img_name = str(audio_img.filename)
            
            file_id=username+'-'+secure_id

            photo_id = audio_data.ins(
                file_id, filename=filename, user_name_uuid=user_name_uuid, title=title, setsumei=setsumei, tag=tag, username=username, genre2=genre2,genre3=genre3,folder=foldername, file=file, audio_img_name=audio_img_name, album_id=album_id)
            if photo_id == 0:
                return msg('アップロード失敗')
            
        audio_data.add_album_count(
                album_count=x,album_id=album_id)
        return redirect('/up/'+username)



# コードのアップロード動作
@ app.route('/code_upload/<user_name>', methods=['POST'])
@user_login.login_required
def code_upload(user_name):
    if request.method == 'POST':

        user_data = fs_data.user_data(user_name)
        album_id=str(uuid.uuid4().hex)

        for i in user_data:
            username = i["user_name"]
            name = i["name"]
            foldername = '/'+i['folder']
            uuid1 = i['uuid']
            icon = i["icon"]

        upfile = request.files.getlist('code_file', None)
        # アップロードしたファイル説明を取得
        title = str(request.form.get('title', ''))
        setsumei = str(request.form.get('explain', ''))
        tag = str(request.form.get('tag', ''))
        #空白を「,」に置き換える
        tag=tag.replace('　', ',')
        print("1")
        genre3=my_text.check_genre(setsumei)
        
        genre2=split_words.split_mecab_a(title, setsumei)
        x=0
        secure_id = str(uuid.uuid4().hex[:5])
    
        user_name_uuid = str(username + '-' + uuid1)
        print("2")
        for file in upfile:
            print("3")
            x+=1
            secure_id = str(uuid.uuid4().hex[:5])
            filename = secure_id+'-'+file.filename
            
            file_id=username+'-'+secure_id

            photo_id = code_data.ins(
                icon=icon,name=name,file_id=file_id, filename=filename, user_name_uuid=user_name_uuid, title=title, setsumei=setsumei, tag=tag, username=username, genre2=genre2,genre3=genre3,folder=foldername, file=file, album_id=album_id)
            if photo_id == 0:
                return msg('アップロード失敗')
        print("4")
        code_data.add_album_count(
                album_count=x,album_id=album_id)
        print("5")
        return redirect('/up/'+username)
    

# 画像コンテンツの詳細画面
@ app.route('/<user_name>/content/<album_id>/<file_id>')
def content(user_name,file_id, album_id):
    me = user_login.get_id()

    mode='follow'
    do_follow=follow_data.follow_q(me)
    if not do_follow:
        mode='unfollow'

    s=0
    pv=0
    #画像のデータを取り出し
    content_data = photo_data.content(album_id)
    #投稿についたコメントを取り出し
    comment_data = photo_data.comment(album_id)
    #投稿者情報を取り出し
    profile_data= fs_data.user_data(user_name)

    for d in profile_data:
        icon = d["icon"]
        name = d["name"]
        to_user_name = d["user_name"]

    for i in content_data:
        if s==0:
            file = i["file"]
            folder = i['folder']
            album_count=int(i["album_count"])
            pv=int(i["pv"])
            s+=1
    pv+=1

    photo_data.pv_count(file_id,pv)

    if me == user_name:
        return render_template('image_content.html',contents_kinds="image", mode="private", user_name=me, name=name, contents_user=user_name, file=file, folder=folder, icon=icon, album_count=album_count, data=content_data, comment=comment_data, file_id=file_id, album_id=album_id)

    return render_template('image_content.html',contents_kinds="image",mode=mode, user_name=me, to_user_name=to_user_name, contents_user=user_name, file=file, folder=folder, icon=icon, album_count=album_count, data=content_data, comment=comment_data, file_id=file_id, album_id=album_id)



# 動画コンテンツの詳細画面
@ app.route('/<user_name>/video_content/<album_id>/<file_id>')
def video_content(user_name,file_id, album_id):
    me = user_login.get_id()

    mode='follow'
    do_follow=follow_data.follow_q(me)
    if not do_follow:
        mode='unfollow'

    s=0
    pv=0
    #画像のデータを取り出し
    content_data = video_data.content(album_id)
    #投稿についたコメントを取り出し
    comment_data = video_data.comment(album_id)
    #投稿者情報を取り出し
    profile_data= fs_data.user_data(user_name)

    for d in profile_data:
        icon = d["icon"]
        name = d["name"]
        to_user_name = d["user_name"]

    for i in content_data:
        if s==0:
            file = i["file"]
            folder = i['folder']
            album_count=int(i["album_count"])
            pv=int(i["pv"])
            s+=1
    pv+=1

    video_data.pv_count(file_id,pv)

    if me == user_name:
        return render_template('video_content.html',mode="private", user_name=me, name=name, contents_user=user_name, file=file, folder=folder, icon=icon, album_count=album_count, data=content_data, comment=comment_data, file_id=file_id, album_id=album_id)

    return render_template('video_content.html',mode=mode, user_name=me, to_user_name=to_user_name, contents_user=user_name, file=file, folder=folder, icon=icon, album_count=album_count, data=content_data, comment=comment_data, file_id=file_id, album_id=album_id)

# コードコンテンツの詳細画面
@app.route('/<user_name>/code_content/<album_id>/<file_id>')
def code_content(user_name,file_id, album_id):
    me = user_login.get_id()

    mode='follow'
    do_follow=follow_data.follow_q(me)
    if not do_follow:
        mode='unfollow'
    
    inside_text_list=[]

    pv=0
    #コードのデータを取り出し
    content_data = code_data.content(album_id)
    #投稿についたコメントを取り出し
    comment_data = code_data.comment(album_id)
    #投稿者情報を取り出し
    profile_data= fs_data.user_data(user_name)

    #アップロードしたユーザーの情報
    for d in profile_data:
        icon = d["icon"]
        name = d["name"]
        to_user_name = d["user_name"]

    #コードファイルの中身
    for i in content_data:
        file = i["file"]
        folder = i['folder']
        album_count=int(i["album_count"])
        pv=int(i["pv"])
        #folderの最初の「/」があると上手く表示されないので消す
        file_path=str(folder[1:] + "/" + file)

        #コードファイルの中身を表示するためにファイルを開く
        with open(file_path, "r") as f:
            inside_text = f.read()
        #リストにコードの内容を追加
        inside_text_list.append(inside_text)

    #PV情報の追加
    pv+=1
    code_data.pv_count(file_id,pv)

    if me == user_name:
        return render_template('code_content.html',mode="private", user_name=me, name=name, contents_user=user_name, file=file, folder=folder, icon=icon, album_count=album_count, data=content_data, comment=comment_data, file_id=file_id, album_id=album_id, inside_text_list=inside_text_list)

    return render_template('code_content.html',mode=mode, user_name=me, to_user_name=to_user_name, contents_user=user_name, file=file, folder=folder, icon=icon, album_count=album_count, data=content_data, comment=comment_data, file_id=file_id, album_id=album_id, inside_text_list=inside_text_list)


# コメントを投稿
@app.route('/post-comment/<album_id>/<file_id>', methods=['POST'])
@user_login.login_required
def comment(album_id,file_id):
    # セッションからユーザー情報を取得
    user_name = user_login.get_id()

    user_data = fs_data.user_data(user_name)
    for i in user_data:
        icon = i["icon"]


    comment = request.form.get('comment','')

    ng_list=["*****","*****","*****"]

    for i in ng_list:
        if i in comment:
            return msg('アップロード失敗')

    photo_data.post_comment(
        icon=icon,comment=comment, user_name=user_name, album_id=album_id)
    return redirect('/'+user_name+'/content/'+album_id+'/'+file_id)


# パスワードを忘れた場合
@ app.route('/forgot')
def forgot():
    return render_template('index.html')

#　一般ユーザーから見えるプロフィール画面
@ app.route('/photos/<user_name>')
def photos(user_name):
    mode='follow'
    me = user_login.get_id()
    do_follow=follow_data.follow_q(me)
    if not do_follow:
        mode='unfollow'

    ok=fs_data.user_name_existence(user_name)
    if not ok:
        return msg('ユーザーが存在しません')
    
    image_data = photo_data.select_all_data(user_name)
    profile_data = fs_data.user_data(user_name)

    for d in profile_data:
        folder = '/'+d['folder']
        background = d['background']
        icon = d["icon"]
        name=d["name"]
        about=d["about"]
        follower=str(d["follower"])
        following=str(d["following"])
        contents=str(d["contents"])

    #ログイン済みのユーザーの時
    if me != None:
        return render_template('user_all_login.html',mode=mode,user_name=user_name,name=name,about=about,image_data=image_data,icon=icon,background=background,folder=folder,follower=follower,following=following,contents=contents)
    return render_template('user_all.html',mode=mode,user_name=user_name,name=name,about=about,image_data=image_data,icon=icon,background=background,folder=folder,follower=follower,following=following,contents=contents)


#　アカウントの所有者が見える画面
@ app.route('/user-photos/<user_name>')
@user_login.login_required
def user(user_name):
    me = user_login.get_id()

    if me != user_name:
        return redirect('/login_form')

    existence=fs_data.user_name_existence(user_name)

    if not existence:
        return msg('ユーザーが存在しません')

    image_data = photo_data.select_all_data(user_name)
    video_dataset=video_data.select_user_data(user_name)
    audio_dataset=audio_data.select_user_data(user_name)
    code_dataset=code_data.select_user_data(user_name)

    profile_data = fs_data.user_data(user_name)

    for d in profile_data:
        folder = '/'+d["folder"]
        background = d["background"]
        icon = d["icon"]
        name=d["name"]
        about=d["about"]
        follower=str(d["follower"])
        following=str(d["following"])
        contents=str(d["contents"])

    return render_template('user.html',user_name=user_name,name=name,about=about,image_data=image_data,video_dataset=video_dataset,audio_dataset=audio_dataset,code_dataset=code_dataset,icon=icon,background=background,folder=folder,follower=follower,following=following,contents=contents)

#プロフィールを変更するためのページ
@ app.route('/edit_user/<user_name>')
@user_login.login_required
def edit(user_name):
    me = user_login.get_id()
    if me != user_name:
        return render_template('login_form.html')

    ok=fs_data.user_name_existence(user_name)

    if not ok:
        return 'ユーザーが存在しません'

    user_photo = photo_data.select_all_data(user_name)

    user_data = fs_data.user_data(user_name)

    for i in user_data:
            name=i["name"]
            about=i["about"]
            icon = i["icon"]
            folder = '/'+i['folder']
            background = i['background']

    return render_template('edit_user.html',name=name,about=about,user_name=user_name,data=user_photo,icon=icon,folder=folder,background=background)


#個人設定を変更
@ app.route('/change_edit_user/<user_name>', methods=['POST'])
@user_login.login_required
def change_edit(user_name):
    me = user_login.get_id()

    if me != user_name:
        return render_template('login_form.html')

    ok=fs_data.user_name_existence(user_name)

    if not ok:
        return 'ユーザーが存在しません'

    user_data = fs_data.user_data(user_name)

    for i in user_data:
            folder = '/'+i['folder']
            uid = i['uuid']

    icon_file = request.files.get('icon', None)
    background_file = request.files.get('background', None)

    name = request.form.get('name', '')
    about = request.form.get('about', '')

    frofile=fs_data.profile_change(user_name=user_name,uid=uid,folder=folder,icon_file=icon_file,background_file=background_file,about=about,name=name)

    if frofile == 0:
        return msg('アップロード失敗')

    return redirect('/user-photos/'+user_name)

#コンテンツの削除機能
@ app.route('/contents_remove/<user_name>/<album_id>', methods=['POST'])
@user_login.login_required
def contents_remove(user_name,album_id):
    me = user_login.get_id()
    #ログインしているか確認
    if me != user_name:
        return render_template('login_form.html')
    #データベースからデータを削除
    photo_data.remove_album_id(album_id)

    return redirect('/user-photos/'+user_name)

#フォロー機能
@ app.route('/follow/<user_name>', methods=['POST'])
@user_login.login_required
def follow(user_name):
    me = user_login.get_id()
    follow_data.follow(me=me,from_user_name=me, to_user_name=user_name)
    return redirect('/photos/'+user_name)

# お問い合わせフォーム
@app.route('/contact_form')
def contact_form():
    return render_template('contact_form.html')

# お問い合わせフォームの送信
@app.route('/contact_post', methods=['POST'])
def contact_post():
    name = request.form.get('name', '')
    email_Address = request.form.get('email', '')
    message = request.form.get('message', '')

    if name==None or email_Address==None or message==None:
        return msg('正しく入力してください')

    ng_list=["FX","副業","信じる心","bitcoin"]

    for i in ng_list:
        if i in message:
            return msg('アップロード失敗')

    subject = name+'のメッセージ'
    bodyText = email_Address+'からのメッセージ'+message
    toAddress = 'cia13267koi@gmail.com'
    fromAddress='youzitsurist@gmail.com'

    # SMTPサーバに接続
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.starttls()
    smtpobj.login(sendAddress, password)

    # メール作成
    msg = MIMEText(bodyText)
    msg['Subject'] = subject
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Date'] = formatdate()

    # 作成したメールを送信
    smtpobj.send_message(msg)
    smtpobj.close()

    return 0

# テンプレートを使ってエラー画面を表示
def msg(s):
    return render_template('message.html', msg=s)

@ app.errorhandler(404)
def page_not_found(error):
    return msg('ページが見つかりません')

# --- テンプレートのフィルタなど拡張機能の指定
# CSSなど静的ファイルの後ろにバージョンを自動追記(キャッシュされて変更されない時のため)
@ app.context_processor
def add_staticfile():
    return dict(staticfile=staticfile_cp)

def staticfile_cp(fname):
    path = os.path.join(app.root_path, 'static', fname)
    mtime = str(int(os.stat(path).st_mtime))
    return '/static/' + fname + '?v=' + str(mtime)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001, ssl_context=('server.crt', 'server.key'))
