import datetime


def generate_plsql_updates(creates, updates, expected_count):
    plsql_block_template = """
{creates}

DECLARE
  l_count NUMBER := 0;
  expected_count CONSTANT NUMBER := {expected_count};
BEGIN
{updates}IF l_count = expected_count THEN
    COMMIT;
    DBMS_OUTPUT.PUT_LINE('success!');
  ELSE
    ROLLBACK;
    DBMS_OUTPUT.PUT_LINE('fail!共更新' || l_count || '条数据');
  END IF;
END;
/
"""

    update_statements = []
    create_statements = []
    for update in updates:
        update_statements.append(
            f"{update};\n\n  l_count := l_count + SQL%ROWCOUNT;\n\n"
        )
    combined_updates = "".join(update_statements)

    for create in creates:
        create_statements.append(f"{create};\n\n")

    combined_reates = "".join(create_statements)

    plsql_block = plsql_block_template.format(
        expected_count=expected_count,
        creates=combined_reates,
        updates=combined_updates,
    )

    return plsql_block


def read_data():
    # 示例用法
    with open(r"C:\Users\Administrator\Desktop\1.txt", mode="r", encoding="utf-8") as f:
        sql_script_content = f.read()
    # 使用SQL关键字进行区分
    create_statements = []
    update_statements = []
    lines = sql_script_content.split(";")
    for line in lines:
        line = line.strip()  # 移除行首尾空白字符
        if line.upper().startswith("CREATE TABLE"):
            create_statements.append(line)
        elif line.upper().startswith("UPDATE"):
            update_statements.append(line)

    # with open(r"C:\Users\Administrator\Desktop\1.txt", mode="r", encoding="utf-8") as f:
    #     for line in f:
    #         # 如果当前行包含分号，则添加到current_data并清空以便开始收集下一段数据
    #         if ";" in line:
    #             update_data += line.split(";")[0]
    #             updates.append(update_data)
    #             update_data = ""
    #         else:
    #             # 若当前行没有分号，那么直接累加到当前数据段
    #             update_data = update_data + line

    # print(updates)
    return create_statements, update_statements


def write_data(data):
    current_date = datetime.datetime.today().strftime("%Y.%m.%d")
    print(current_date)
    with open(
        r"C:\Users\Administrator\Desktop\数据修复-OGG接口报错" + current_date + r".sql",
        mode="w",
        encoding="utf-8",
    ) as f:
        f.write(data)


expected_count = 2
creates_list, updates_list = read_data()
plsql_script = generate_plsql_updates(creates_list, updates_list, expected_count)
print(plsql_script)
write_data(plsql_script)
