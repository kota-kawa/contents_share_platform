# MySQLdbのインポート
import MySQLdb
import os
import uuid
from werkzeug.security import generate_password_hash
BASE_DIR = os.path.dirname(__file__)
STATIC = BASE_DIR+'/static/upload'

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

#１日以上仮登録だった場合
def remove_data():
    cursor.execute(
        "DELETE FROM id WHERE mail_address IS NULL AND time< DATE_SUB(now(), INTERVAL 1 DAY)")
    # 保存を実行
    connection.commit()


# 画像を投稿
def save_file(id, folder, filena):
    name = id
    fold = folder
    files = filena
    cursor.execute(
        "INSERT INTO id (time,mail_address,folder,file) VALUES (NOW(),%s,%s,%s)", (name, fold, files))
    # 保存を実行
    connection.commit()


# すべての画像を新しい順に表示
def select_all_data():
    cursor.execute(
        " SELECT * FROM photo ORDER BY suji DESC")
    result = cursor.fetchall()

    return result

#　ユーザー名のアカウントが存在するか確認
def account_existence(user_name):
    cursor.execute(
        " SELECT user_name FROM id WHERE user_name = %s ", (user_name,))
    
    result = cursor.fetchone()
    print(result)
    if result is None:
        return None

    return True


#　認証用のURLの使用を一度だけにする
def account_existence(kari_mail,user_name):
    cursor.execute(
        " SELECT user_name FROM id WHERE  mail_address = %s AND user_name = %s", (kari_mail,user_name))
    result = cursor.fetchone()
    if result is None:
        return True
    return "error"
    
#　ユーザー名が存在するか確認
def user_name_existence(user_name):
    cursor.execute(
        " SELECT * FROM id WHERE user_name = %s", (user_name,))
    result = cursor.fetchone()
    if result is None:
        return False
    return True

    

#プロフィールの変更
def profile_change(user_name,uid,folder,icon_file, background_file,about, name):
    secure_id = str(uuid.uuid4().hex[:5])
    path = str(uid)

    icon_name = secure_id + '-' + icon_file.filename
    background_name = secure_id + '-' + background_file.filename

    icon=folder + "/"+ icon_name
    background=folder + "/" + background_name

    icon_len=len(icon_name)

    background_len=len(background_name)

#ユーザー名だけ変更
    if icon_len < 7 and background_len < 7:
        cursor.execute(
        "UPDATE id SET name = %s, about = %s WHERE user_name = %s", (name,about,user_name))
        connection.commit()
#名前と背景を変更
    elif icon_len < 7:
        background_file.save(STATIC + '/' + user_name +'-' + path + '/' +  background_name)

        cursor.execute(
            "UPDATE id SET name = %s, about = %s,background = %s WHERE user_name = %s", (name,about, background,user_name))
        # 保存を実行
        connection.commit()
#名前とアイコンを変更
    elif background_len < 7:
        icon_file.save(STATIC + '/' + user_name +'-' + path + '/' +  icon_name)

        cursor.execute(
            "UPDATE id SET name = %s, about = %s,icon = %s WHERE user_name = %s", (name,about, icon,user_name))
        # 保存を実行
        connection.commit()
#すべてを変更
    else:
        #ファイルをサーバーに保存
        icon_file.save(STATIC + '/' + user_name +'-' + path + '/' +  icon_name)
        background_file.save(STATIC + '/' + user_name +'-' + path + '/' +  background_name)

        cursor.execute(
            "UPDATE id SET name = %s, about = %s,icon = %s,background = %s WHERE user_name = %s", (name,about, icon, background,user_name))
        # 保存を実行
        connection.commit()

# 仮登録
def kari_toroku(toAddress, login_password, name, username, user_uuid):
    i = None
    password=generate_password_hash(login_password)

#ユーザー名が既に使われているか確認
    cursor.execute(
        " SELECT user_name FROM id WHERE user_name = %s", (username,))
    result = cursor.fetchall()

    for i in result:
        i = i["user_name"]
#ユーザー名が既に使われていない場合
    if i is None:
        cursor.execute(
            " INSERT INTO id  (time,name,user_name,kari_mail,kari_pass,uuid) VALUES (NOW(),%s,%s,%s,%s,%s)", (name, username, toAddress, password, user_uuid))
        # 保存を実行
        connection.commit()
        return True

    return False

# 本登録のためにUUIDからデータを検索
def select_uuid(user_name):
    cursor.execute(
        " SELECT * FROM id WHERE user_name = %s", (user_name,))
    result = cursor.fetchall()

    return result


# ユーザー名からデータを取得
def user_data(user_name):
    cursor.execute(
        " SELECT * FROM id WHERE user_name = %s", (user_name,))
    result = cursor.fetchall()

    return result

# 本登録
def regist_user(mail, pas, foldername, ud):
    address = mail
    word = pas
    uid = ud
    cursor.execute(""" UPDATE id
                        SET mail_address=%s,
                            password=%s,
                            folder=%s
                       WHERE uuid=%s""", (address, word, foldername, uid))
    # 保存を実行
    connection.commit()

