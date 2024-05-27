# MySQLdbのインポート
import MySQLdb
import os

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


# すべての音源を新しい順に表示
def select_all_data():
    cursor.execute(
        " SELECT * FROM audio ORDER BY suji DESC")
    result = cursor.fetchall()

    return result

# ユーザー名をもとに音源を表示
def select_user_data(user_name):
    cursor.execute(
        " SELECT * FROM audio WHERE user_name = %s ORDER BY suji DESC", (user_name,))
    result = cursor.fetchall()

    return result

# オーディオを投稿
def ins(file_id, filename, user_name_uuid, title, setsumei, tag, username, genre2,genre3,folder, file, audio_img_name, album_id):
    path = str(user_name_uuid)

    album_id=album_id

    file.save(STATIC + '/'+path + '/'+filename)
    
    cursor.execute(
        "INSERT INTO audio (time,title,ex_plain,tag,user_name,folder,file,genre2,genre3,file_id,album_id,audio_img) VALUES (NOW(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (title, setsumei, tag, username,folder, filename,genre2,genre3,file_id,album_id,audio_img_name))
    
    cursor.execute(
        "UPDATE id SET contents = contents + 1 WHERE user_name = %s", (username,))
    # 保存を実行
    connection.commit()

#　アルバムIDから画像の枚数を保存
def add_album_count(album_count,album_id):
    cursor.execute(
        " UPDATE audio SET album_count = %s WHERE album_id = %s ",(album_count,album_id))
    # 保存を実行
    connection.commit()


# アルバムIDをもとにデータを抽出
def content(album_id):
    cursor.execute(
        " SELECT  title,ex_plain,folder,time,file,audio_img,album_count,pv FROM audio WHERE album_id = %s", (album_id,))
    result = cursor.fetchall()

    return result


# アルバムIDをもとにデータを削除
def remove_album_id(album_id):

    cursor.execute(
        " SELECT  user_name,folder,file FROM audio WHERE album_id = %s", (album_id,))
    result = cursor.fetchall()
    for i in result:
        folder=i["folder"]
        file=i["file"]
        username=i["user_name"]
        #/staticではなくstaticだけ
        path=str(folder[1:] +'/'+ file)
        os.remove(path)
        cursor.execute("DELETE FROM audio WHERE album_id = %s", (album_id,))
        cursor.execute(
        "UPDATE id SET contents = contents - 1 WHERE user_name = %s", (username,))
        # 保存を実行
    connection.commit()

# PVの追加
def pv_count(file_id,pv):
    cursor.execute(
        "UPDATE audio SET pv = %s WHERE file_id = %s", (pv,file_id))
    # 保存を実行
    connection.commit()

# ファイルIDをもとにそれについたコメントを抽出(新しい順)
def comment(album_id):
    cursor.execute(
        " SELECT * FROM comment WHERE album_id = %s ORDER BY suji DESC" , (album_id,))
    result = cursor.fetchall()

    return result

