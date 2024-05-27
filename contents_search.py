# MySQLdbのインポート
import MySQLdb
import my_text

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


def search(kensaku):
    list_all=[]
    user_name_list=[]
    folder_list=[]
    file_list=[]
    file_id_list=[]
    album_id_list=[]

    count=0

    #すべてにヒットした
    cursor.execute(
        " SELECT file_id FROM photo WHERE title LIKE %s AND ex_plain LIKE %s AND tag LIKE %s", ('%'+kensaku+'%', '%'+kensaku+'%', '%'+kensaku+'%'))
    all_fit_data = cursor.fetchall()
    for i in all_fit_data:
        list_all.append(i["file_id"])

    #２つヒットしたとき
    cursor.execute(
        " SELECT file_id FROM photo WHERE title LIKE %s AND ex_plain LIKE %s", ('%'+kensaku+'%', '%'+kensaku+'%'))
    two1_fit_data = cursor.fetchall()
    for i in two1_fit_data:
        list_all.append(i["file_id"])

    cursor.execute(
        " SELECT file_id FROM photo WHERE title LIKE %s AND tag LIKE %s", ('%'+kensaku+'%', '%'+kensaku+'%'))
    two2_fit_data = cursor.fetchall()
    for i in two2_fit_data:
        list_all.append(i["file_id"])

    cursor.execute(
        " SELECT file_id FROM photo WHERE tag LIKE %s AND ex_plain LIKE %s", ('%'+kensaku+'%', '%'+kensaku+'%'))
    two3_fit_data = cursor.fetchall()
    for i in two3_fit_data:
        list_all.append(i["file_id"])
    ##################

    #一つでも一致するものがあれば
    cursor.execute(
        " SELECT file_id FROM photo WHERE title LIKE %s OR ex_plain LIKE %s OR tag LIKE %s", ('%'+kensaku+'%', '%'+kensaku+'%', '%'+kensaku+'%'))
    one_fit_data = cursor.fetchall()
    for i in one_fit_data:
        list_all.append(i["file_id"])

    list_final=list(dict.fromkeys(list_all))

    for i in list_final:
        
        file_id=str(i)

        cursor.execute(
        " SELECT  title,ex_plain,folder,time,file,user_name,file_id,album_id FROM photo WHERE file_id LIKE %s ", ('%'+file_id+'%',))
        result = cursor.fetchall()
        print(result)

        for d in result:
            count+=1
            user_name_list.append(d["user_name"])
            folder_list.append(d["folder"])
            file_list.append(d["file"])
            file_id_list.append(d["file_id"])
            album_id_list.append(d["album_id"])

        
    return count,user_name_list,folder_list,file_list,file_id_list,album_id_list


