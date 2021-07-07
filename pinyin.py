from pypinyin import pinyin

# 输入name
def get_pinyin_first_alpha(name):
    return "".join([i[0][0].upper() for i in pinyin(name)])


print(get_pinyin_first_alpha("郑州大学第一附属医院"))
