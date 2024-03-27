import pymysql
def exec_mysql(host: str, user: str, password: str, database: str, sql: str):
    """
    执行MySQL查询

    参数:
    host (str): MySQL服务器地址
    user (str): MySQL用户名
    password (str): MySQL密码
    database (str): MySQL数据库名
    sql (str): 要执行的SQL查询语句

    返回: dict
    status: bool
    data: list
    """
    try:
        db = pymysql.connect(host=host,
                            user=user,
                            password=password,
                            database=database)
        cursor = db.cursor()
        cursor.execute(f"{sql}")
        data = cursor.fetchall() # 获取所有结果
    except Exception as e:
        return {
            "status": False,
            "data": f"执行sql报错:{e}"
        }
    else:
        return {
            "status": True,
            "data": data
        }
    finally:
        db.close()
