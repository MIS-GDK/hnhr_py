#2023年客户销售汇总，只看销售金额含税、无税的汇总

import pandas as pd
import glob
import os
import warnings
from openpyxl import Workbook

# 忽略来自openpyxl.styles.stylesheet模块的特定警告
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl.styles.stylesheet")

# 使用glob获取所有月份的销售明细Excel文件路径，假设文件都在当前目录下，文件名类似"2023-01.xlsx"这样的格式
excel_files = glob.glob(os.path.join("C:\\Users\\Administrator\\Desktop\\2023年全年销售明细", "*"))

# 打印获取到的Excel文件路径列表，方便查看是否正确获取到文件
print("获取到的Excel文件路径列表:", excel_files)

# 定义需要读取的列，包含两列销售金额以及其他相关列，按需调整列名
columns_to_read = ["客户名称","收单方", "含税金额", "无税金额", "客户分类", "条线", "客户所在省", "客户所在市", "客户所在县"]
data_frames = []

# 遍历每个Excel文件，读取数据并添加到列表中，同时详细捕捉读取过程中的异常情况
for file in excel_files:
    try:
        df = pd.read_excel(
            file,
            usecols=columns_to_read,
            dtype={"含税金额": "float64", "无税金额": "float64"}
        )
        # 验证数据框是否为空，如果为空则打印提示信息
        if df.empty:
            print(f"从文件 {file} 读取的数据框为空，请检查该文件的数据情况及筛选条件！")
        else:
            data_frames.append(df)
    except Exception as e:
        print(f"读取文件 {file} 时出现严重错误，错误信息如下: {e.__class__.__name__}: {e}")

# 只有当成功读取到非空的数据框时，才进行拼接操作
if data_frames:
    # 将列表中的所有数据合并成一个大的DataFrame，使用ignore_index避免不必要的索引重复问题
    combined_df = pd.concat(data_frames, ignore_index=True)

    # 先按照"客户名称"和"收单方"进行分组，并汇总含税金额和无税金额，同时选取"客户分类"、"条线"及新增三列字段
    result = combined_df.groupby(["客户名称", "收单方"]).agg({
        "含税金额": "sum",
        "无税金额": "sum",
        "客户分类": "last",
        "条线": "last",
        "客户所在省": "last",
        "客户所在市": "last",
        "客户所在县": "last"
    }).reset_index()

    # 调整列的顺序，将收单方列放在客户名称列后面
    result = result[["客户名称", "收单方", "含税金额", "无税金额", "客户分类", "条线", "客户所在省", "客户所在市", "客户所在县"]]

    # 获取第一个Excel文件所在的目录路径，以此作为新文件的保存目录（假设所有文件在同一目录下）
    # 如果没有找到任何文件，这里会报错，实际中可以根据情况做更完善的错误处理
    save_path = os.path.dirname(excel_files[0])

    # 将结果写入到新的Excel表格"2023年全年客户销售汇总表.xlsx"中，指定引擎为openpyxl提高写入效率
    # 组合保存路径和文件名，确保新文件保存在原文件夹内
    result.to_excel(os.path.join(save_path, "2023年全年客户销售汇总表.xlsx"), index=False, engine="openpyxl")
else:
    print("没有成功读取到有效的销售明细数据，无法进行汇总操作，请检查文件及读取过程！")
