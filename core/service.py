from core import service, handler
from multiprocessing import Process
from utils import utils
from dao import save_data


def execute_task():
    p_consumers = []
    process_config = utils.build_process()
    shared_data = handler.init_shared_data()  # 初始化跨进程数据列表
    consumer_num = process_config['consumer']['size']  # 获取消费者数量（5个）

    # 启动生产者
    q = process_config['producer']['q']
    p_producer = Process(target=utils.generate_url, args=(q, consumer_num))
    p_producer.start()

    # 启动消费者（传递共享数据列表）
    q = process_config['consumer']['q']
    for _ in range(consumer_num):
        consumer_process = Process(target=handler.spider_data, args=(q, shared_data))
        consumer_process.start()
        p_consumers.append(consumer_process)

    # 等待生产者完成
    p_producer.join()
    print("生产者进程已结束")
    # 等待所有消费者完成
    for pro in p_consumers:
        pro.join()
    print("所有消费者进程已结束")

    # 打印最终数据量，方便排查
    total_data = len(shared_data)
    print(f"抓取完成 | 总数据量：{total_data}条")

    # 所有数据收集完成后，统一写入Excel
    save_data.save_data_excel(list(shared_data))  # 转成普通列表写入
    print("数据已写入 save_file/xunyiwenyao.xlsx")
