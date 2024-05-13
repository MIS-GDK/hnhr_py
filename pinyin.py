from pypinyin import pinyin
# 输入name
def get_pinyin_first_alpha(name):
    return "".join([i[0][0].upper() for i in pinyin(name)])


with open(r"C:\Users\Administrator\Desktop\1.txt", mode="rt", encoding="utf-8") as f:
    line = f.readline().strip()
    while line:
        print(get_pinyin_first_alpha(line))
        line = f.readline().strip()
