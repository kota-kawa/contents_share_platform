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


# ユーザーのすべての画像を表示
def select_all_data(user_name):
    cursor.execute(
        " SELECT * FROM photo WHERE user_name = %s ORDER BY suji DESC", (user_name,))
    result = cursor.fetchall()

    return result


# 検索結果の画像を表示
def search(kensaku):
    cursor.execute(
        " SELECT  title,ex_plain,folder,time,file,user_name,file_id,album_id FROM photo WHERE title LIKE %s OR ex_plain LIKE %s ORDER BY suji DESC", ('%'+kensaku+'%', '%'+kensaku+'%'))
    result = cursor.fetchall()

    return result


# 画像を投稿
def ins(file_id, filename, user_name_uuid, title, setsumei, tag, username, folder,genre2,genre3, file,album_id):
    path = str(user_name_uuid)

    album_id=album_id

    file.save(STATIC + '/'+path + '/'+filename)
    cursor.execute(
        "INSERT INTO photo (time,title,ex_plain,tag,user_name,folder,file,genre2,genre3,file_id,album_id) VALUES (NOW(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (title, setsumei, tag, username, folder, filename,genre2,genre3, file_id,album_id))
    cursor.execute(
        "UPDATE id SET contents = contents + 1 WHERE user_name = %s", (username,))
    # 保存を実行
    connection.commit()


#　アルバムIDから画像の枚数を保存
def add_album_count(album_count,album_id):

    cursor.execute(
        " UPDATE photo SET album_count = %s WHERE album_id = %s ",(album_count,album_id))

    # 保存を実行
    connection.commit()

    
#　ファイルIDから顔があるかの画像のジャンルを追加
def genre1(face,file_id):

    cursor.execute(
        " UPDATE photo SET genre1 = %s WHERE file_id = %s ",(face,file_id))

    # 保存を実行
    connection.commit()



# アルバムIDをもとにデータを抽出
def content(album_id):
    cursor.execute(
        " SELECT  title,ex_plain,folder,time,file,album_count,pv FROM photo WHERE album_id = %s", (album_id,))
    result = cursor.fetchall()

    return result


# アルバムIDをもとにデータを削除
def remove_album_id(album_id):

    cursor.execute(
        " SELECT  user_name,folder,file FROM photo WHERE album_id = %s", (album_id,))
    result = cursor.fetchall()
    for i in result:
        folder=i["folder"]
        file=i["file"]
        username=i["user_name"]
        path=str(folder[1:] +'/'+ file)
        os.remove(path)
        cursor.execute("DELETE FROM photo WHERE album_id = %s", (album_id,))
        cursor.execute(
        "UPDATE id SET contents = contents - 1 WHERE user_name = %s", (username,))
        # 保存を実行
    connection.commit()

# PVの追加
def pv_count(file_id,pv):
    cursor.execute(
        "UPDATE photo SET pv = %s WHERE file_id = %s", (pv,file_id))
    # 保存を実行
    connection.commit()

# ファイルIDをもとにそれについたコメントを抽出(新しい順)
def comment(album_id):
    cursor.execute(
        " SELECT * FROM comment WHERE album_id = %s ORDER BY suji DESC" , (album_id,))
    result = cursor.fetchall()

    return result

# コメントを投稿
def post_comment(icon,comment, user_name, album_id):
    cursor.execute(
        "INSERT INTO comment (time,icon,comment,user_name,album_id) VALUES (NOW(),%s,%s,%s,%s)", (icon,comment, user_name, album_id))
    # 保存を実行
    connection.commit()