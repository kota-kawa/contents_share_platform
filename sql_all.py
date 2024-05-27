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


# ユーザープロフィールテーブルの初期化
cursor.execute("DROP TABLE IF EXISTS id")

# テーブルの作成
cursor.execute("""CREATE TABLE id(
  suji INT(11) AUTO_INCREMENT NOT NULL,
  time DATETIME ,
  name VARCHAR(30),
  user_name VARCHAR(30),
  mail_address VARCHAR(300),
  phone_address VARCHAR(30),
  password VARCHAR(300),
  folder VARCHAR(300),
  icon VARCHAR(300) DEFAULT "/static/tsubaki.jpeg",
  background VARCHAR(300) DEFAULT "/static/onsitsu.jpeg",
  follower INT DEFAULT 0,
  following INT DEFAULT 0,
  contents INT DEFAULT 0,
  about VARCHAR(300),
  uuid VARCHAR(300),
  kari_mail VARCHAR(300),
  kari_pass VARCHAR(300),
  unique_id VARCHAR(300),
  PRIMARY KEY (suji)
 )""")


# コメントテーブルの初期化
cursor.execute("DROP TABLE IF EXISTS comment")

# テーブルの作成
cursor.execute("""CREATE TABLE comment(
  suji INT(11) AUTO_INCREMENT NOT NULL,
  time DATETIME ,
  user_name VARCHAR(30),
  mail_address VARCHAR(30),
  icon VARCHAR(200),
  comment VARCHAR(500),
  file_id VARCHAR(300),
  album_id VARCHAR(100),
  PRIMARY KEY (suji)
 )""")

# フォローテーブルの初期化
cursor.execute("DROP TABLE IF EXISTS follow")

# テーブルの作成
cursor.execute("""CREATE TABLE follow(
  suji INT(11) AUTO_INCREMENT NOT NULL,
  time DATETIME ,
  from_user_name VARCHAR(30),
  to_user_name VARCHAR(30),
  PRIMARY KEY (suji)
 )""")

# 写真テーブルの初期化
cursor.execute("DROP TABLE IF EXISTS photo")

# テーブルの作成
cursor.execute("""CREATE TABLE photo(
  suji INT(11) AUTO_INCREMENT NOT NULL,
  time DATETIME ,
  user_name VARCHAR(30),
  mail_address VARCHAR(30),
  title VARCHAR(30),
  ex_plain VARCHAR(300),
  comment VARCHAR(500),
  folder VARCHAR(300),
  file VARCHAR(300),
  genre1 VARCHAR(300),
  genre2 VARCHAR(300),
  genre3 VARCHAR(300),
  file_id VARCHAR(300),
  album_id VARCHAR(100),
  album_count VARCHAR(10),
  tag VARCHAR(300),
  pv INT DEFAULT 0,
  PRIMARY KEY (suji)
 )""")

# 動画テーブルの初期化
cursor.execute("DROP TABLE IF EXISTS video")

# テーブルの作成
cursor.execute("""CREATE TABLE video(
  suji INT(11) AUTO_INCREMENT NOT NULL,
  time DATETIME ,
  user_name VARCHAR(30),
  mail_address VARCHAR(30),
  title VARCHAR(30),
  ex_plain VARCHAR(300),
  comment VARCHAR(500),
  folder VARCHAR(300),
  file VARCHAR(300),
  genre2 VARCHAR(300),
  genre3 VARCHAR(300),
  file_id VARCHAR(300),
  album_id VARCHAR(100),
  album_count VARCHAR(10),
  tag VARCHAR(300),
  pv INT DEFAULT 0,
  PRIMARY KEY (suji)
 )""")

# オーディオテーブルの初期化
cursor.execute("DROP TABLE IF EXISTS audio")

# テーブルの作成
cursor.execute("""CREATE TABLE audio(
  suji INT(11) AUTO_INCREMENT NOT NULL,
  time DATETIME ,
  user_name VARCHAR(30),
  mail_address VARCHAR(30),
  title VARCHAR(30),
  ex_plain VARCHAR(300),
  comment VARCHAR(500),
  folder VARCHAR(300),
  file VARCHAR(300),
  audio_img VARCHAR(300),
  genre2 VARCHAR(300),
  genre3 VARCHAR(300),
  file_id VARCHAR(300),
  album_id VARCHAR(100),
  album_count VARCHAR(10),
  tag VARCHAR(300),
  pv INT DEFAULT 0,
  PRIMARY KEY (suji)
 )""")

# オーディオテーブルの初期化
cursor.execute("DROP TABLE IF EXISTS code")

# テーブルの作成
cursor.execute("""CREATE TABLE code(
  suji INT(11) AUTO_INCREMENT NOT NULL,
  time DATETIME ,
  user_name VARCHAR(30),
  name VARCHAR(30),
  icon VARCHAR(300),
  mail_address VARCHAR(30),
  language  VARCHAR(30),
  logo  VARCHAR(30),
  title VARCHAR(30),
  ex_plain VARCHAR(300),
  comment VARCHAR(500),
  folder VARCHAR(300),
  file VARCHAR(300),
  genre2 VARCHAR(300),
  genre3 VARCHAR(300),
  file_id VARCHAR(300),
  album_id VARCHAR(100),
  album_count VARCHAR(10),
  tag VARCHAR(300),
  pv INT DEFAULT 0,
  PRIMARY KEY (suji)
 )""")

# 保存を実行
connection.commit()

# 接続を閉じる
connection.close()
