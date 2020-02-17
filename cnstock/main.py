import sys
import time

sys.path.append("./../")
from cnstock.cn_4_hours import CNStock_2
from cnstock.hongguan import CNStock


def task():
    task_info = {
        'qmt-sns_yw': "要闻-宏观",
        "qmt-sns_jg": "要闻-金融",

        "qmt-scp_gsxw": "公司-公司聚焦",
        "qmt-tjd_ggkx": "公司-公告快讯",
        "qmt-tjd_bbdj": "公司-公告解读",

        "qmt-smk_gszbs": "市场-直播",
        "qmt-sx_xgjj": "市场-新股-新股聚焦",
        "qmt-sx_zcdt": "市场-新股-政策动态",
        "qmt-sx_xgcl": "市场-新股-新股策略",
        "qmt-sx_ipopl": "市场-新股-IPO评论",

        "qmt-smk_jjdx": "市场-基金",
        "qmt-sns_qy": "市场-券业",
        "qmt-smk_zq": "市场-债券",
        "qmt-smk_xt": "市场-信托",

        "qmt-skc_tt": "科创板-要闻",
        "qmt-skc_jgfx": "科创板-监管",
        "qmt-skc_sbgsdt": "科创板-公司",
        "qmt-skc_tzzn": "科创板-投资",
        "qmt-skc_gd": "科创板-观点",
        "qmt-sjrz_yw": "新三板-要闻",
    }
    now = lambda: time.time()
    for topic in task_info:
        print("{} spider strat.".format(task_info.get(topic)))
        t1 = now()
        runner = CNStock(topic=topic)
        runner.start()
        print("{} spider end, use {} s.\n\n".format(
            task_info.get(topic),
            (now() - t1)
        )
        )
    # 上证四小时是不同的网页模式
    t2 = now()
    print("{} spider strat.".format("上证4小时"))
    runner = CNStock_2()
    runner.start()
    print("{} spider end, use {} s.\n\n".format(
        "上证4小时",
        (now() - t2)
    )
    )


task()