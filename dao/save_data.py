"""
@Author  : 孔天宇
@Desc    : 
"""
import os.path

import pandas as pd


def save_data_excel(data):
    # 将数据保存到excel中
    if not os.path.exists('save_file'):
        os.mkdir('save_file')
    pf = pd.DataFrame(data)
    path_file = os.path.join('./save_file', 'xunyiwenyao.xlsx')
    pf.to_excel(path_file, index=False)
