# -*- coding: utf-8 -*-

import os
from os.path import expanduser

# DATA_DIR
data_dir = os.path.join(expanduser('~'), 'data')

# 配置log文件路径
log_root_path = os.path.join(data_dir, 'logs')
# 配置csv文件路径
csv_root_path = os.path.join(data_dir, 'csv')
# 配置需要日期区间,包含起止日期
date_start = '2018-08-07'
date_end = '2018-08-10'
