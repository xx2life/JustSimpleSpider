import datetime
import random
import time

import pymysql
import threadpool
import os
from apscheduler.schedulers.blocking import BlockingScheduler

import sys
sys.path.append('./../../')

from PublicOpinion.carticle.cbase import CArticleBase
from PublicOpinion.configs import DC_HOST, DC_PORT, DC_USER, DC_PASSWD, DC_DB

now = lambda: time.time()


class Schedule(object):
    def __init__(self):
        # 部分 code 可能查询不出对应的中文简称 所以这里不能对其 values 进行 sorted 比较
        self.keys = list(self.dc_info().values())
        random.shuffle(self.keys)

    def dc_info(self):  # {'300150.XSHE': '世纪瑞尔',
        """
        从 datacanter.const_secumain 数据库中获取当天需要爬取的股票信息
        返回的是 股票代码: 中文名简称 的字典的形式
        """
        try:
            conn = pymysql.connect(host=DC_HOST, port=DC_PORT, user=DC_USER,
                                   passwd=DC_PASSWD, db=DC_DB)
        except Exception as e:
            raise

        cur = conn.cursor()
        cur.execute("USE datacenter;")
        cur.execute("""select SecuCode, ChiNameAbbr from const_secumain where SecuCode \
            in (select distinct SecuCode from const_secumain);""")
        dc_info = {r[0]: r[1] for r in cur.fetchall()}
        cur.close()
        conn.close()
        return dc_info

    def start(self, key):
        c = CArticleBase(key=key)
        c.start()

    def thread_run(self):
        start_time = now()
        pool = threadpool.ThreadPool(4)
        requests = threadpool.makeRequests(self.start, self.keys)
        [pool.putRequest(req) for req in requests]
        pool.wait()
        print("用时: {}".format(now() - start_time))

    def simple_run(self):
        # 代理状态不好 所以不开启多线程了 一会就崩了
        start_time = now()
        for key in self.keys:
            self.start(key)
        print("用时: {}".format(now() - start_time))


# sche = Schedule()
# sche.simple_run()

# 尝试使用 apschedule 设置定时任务（：换个库新鲜一下 总之东财因为 ip 的问题一直是单独部署的
# https://github.com/agronholm/apscheduler/blob/master/examples/schedulers/blocking.py


def tick():
    print('Tick! The time is: %s' % datetime.datetime.now())
    sche = Schedule()
    sche.simple_run()


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    # scheduler.add_job(tick, 'interval', seconds=3)
    tick()
    scheduler.add_job(tick, 'interval', hours=15)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
