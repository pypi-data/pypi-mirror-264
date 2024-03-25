# -*-coding:utf-8-*-
# Author: Eason.Deng
# Github: https://github.com/holbos-deng
# Email: 2292861292@qq.com
# CreateDate: 2022/10/28 15:52
# Description:
import time
from perfect_eval import eval_expr
from datetime import datetime


def test_eval():
    t1 = time.time()

    eval_expr("print('hello world')", {"print": print})
    print(eval_expr("now.strftime('%m-%d')", {"now": datetime.now()}))
    print(eval_expr("a + b", {"a": 123, "b": 456}))
    print(eval_expr("f'{a} + {b} = {a + b}'", {"a": 123, "b": 456}))
    print(eval_expr("match(a, [(1, '11'), (2, '22'), (3, '33')], default='ooo')", {"a": 1}))
    print(eval_expr(r"re.sub(r'\d+', '很多', count)", {"count": '10个'}))
    print(eval_expr(
        """(x := random.randint(1, 10)) and (x <= 4 and random.choice(["好的", "好哦", "好呢"])) or (x <= 10 and "....")"""))

    print(eval_expr(
        '''match(weather_condition, [("晴", "晴空万里"), ("多云", "浮云甚多"), ("阴", random.choice(["乌云密布", "乌云低垂"])),
        ("小雨", "落细雨"), ("中雨", "淅沥中雨"), ("大雨", "大雨滂沱")])''',
        {"weather_condition": "阴"}))

    print(eval_expr("time.sleep(3)"))

    print(time.time() - t1)


if __name__ == "__main__":
    test_eval()
