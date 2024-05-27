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

# すべての動画を新しい順に表示
def select_all_data():
    cursor.execute(
        " SELECT * FROM video ORDER BY suji DESC")
    result = cursor.fetchall()

    return result

# ユーザー名をもとに動画を表示
def select_user_data(user_name):
    cursor.execute(
        " SELECT * FROM video WHERE user_name = %s ORDER BY suji DESC", (user_name,))
    result = cursor.fetchall()

    return result

# 動画を投稿
def ins(file_id, filename, user_name_uuid, title, setsumei, tag, username, folder,genre2,genre3, file,album_id):
    path = str(user_name_uuid)

    album_id=album_id

    file.save(STATIC + '/'+path + '/'+filename)
    cursor.execute(
        "INSERT INTO video (time,title,ex_plain,tag,user_name,folder,file,genre2,genre3,file_id,album_id) VALUES (NOW(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (title, setsumei, tag, username, folder, filename,genre2,genre3, file_id,album_id))
    cursor.execute(
        "UPDATE id SET contents = contents + 1 WHERE user_name = %s", (username,))
    # 保存を実行
    connection.commit()

#　アルバムIDから画像の枚数を保存
def add_album_count(album_count,album_id):

    cursor.execute(
        " UPDATE video SET album_count = %s WHERE album_id = %s ",(album_count,album_id))

    # 保存を実行
    connection.commit()

# アルバムIDをもとにデータを削除
def remove_album_id(album_id):

    cursor.execute(
        " SELECT  user_name,folder,file FROM video WHERE album_id = %s", (album_id,))
    result = cursor.fetchall()
    for i in result:
        folder=i["folder"]
        file=i["file"]
        username=i["user_name"]
        #/staticではなくstaticだけ
        path=str(folder[1:] +'/'+ file)
        os.remove(path)
        cursor.execute("DELETE FROM video WHERE album_id = %s", (album_id,))
        cursor.execute(
        "UPDATE id SET contents = contents - 1 WHERE user_name = %s", (username,))
        # 保存を実行
    connection.commit()

# PVの追加
def pv_count(file_id,pv):
    cursor.execute(
        "UPDATE video SET pv = %s WHERE file_id = %s", (pv,file_id))
    # 保存を実行
    connection.commit()

# ファイルIDをもとにそれについたコメントを抽出(新しい順)
def comment(album_id):
    cursor.execute(
        " SELECT * FROM comment WHERE album_id = %s ORDER BY suji DESC" , (album_id,))
    result = cursor.fetchall()

    return result


# アルバムIDをもとにデータを抽出
def content(album_id):
    cursor.execute(
        " SELECT * FROM video WHERE album_id = %s", (album_id,))
    result = cursor.fetchall()

    return result
