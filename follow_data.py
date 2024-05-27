# MySQLdbのインポート
import MySQLdb

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

#　フォーロー・フォロー解除機能
def follow(me, from_user_name, to_user_name):
    i = None
#フォローしているか確認
    cursor.execute(
        " SELECT * FROM follow WHERE from_user_name = %s ", (me,))
    result = cursor.fetchall()

    for i in result:
        i = i
#　フォローしてない時
    if i is None:
        cursor.execute(
        "INSERT INTO follow (time,from_user_name, to_user_name) VALUES (NOW(),%s,%s)", (from_user_name, to_user_name))
        cursor.execute(
        "UPDATE id SET following = following + 1 WHERE user_name = %s", (from_user_name,))
        cursor.execute(
        "UPDATE id SET follower = follower + 1 WHERE user_name = %s", (to_user_name,))

        # 保存を実行
        connection.commit()
#　フォローしていた時
    else:
        cursor.execute(
        "DELETE FROM follow WHERE from_user_name = %s AND to_user_name = %s", (from_user_name, to_user_name))
        cursor.execute(
        "UPDATE id SET following = following - 1 WHERE user_name = %s", (from_user_name,))
        cursor.execute(
        "UPDATE id SET follower = follower - 1 WHERE user_name = %s", (to_user_name,))
    # 保存を実行
    connection.commit()

#　セッションからユーザーをフォローしているのかを確認
def follow_q(me):
    i = None

    cursor.execute(
        " SELECT * FROM follow WHERE from_user_name = %s ", (me,))
    result = cursor.fetchall()

    for i in result:
        i = i

    if i is None:
        return False

    return True
