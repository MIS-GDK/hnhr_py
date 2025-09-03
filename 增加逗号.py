import os


def add_comma(address, filename):
    # 使用os.path.join拼接路径，兼容不同操作系统
    filepath = os.path.join(address, filename)
    # 以读模式打开文件，读取所有行到列表
    with open(filepath, "r", encoding="UTF-8") as f:
        lines = f.readlines()
    # 以写模式打开同一文件，准备写入处理后的内容
    with open(filepath, "w", encoding="UTF-8") as f:
        for idx, line in enumerate(lines):
            # 去除每行末尾换行和首尾空格
            content = line.rstrip("\n").strip()
            if idx != len(lines) - 1:
                # 不是最后一行，末尾加逗号
                f.write(f"{content},\n")
            else:
                # 最后一行，不加逗号
                f.write(f"{content}\n")


# 调用函数，处理桌面上的2.txt文件
add_comma("C:/Users/Administrator/Desktop", "2.txt")
