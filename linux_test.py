import pyodbc

try:
    sql_PIM = pyodbc.connect(
        "DRIVER={SQL Server};SERVER=192.168.0.165;DATABASE=suerp;UID=hrhn_suerp;PWD=OcZi2UktnEwM"
    )
except Exception as e:
    print(e)