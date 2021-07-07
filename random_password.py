import random
import string
import re
import hashlib

Pass_result = ""


def pass_random_md5():
    user_list = []
    global Pass_result
    punctuation = string.punctuation
    punctuation = punctuation.replace("&", "")
    for i in range(15):
        Your_pass = random.choice(string.ascii_letters + string.digits + punctuation)
        user_list.append(Your_pass)

    # 创建md5对象
    m = hashlib.md5()

    Pass_result = "".join(user_list)
    print(Pass_result)
    utf_pass = Pass_result.encode(encoding="utf-8")
    m.update(utf_pass)
    pass_md5 = m.hexdigest()
    return pass_md5


pass_random_md5()
