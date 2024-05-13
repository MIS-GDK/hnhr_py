import base64
import datetime
import hashlib
import hmac
import json
import os
import re
import time
import urllib

import paramiko
import requests

hostlist = [
    {
        "host": "IP地址",
        "port": "ssh端口",
        "user": "ogg操作系统用户",
        "pwd": "xxxx",
        "oggdir": "ogg安装目录",
        "orahome": "oracle_home目录",
    }
]

# 钉钉发送函数，输入markdown格式消息文本即可发送
def send_message(send_msg, warn_type):
    ### 钉钉配置 begin ###
    # 如果是内网，需要有互联网代理配置
    # proxies = {'http':'http://IP:PORT','https':'http://IP:PORT'}
    # os.environ["https_proxy"] = "http://IP:PORT"
    webhook = "钉钉机器人webhook地址"
    timestamp = str(round(time.time() * 1000))
    secret = "钉钉机器人加密密钥"
    secret_enc = secret.encode("utf-8")
    string_to_sign = "{}\n{}".format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode("utf-8")
    hmac_code = hmac.new(
        secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
    ).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    webhook = webhook + "&timestamp=" + timestamp + "&sign=" + sign
    # timestamp 与系统当前时间戳如果相差1小时以上，则认为是非法的请求，所以需要注意发送消息服务器时间不能与标准时间相差超过一小时
    headers = {"Content-Type": "application/json"}
    user = "all"
    ### 钉钉配置 end ###
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "数据库告警",
            "text": f'# <font face="华云彩绘" color="#FF0000" size="10">{warn_type}</font> \n '
            + send_msg,
        },
        "at": {"atMobiles": [user], "isAtAll": False},
    }
    # print(data)
    x = requests.post(url=webhook, data=json.dumps(data), headers=headers)
    # 打印发送钉钉结果
    print("钉钉推送结果为： " + str(x.json()) + "\n")


def curtime():
    timenow = str(datetime.datetime.now()) + " "
    return timenow


# 定义一个休眠循环，定期执行脚本
def sleeptime(hour, min, sec):
    return hour * 3600 + min * 60 + sec


class SshOgg:
    def __init__(self, host, port, username, pwd):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.orahome = orahome
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.host, self.port, self.username, self.pwd, timeout=5)
            self.sshinvalid = False
            print(self.sshinvalid)
        except:
            self.sshinvalid = True
            print(self.sshinvalid)

    def check_ogg_status(self, orahome, oggdir):
        if self.sshinvalid:
            send_msg = "**告警时间：** " + curtime() + " \\\n **告警主机：** " + self.host
            send_message(send_msg, warn_type="主机SSH无法连接")
        else:
            # 考虑AIX与Linux不同平台library path不同，所以一起设置，防止需要多判断处理不同平台
            cmd = (
                'export LD_LIBRARY_PATH=%s/lib:%s && export LD_LIBRARY_PATH=%s/lib:%s && echo "info all" |%s/ggsci'
                % (orahome, oggdir, orahome, oggdir, oggdir)
            )
            # print(cmd)
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            # print(stdout.readlines)
            for i in stderr.readlines():
                send_msg = (
                    "**告警时间：** "
                    + curtime()
                    + " \\\n **告警主机：** "
                    + self.host
                    + " \\\n **告警内容：** "
                    + i
                )
                send_message(send_msg, warn_type="无法检测OGG")
                print(i)
            # print(stdout.readlines)
            for i in stdout.readlines():
                # 计数进程和，不为0再进行处理
                v_proc_cnt = i.count("MANAGER")
                v_proc_cnt = v_proc_cnt + i.count("EXTRACT")
                v_proc_cnt = v_proc_cnt + i.count("REPLICAT")
                while v_proc_cnt >= 1:
                    # 确定取到进程行再进行切片，方便判断取值
                    v_i = i.split()
                    print(v_i)
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
                            print(lag_at_ckpt)
                        print(v_lac)
                        # 切片time since ckpt，然后计算延迟秒数
                        v_tsc = str(v_i[4]).split(":")
                        print(v_tsc)
                        time_since_ckpt = (
                            int(v_tsc[0]) * 3600 + int(v_tsc[1]) * 60 + int(v_tsc[2])
                        )
                        print(time_since_ckpt)

                    if v_proc_type == "MANAGER":
                        print(curtime())
                        print(self.host)
                        print(v_proc_type)
                        print(v_proc_status)
                        send_msg = (
                            "**告警时间：** "
                            + curtime()
                            + " \\\n **告警主机：** "
                            + self.host
                            + " \\\n **OGG进程：** "
                            + v_proc_type
                            + " \\\n **当前状态 ：** "
                            + v_proc_status
                        )
                    else:
                        send_msg = (
                            "**告警时间：** "
                            + curtime()
                            + " \\\n **告警主机：** "
                            + self.host
                            + " \\\n **进程类型：** "
                            + v_proc_type
                            + " \\\n **进程名称 ：**  "
                            + v_proc_name
                            + " \\\n **当前状态 ：** "
                            + v_proc_status
                            + " \\\n **Lag at Chkpt：** "
                            + str(lag_at_ckpt)
                            + "s"
                            + " \\\n **Time Since Chkpt：** "
                            + str(time_since_ckpt)
                            + "s"
                        )
                    """
                    1.
    
                    """
                    if v_proc_type == "MANAGER" and v_proc_status == "RUNING":
                        send_message(send_msg, warn_type="OGG MGR正常")
                        time.sleep(3)
                    elif v_proc_type == "MANAGER" and v_proc_status != "RUNNING":
                        send_message(send_msg, warn_type="OGG MGR异常")
                        time.sleep(3)
                    # 进程lag at chkpt如果状态为unknown则，len(v_lac)为1
                    elif len(v_lac) == 1:
                        send_message(send_msg, warn_type="OGG状态异常")
                        time.sleep(3)
                    elif len(v_lac) > 1 and v_proc_status == "ABENDED":
                        send_message(send_msg, warn_type="OGG故障")
                        time.sleep(3)
                    elif len(v_lac) > 1 and v_proc_status == "STOPPED":
                        send_message(send_msg, warn_type="OGG停止")
                        time.sleep(3)
                    elif len(v_lac) > 1 and lag_at_ckpt >= 1800:
                        send_message(send_msg, warn_type="OGG队列读延迟")
                        time.sleep(3)
                    elif time_since_ckpt >= 1800:
                        send_message(send_msg, warn_type="OGG应用延迟")
                        time.sleep(3)
                    elif v_proc_type == "EXTRACT" and v_proc_status != "RUNNING":
                        send_message(send_msg, warn_type="OGG EXTRACT异常")
                        time.sleep(3)
                    elif v_proc_type == "REPLICAT" and v_proc_status != "RUNNING":
                        send_message(send_msg, warn_type="OGG应用异常")
                        time.sleep(3)
                    else:
                        send_message(send_msg, warn_type="其他情况")
                        time.sleep(3)
                    # while只执行一次即重新获取下一行进程信息判断，避免陷入死循环
                    break

    def closed(self):
        self.ssh.close()


# 定时格式为时，分，秒，间隔5分钟执行一次
second = sleeptime(0, 0, 10)
# 用于监测脚本本身，定时发送脚本运行邮件，防止脚本自身异常
exec_cnt = 0
while 1 == 1:
    for con_info in hostlist:
        host = con_info["host"]
        port = con_info["port"]
        username = con_info["user"]
        pwd = con_info["pwd"]
        oggdir = con_info["oggdir"]
        orahome = con_info["orahome"]
        ssh = SshOgg(host, port, username, pwd)
        print("\n------------%s上ogg进程运行状态信息------------" % host)
        print(curtime() + "\n")
        ssh.check_ogg_status(orahome, oggdir)
        ssh.closed()
    print(curtime())
    exec_cnt = exec_cnt + 1
    print("Current execute count is :" + str(exec_cnt) + "\n")
    if exec_cnt == 10:
        send_message("This scripts is running!", warn_type="推送服务监测")
        exec_cnt = 0
    time.sleep(second)
