FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    apt-get install -y libglib2.0-0 && \
    apt-get clean

RUN apt-get update && \
    apt-get install -y python3 python3-pip mysql-server default-libmysqlclient-dev libmysqlclient-dev && \
    pip install mysqlclient==2.1.1 && \
    pip3 install flask==2.2.3 && \
    pip install oauthlib==3.2.2 && \
    pip install Flask-SSLify==0.1.5 && \
    pip install opencv-python==4.7.0.72 && \
    pip install numpy==1.23.5 && \
    pip install tensorflow==2.12.0

RUN apt-get update && \
    apt-get install -y mecab libmecab-dev mecab-ipadic-utf8 git make curl xz-utils file && \
    pip3 install unidic-lite && \
    pip3 install mecab-python3==1.0.6

RUN apt-get update && \
    apt-get install -y curl git make xz-utils file sudo && \
    git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git && \
    cd mecab-ipadic-neologd && \
    ./bin/install-mecab-ipadic-neologd -n -y && \
    cd ../ && \
    rm -rf mecab-ipadic-neologd


COPY . /app
WORKDIR /app

RUN service mysql start && \
    sleep 10 && \
    mysql -u root -e "CREATE DATABASE myapp;" && \
    mysql -u root -e "CREATE USER 'user' IDENTIFIED BY 'password';" && \
    mysql -u root -e "GRANT ALL PRIVILEGES ON myapp.* TO 'user';" && \
    mysql -u root -e "FLUSH PRIVILEGES;"

RUN service mysql start



EXPOSE 5001

CMD ["sh", "-c", "python3 sql_all.py && app.py"]

#python3 sql_all.py && 