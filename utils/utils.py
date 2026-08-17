import time
from multiprocessing import Queue


def build_process():
    q = Queue()
    production = {
        'producer': {'size': 1, 'q': q},
        'consumer': {'size': 5, 'q': q}
    }
    return production


def generate_url(qu, consumer_num):
    # 获取页数
    for page in range(20):
        url = f'https://club.xywy.com/list_all_{1 + page}.htm'
        # 将url放进队列中
        qu.put(url)
        print(f"生产URL：{url}")  # 日志：打印生产的URL
        time.sleep(0.2)
    # 生产完所有URL后，放入「结束信号」（数量=消费者数）
    for _ in range(consumer_num):
        qu.put(None)
    print(f"所有URL生产完成（共20页），已放入{consumer_num}个结束信号")
