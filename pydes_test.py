import base64
from pyDes import *

Des_Key = "W2*&U<FR"  # Key 长度为8
Des_IV = b"\x52\x63\x78\x61\xBC\x48\x6A\x08"  # 自定IV向量


# 加密
def Encrption(str):
    k = des(Des_Key, CBC, Des_IV, padmode=PAD_PKCS5)
    return base64.b64encode(k.encrypt(str))


# 解密
def Deode(str):
    k = des(Des_Key, CBC, Des_IV, padmode=PAD_PKCS5)
    return k.decrypt(base64.b64decode(str))


if __name__ == "__main__":
    d = Encrption("j7OPm0%v6MXPSQoF")
    print(d)
    # print(Encrption("my name is").decode("utf-8"))
    print(str(Deode("l13jUuhuxw/+aIwKMtqO8w=="), "utf-8"))
