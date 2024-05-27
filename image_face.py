import cv2
import os

BASE_DIR = os.path.dirname(__file__)

# カスケードファイルを指定して検出器を作成 --- (*1)
cascade_file = BASE_DIR+"/static/haarcascade_frontalface_alt.xml"
cascade = cv2.CascadeClassifier(cascade_file)

def check(file):
    print(file)
    path=BASE_DIR+file
    # 画像の読み込んでグレイスケールに変換する --- (*2)
    img = cv2.imread(path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 顔認識を実行 --- (*3)
    face_list = cascade.detectMultiScale(img_gray, minSize=(150,150))
    # 結果を確認 --- (*4)
    if len(face_list) == 0:
        return False
    # 認識した部分に印をつける --- (*5)
    for (x,y,w,h) in face_list: 
        return '顔'




