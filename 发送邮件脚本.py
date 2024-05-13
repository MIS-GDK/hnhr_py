import email.mime.multipart
import email.mime.text
import smtplib

# server = "smtp.qq.com"  # 邮箱服务器
# port = "25"  # 邮箱服务器端口
server = "smtp.aliyun.com"  # 邮箱服务器
port = 25


def sendmail(server, port, user, pwd, msg):
    smtp = smtplib.SMTP()
    smtp.connect(server, port)
    smtp.login(user, pwd)
    smtp.sendmail(msg["from"], msg["to"], msg.as_string())
    smtp.quit()
    print("邮件发送成功email has send out !")


if __name__ == "__main__":
    msg = email.mime.multipart.MIMEMultipart()
    msg["Subject"] = "系统监控告警邮件"  # 邮件标题
    # msg["From"] = "1530951440@qq.com"  # 发送方的邮箱地址
    # msg["To"] = "1530951440@qq.com"  # 目的邮箱地址
    # user = "1530951440@qq.com"  # 登陆的用户
    # pwd = "wjhatwyljohqgfia"  # 授权码
    msg["From"] = "dangxiayehenyouyu@aliyun.com"  # 发送方的邮箱地址
    msg["To"] = "1530951440@qq.com"  # 目的邮箱地址
    user = "dangxiayehenyouyu@aliyun.com"  # 登陆的用户
    pwd = "414214Gdk.."  # 授权码
    content = "%s\n%s" % (
        "".join("ogg预警\n"),
        "".join("ogg出现问题了"),
    )  # 格式处理，专门针对我们的邮件格式
    txt = email.mime.text.MIMEText(content, _charset="utf-8")
    msg.attach(txt)
    sendmail(server, port, user, pwd, msg)
