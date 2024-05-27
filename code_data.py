# MySQLdbのインポート
import MySQLdb
import os
from werkzeug.utils import secure_filename

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

# すべてのコードを新しい順に表示
def select_all_data():
    cursor.execute(
        " SELECT * FROM code ORDER BY suji DESC")
    result = cursor.fetchall()
    print(result)

    return result

# ユーザー名をもとにコードを表示
def select_user_data(user_name):
    cursor.execute(
        " SELECT * FROM code WHERE user_name = %s ORDER BY suji DESC", (user_name,))
    result = cursor.fetchall()

    return result

# コードを投稿
def ins(icon, name, file_id, filename, user_name_uuid, title, setsumei, tag, username, genre2,genre3,folder, file, album_id):
    path = str(user_name_uuid)

    #　ファイル名から拡張子を得る
    file_kinds = secure_filename(file.filename)
    language = file_kinds.rsplit('.', 1)[1].lower()  # ファイル名から拡張子を取得

    if language == "py":
        logo="static/img/python.png"
    elif language == "c":
        logo="static/img/c.png"
    elif language == "cpp":
        logo="static/img/c-plus-plus.png"
    elif language == "cs":
        logo="static/img/c-sharp.png"
    elif language == "java":
        logo="static/img/java.png"
    elif language == "js":
        logo="static/img/javascript.png"
    elif language == "pl":
        logo="static/img/perl.png"
    elif language == "php":
        logo="static/img/php.png"
    elif language == "r":
        logo="static/img/r.png"
    elif language == "rb":
        logo="static/img/ruby.png"
    elif language == "ts":
        logo="static/img/typescript.png"
    elif language == "swift":
        logo="static/img/swift.png"
    elif language == "kt":
        logo="static/img/kotlin.png"

    elif language == "docx" or language == "doc":
        logo="static/img/word.png"
    elif language == "xlsx" or language == "dxls":
        logo="static/img/excel.png"
    elif language == "ppt":
        logo="static/img/powerpoint.png"

    elif language == "txt":
        logo="static/img/txt.png"

    album_id=album_id

    file.save(STATIC + '/'+path + '/'+filename)
    
    cursor.execute(
        "INSERT INTO code (time,language,logo,title,ex_plain,tag,user_name,folder,file,genre2,genre3,file_id,album_id,icon,name) VALUES (NOW(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (language, logo, title, setsumei, tag, username,folder, filename,genre2,genre3,file_id,album_id,icon,name))
    
    cursor.execute(
        "UPDATE id SET contents = contents + 1 WHERE user_name = %s", (username,))
    # 保存を実行
    connection.commit()

#　アルバムIDからコードファイルの数を保存
def add_album_count(album_count,album_id):
    cursor.execute(
        " UPDATE code SET album_count = %s WHERE album_id = %s ",(album_count,album_id))
    # 保存を実行
    connection.commit()


# アルバムIDをもとにデータを抽出
def content(album_id):
    cursor.execute(
        " SELECT  title,ex_plain,folder,time,file,album_count,pv FROM code WHERE album_id = %s", (album_id,))
    result = cursor.fetchall()

    return result


# アルバムIDをもとにデータを削除
def remove_album_id(album_id):

    cursor.execute(
        " SELECT user_name,folder,file FROM code WHERE album_id = %s", (album_id,))
    result = cursor.fetchall()
    for i in result:
        folder=i["folder"]
        file=i["file"]
        username=i["user_name"]
        path=str(folder[1:] +'/'+ file)
        os.remove(path)
        cursor.execute("DELETE FROM code WHERE album_id = %s", (album_id,))
        cursor.execute(
        "UPDATE id SET contents = contents - 1 WHERE user_name = %s", (username,))
        # 保存を実行
    connection.commit()

# PVの追加
def pv_count(file_id,pv):
    cursor.execute(
        "UPDATE code SET pv = %s WHERE file_id = %s", (pv,file_id))
    # 保存を実行
    connection.commit()

# ファイルIDをもとにそれについたコメントを抽出(新しい順)
def comment(album_id):
    cursor.execute(
        " SELECT * FROM comment WHERE album_id = %s ORDER BY suji DESC" , (album_id,))
    result = cursor.fetchall()

    return result

