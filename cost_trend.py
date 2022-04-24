import os  # 读文件用，自带的，
from pyecharts import Bar  # 画柱状图用
from pyecharts import Line  # 画折线图用

if __name__ == "__main__":
    ALL_DATA = []
    cost_file = "C:/Users/Administrator/Desktop/1.txt"
    with open(cost_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        # 获取所有sql_id，不重复，用sql_id来获取其他性能数据
        number = []
        for lss in lines:
            # 去掉换行符
            m = lss.replace("\n", "")
            # print(m)
            # print(lss.split())
            sql_id = lss.split()[3]
            if sql_id not in number:
                number.append(sql_id)
        print(number)
        for j in range(len(number)):
            sql_id_w = number[j]
            for lss in lines:
                lss = lss.replace("\n", "")
                sql_id_n = lss.split()[3]

                if sql_id_w == sql_id_n:
                    snap_id = lss.split()[0]
                    cost = lss.split()[5]
                    ALL_DATA.append({"snap_id": snap_id, "cost": cost})

            # 一个sql_id相关数据获取完成，开始画图
            show_data = ALL_DATA
            snap_id = list(map(lambda ALL_DATA: ALL_DATA["snap_id"], show_data))
            cost = list(map(lambda ALL_DATA: int(ALL_DATA["cost"]), show_data))
            chart = Bar(f"sql_id:{sql_id_w} cost变化趋势图:")  # 需要安装pyechart模块
            chart.add("cost变化趋势图", snap_id, cost)
            f_out = f"sql_cost_{sql_id_w}.html"
            chart.render(f_out)
            line = Line("cost变化趋势图", title_top="50%")
            line.add("cost变化趋势图", snap_id, cost)
            line.show_config()
            f_out = f"sql_cost_line_{sql_id_w}.html"
            line.render(f_out)
            ALL_DATA = []