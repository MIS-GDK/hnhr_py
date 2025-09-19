import pandas as pd
from sqlalchemy import create_engine, Text, text
from sqlalchemy.types import VARCHAR, Integer, DECIMAL
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from urllib.parse import quote_plus


def get_postgres_types(df):
    """
    根据DataFrame的数据类型生成PostgreSQL数据类型映射
    """
    type_dict = {}
    for col, dtype in zip(df.columns, df.dtypes):
        if "object" in str(dtype):
            type_dict[col] = Text()
        elif "float" in str(dtype):
            type_dict[col] = DOUBLE_PRECISION
        elif "int" in str(dtype):
            type_dict[col] = Integer()
        elif "decimal" in str(dtype):
            type_dict[col] = DECIMAL(20, 2)
    return type_dict


def import_to_postgres(file_path, table_name, schema=None):
    """
    将文件数据导入到PostgreSQL数据库
    """
    try:
        # 读取数据文件
        df = pd.read_csv(file_path, sep="\t", encoding="utf-8")
        print(f"读取到 {len(df)} 行数据")

        # 获取数据类型映射
        dtype_dict = get_postgres_types(df)
        password = quote_plus("Syk,.%902ddk2@9")
        # 创建数据库连接
        engine = create_engine(
            f"postgresql://postgres:{password}@172.18.23.13:26699/postgres"
        )

        # 导入数据
        df.to_sql(
            table_name,
            engine,
            schema=schema,
            if_exists="replace",
            index=False,
            dtype=dtype_dict,
        )

        # 验证导入结果
        with engine.connect() as conn:
            table_path = f"{schema+'.' if schema else ''}{table_name}"
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_path}")).scalar()
            print(f"成功导入 {result} 行数据到表 {table_path}")

    except Exception as e:
        print(f"导入失败: {str(e)}")
    finally:
        if "engine" in locals():
            engine.dispose()


if __name__ == "__main__":
    # 调用导入函数
    import_to_postgres(
        file_path="C:/Users/Administrator/Desktop/1.txt",
        table_name="t_receiver_user",
        schema="bilocal",  # 可选参数，不指定则使用默认schema
    )
