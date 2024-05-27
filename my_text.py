import pickle, tfidf
import numpy as np

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
from keras.models import model_from_json

from keras.models import load_model
# 独自のテキストを指定 --- (*1)

text1 = """
野球を観るのは楽しいものです。
試合だけでなくインタビューも楽しみです。
"""
text2 = """
常にiPhoneとiPadを持っているので、
二口あるモバイルバッテリがあると便利。
"""
text3 = """
幸せな結婚の秘訣は何でしょうか。
夫には敬意を、妻には愛情を示すことが大切。
"""

# TF-IDFの辞書を読み込む --- (*2)
tfidf.load_dic("static/genre-tdidf.dic")

model = load_model('./static/model.h5')


# テキストを指定して判定 --- (*4)
def check_genre(text):
    # ラベルの定義
    LABELS = ["スポーツ", "IT", "映画", "ライフ"]
    # TF-IDFのベクトルに変換 -- (*5)
    data = tfidf.calc_text(text)
    # MLPで予測 --- (*6)
    pre = model.predict(np.array([data]))[0]
    n = pre.argmax()
    print(LABELS[n], "(", pre[n], ")")
    return LABELS[n]

