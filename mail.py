import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
charset = "iso-2022-jp"

""" メール本文情報（要編集）"""
To = "*****"
Subject = "件名を入力"
MailBody = "本文を入力"
    
#SMTPサーバー接続・ログイン情報
my_mail = "*****"
app_password = "*****"
smtp = smtplib.SMTP("smtp.gmail.com",587)
    

From = my_mail
Atesaki = To
Kenmei = Subject
Body = MailBody
    
#メール本文を読込
msg = MIMEMultipart()
msg.attach(MIMEText(Body))
msg["Subject"] = Header(Kenmei.encode(charset),charset)


#サーバー・ポート接続
smtp.ehlo()
#TLS暗号化
smtp.starttls()
#SMTPサーバーログイン
smtp.login(my_mail,app_password)
#メール送信
smtp.sendmail(From,Atesaki,msg.as_string())
#SMTPサーバー遮断
smtp.quit()
    
print("メールを送信しました。")

