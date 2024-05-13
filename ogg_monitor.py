import datetime
import email.mime.multipart
import email.mime.text
import smtplib
import time

import paramiko

hostlist = [
    {
        "host": "192.168.0.43",
        "port": "22",
        "user": "hnoracle",
        "pwd": "5N@bGsfpBX",
        "oggdir": "/u01/app/ogg",
        "orahome": "/u03/app/oracle/product/11.2.0/dbhome_1",
    }
]


def send_mail(server, port, user, pwd, msg):
    smtp = smtplib.SMTP()
    smtp.connect(server, port)
    smtp.login(user, pwd)
    smtp.sendmail(msg["From"], msg["To"].split(","), msg.as_string())
    smtp.quit()
    print("邮件发送成功email has send out !")


def make_mail(send_msg, warn_type):
    # server = "smtp.qq.com"  # 邮箱服务器
    server = "10.8.82.168"
    # port = "25"  # 邮箱服务器
    # server = "smtp.aliyun.com"  # 邮箱服务器
    port = 25
    msg = email.mime.multipart.MIMEMultipart()
    msg["Subject"] = "系统监控告警邮件"  # 邮件标题
    msg["From"] = "gaodakui1@hrhnyy.com.cn"  # 发送方的邮箱地址
    _recer = ["mazhiqiang29@hrhnyy.com.cn", "gaodakui1@hrhnyy.com.cn", "zhanhaichuan1@hrhnyy.com.cn"]
    # _recer = ["1530951440@qq.com"]
    msg["To"] = ",".join(_recer)  # 目的邮箱地址
    # print(msg["To"])
    # print(msg["To"].split(","))

    # user = "1530951440@qq.com"  # 登陆的用户
    # pwd: str = "wjhatwyljohqgfia"  # 授权码
    user = 'gaodakui1@hrhnyy.com.cn'
    pwd = 'iXu5hh8Esn826VK6'
    # content = "%s\n%s" % (
    #     "".join("ogg预警\n"),
    #     "".join("ogg出现问题了,请及时修复"),
    # )
    if warn_type == "主机SSH无法连接":
        content = warn_type + "\n" + send_msg
    else:
        # 格式处理，专门针对我们的邮件格式
        content = warn_type + "\n" + send_msg
    txt = email.mime.text.MIMEText(content, _charset="utf-8")
    msg.attach(txt)
    send_mail(server, port, user, pwd, msg)


def curtime():
    timenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return timenow


class SshOgg:
    def __init__(self, host, port, username, pwd):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.orahome = ""
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.host, self.port, self.username, self.pwd, timeout=5)
            self.sshinvalid = False
            # print(self.sshinvalid)
        except:
            self.sshinvalid = True
            # print(self.sshinvalid)

    def check_ogg_status(self, orahome, oggdir):
        # print(self.sshinvalid)
        if self.sshinvalid:
            send_msg = "**告警时间：** " + curtime() + " \n **告警主机：** " + self.host
            make_mail(send_msg, warn_type="主机SSH无法连接")
        else:
            # 考虑AIX与Linux不同平台library path不同，所以一起设置，防止需要多判断处理不同平台
            cmd = 'export LD_LIBRARY_PATH=%s/lib:%s && echo "info all" |%s/ggsci' % (
                orahome,
                oggdir,
                oggdir,
            )

            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            for i in stderr.readlines():
                send_msg = (
                        "**告警时间：** "
                        + curtime()
                        + " \n **告警主机：** "
                        + self.host
                        + " \n **告警内容：** "
                        + i
                )
                make_mail(send_msg, warn_type="无法检测OGG")

            for i in stdout.readlines():
                # 计数进程和，不为0再进行处理

                v_proc_cnt = i.count("MANAGER")
                v_proc_cnt = v_proc_cnt + i.count("EXTRACT")
                v_proc_cnt = v_proc_cnt + i.count("REPLICAT")
                while v_proc_cnt >= 1:
                    # print(i)
                    # 确定取到进程行再进行切片，方便判断取值
                    v_lac = ''
                    time_since_ckpt = 0
                    v_proc_name = ''
                    v_proc_type = ''
                    v_proc_status = ''
                    lag_at_ckpt = ''
                    print(i)
                    v_i = i.split()
                    # 将进程与状态赋予变量，用于后面判断
                    if len(v_i) == 2:
                        v_proc_type = v_i[0]
                        v_proc_status = v_i[1]
                    elif len(v_i) >= 3:
                        # 进程类型
                        v_proc_type = v_i[0]
                        v_proc_status = v_i[1]
                        # 进程具体名称
                        v_proc_name = v_i[2]
                        # lag at chkpt，读取trail检查点延迟
                        v_lac = str(v_i[3]).split(":")
                        if len(v_lac) == 1:
                            lag_at_ckpt = v_lac[0]
                        else:
                            lag_at_ckpt = (
                                    int(v_lac[0]) * 3600
                                    + int(v_lac[1]) * 60
                                    + int(v_lac[2])
                            )
                            # print(lag_at_ckpt)
                        # print(v_lac)
                        # 切片time since ckpt，然后计算延迟秒数
                        v_tsc = str(v_i[4]).split(":")
                        # print(v_tsc)
                        time_since_ckpt = (
                                int(v_tsc[0]) * 3600 + int(v_tsc[1]) * 60 + int(v_tsc[2])
                        )
                        # print(time_since_ckpt)
                    if v_proc_type == "MANAGER":
                        # print(curtime())
                        # print(self.host)
                        # print(v_proc_type)
                        # print(v_proc_status)
                        send_msg = (
                                "**告警时间：** "
                                + curtime()
                                + " \n **告警主机：** "
                                + self.host
                                + " \n **OGG进程：** "
                                + v_proc_type
                                + " \n **当前状态 ：** "
                                + v_proc_status
                        )
                        print(send_msg)
                    else:
                        send_msg = (
                                "**告警时间：** "
                                + curtime()
                                + " \n **告警主机：** "
                                + self.host
                                + " \n **进程类型：** "
                                + v_proc_type
                                + " \n **进程名称 ：**  "
                                + v_proc_name
                                + " \n **当前状态 ：** "
                                + v_proc_status
                                + " \n **Lag at Chkpt：** "
                                + str(lag_at_ckpt)
                                + "s"
                                + " \n **Time Since Chkpt：** "
                                + str(time_since_ckpt)
                                + "s"
                        )
                        print(send_msg)
                    if v_proc_type == "MANAGER" and v_proc_status != "RUNNING":
                        make_mail(send_msg, warn_type="OGG MGR异常")
                    elif len(v_lac) == 1:
                        make_mail(send_msg, warn_type="OGG状态异常")
                    elif len(v_lac) > 1 and v_proc_type != "MANAGER" and v_proc_status == "ABENDED":
                        make_mail(send_msg, warn_type="OGG " + v_proc_type + "故障")
                    elif len(v_lac) > 1 and v_proc_type != "MANAGER" and v_proc_status == "STOPPED":
                        make_mail(send_msg, warn_type="OGG " + v_proc_type + "停止")
                    elif len(v_lac) > 1 and v_proc_type != "MANAGER" and lag_at_ckpt >= 600:
                        make_mail(send_msg, warn_type="OGG " + v_proc_type + "队列读延迟")
                    elif len(v_lac) > 1 and time_since_ckpt >= 600 and v_proc_type != "MANAGER":
                        make_mail(send_msg, warn_type="OGG " + v_proc_type + "应用延迟")

                    break

    def closed(self):
        self.ssh.close()


if __name__ == "__main__":
    for con_info in hostlist:
        host: str = con_info["host"]
        port = con_info["port"]
        username = con_info["user"]
        pwd = con_info["pwd"]
        oggdir = con_info["oggdir"]
        orahome = con_info["orahome"]
        ssh = SshOgg(host, port, username, pwd)
        ssh.check_ogg_status(orahome, oggdir)
        ssh.closed()
