import time
import traceback

import requests
from lxml import etree
from config import settings
from multiprocessing import Manager  # 新增：跨进程共享列表


# 新增：初始化跨进程数据列表（替代直接写入）
def init_shared_data():
    manager = Manager()
    return manager.list()


def spider_data(qu, shared_data):
    num = 0
    # 向url发送请求并获取数据
    while True:
        # # 如果队列为空值则跳出循环
        # if qu.empty():
        #     break
        # 先取数据，再判断是否为结束信号（核心修复）
        url_ = qu.get()
        if url_ is None:  # 收到结束信号则退出
            print("收到结束信号，消费者进程退出")
            break
        try:
            request = requests.get(url_, headers=settings.HEADERS)
            request.encoding = 'gbk'
            url_data = request.text
            # 对数据进行提取
            tree = etree.HTML(url_data)
            div_list = tree.xpath('//div[@class="ksAll-list bgfff clearfix"]/div')
            num += 1
            print(f'第{num}页开始抓取,抓到{len(div_list)}条数据')

            for div in div_list:
                data = {}
                title = div.xpath('.//a[@class="fl th"]/text()')[0]
                text = div.xpath('.//div[@class="ask-con "]//p/text()')[0]
                data['标题'] = title
                data['内容'] = text
                shared_data.append(data)  # 加入共享列表
                # print(f'{title}:::{text}')
            # 将数据保存到excel文件中
            time.sleep(0.1)

        except Exception as e:
            print(traceback.format_exc())
            print('异常捕获', e)
