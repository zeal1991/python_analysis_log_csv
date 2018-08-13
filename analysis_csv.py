#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from datetime import datetime, time, timedelta
from config import *
import json
import csv
import codecs

import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


def analysis():
    # 分析log日志文件,将json数据匹配出来

    # 根据配置文件里的起止日期,查询出所有日期
    datestart = datetime.strptime(date_start, '%Y-%m-%d')
    dateend = datetime.strptime(date_end, '%Y-%m-%d')
    date_list = [datestart.strftime('%Y-%m-%d')]
    while datestart < dateend:
        datestart += timedelta(days=1)
        date_list.append(datestart.strftime('%Y-%m-%d'))

    result = []
    if date_list is not None:
        log_names = {}
        for key, value in enumerate(date_list):
            # 拼接日志文件名称
            log_names[key] = 'nps_' + str(value) + '.log'
            # 查找到文件handle
            log_path = os.path.join(log_root_path, log_names[key])
            if not os.path.exists(log_path):
                print u'对不起,' + log_names[key] + u'文件不存在'
            else:
                with open(log_path.decode('utf-8'), 'r') as txt:
                    # txt.read().encode('utf-8')
                    for line in txt:
                        pattern = re.compile(r'yuanli dumping status:(.+)')
                        goal = pattern.search(line)
                        if goal is not None:
                            result.append(goal.groups()[0])

    return result


def create_csv():
    # 获取匹配到的数据
    data = analysis()
    # print data
    new_data = []
    for x in data:
        # 截取 yuanli dumping status: 字符
        # x = x[22:]
        x = x.decode('gbk')
        x = json.loads(x)
        # print x
        new_data.append([
            str(x['user']), str(x['event']), str(x['ts']),
            str(x['app'] if x['app'] else None),
            str(x['city'] if 'city' in x.keys() else None),
            str(x['modType'] if 'modType' in x.keys() else None),
            str(x['ip'] if 'ip' in x.keys() else None),
            str(x['module'] if 'module' in x.keys() else None),
            str(x['userName'] if 'userName' in x.keys() else None),
            str(x['url'] if 'url' in x.keys() else None),
            str(x['modId'] if 'modId' in x.keys() else None),
            str(x['conditions'] if 'conditions' in x.keys() else None),
            str(x['modAllCount'] if 'modAllCount' in x.keys() else None),
            str(x['mod1Count'] if 'mod1Count' in x.keys() else None),
            str(x['mod0Count'] if 'mod0Count' in x.keys() else None),
            str(x['modAUC'] if 'modAUC' in x.keys() else None),
            str(x['modShare'] if 'modShare' in x.keys() else None),
            str(x['forecastCount'] if 'forecastCount' in x.keys() else None),
            str(x['forecastDown'] if 'forecastDown' in x.keys() else None),
            str(x['dataPeriods'] if 'dataPeriods' in x.keys() else None),
            str(x['dataType'] if 'dataType' in x.keys() else None)
        ])

    t = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = 'new_analysis_'+str(t)+'.csv'
    csv_new = os.path.join(csv_root_path, file_name)
    print u'我们创建了新的文件'+file_name + u'在' + csv_root_path + u'路径下,请注意查收'

    fileHeader = [u'用户名ID', u'操作类型', u'访问时间', u'应用名', u'所属地市',
                  u'模型类型', u'访问ip', u'所属模块名', u'用户姓名', u'访问url',
                  u'模型id', u'条件', u'更新模型时使用的样本数据总量',
                  u'更新模型时使用的正样本数据总量',
                  u'更新模型时使用的负样本数据总量',
                  u'模型生成后的auc', u'模型共享范围', u'预测前的数据量',
                  u'下载的数据量', u'数据期数', u'数据类型']

    csvFile = open(csv_new, "wb")
    csvFile.write(codecs.BOM_UTF8)
    writer = csv.writer(csvFile)
    # 写入的内容都是以列表的形式传入函数
    writer.writerow(fileHeader)

    for item in new_data:
        writer.writerow(item)

    csvFile.close()


def main():
    create_csv()


if __name__ == '__main__':
    main()
