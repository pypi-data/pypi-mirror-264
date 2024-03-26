import os
import pandas as pd

def list_write_excel(data: list, filename=None):
    """
    将列表字典写入excel中
    @param data: 数据,列表字典
    @param filename: 文件名[可选]
    """
    # 判断data是否为list类型
    if not isinstance(data, list):
        raise Exception('传入data必须为list类型')
    if filename and not str(filename).endswith('.xlsx'):
        filename = filename + '.xlsx'
    df = pd.DataFrame(data)
    if filename:
        df.to_excel(filename, index=False)
    else:
        # data.xlsx的文件存在则删除
        try:
            os.remove('data.xlsx')
        except FileNotFoundError:
            pass
        df.to_excel('data.xlsx', index=False)
    print('数据写入成功')
