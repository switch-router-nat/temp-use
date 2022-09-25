#!/usr/bin/python
# -*- coding: UTF-8 -*-
import akshare as ak

stocks = {"长沙银行":"601577","紫金银行":"601860","上海银行":"601229","中信银行":"601998","成都银行":"601838","渝农商行":"601077",
          "中国银行":"601988","建设银行":"601939","邮储银行":"601658","郑州银行":"002936","常熟银行":"601128","光大银行":"601818",
          "农业银行":"601288","青农商行":"002958","青岛银行":"002948","华夏银行":"600015","民生银行":"600016","浦发银行":"600000",
          "招商银行":"600036","贵阳银行":"601997","杭州银行":"600926","北京银行":"601169","重庆银行":"601963","张家港行":"002839",
          "兴业银行":"601166","西安银行":"600928","宁波银行":"002142","工商银行":"601398","苏农银行":"603323","浙商银行":"601916",
          "沪农银行":"601825","交通银行":"601328","南京银行":"601009","无锡银行":"600908","苏州银行":"002966","平安银行":"000001",
          "齐鲁银行":"601665","江苏银行":"600919","兰州银行":"001227","瑞丰银行":"601528","厦门银行":"601187","江阴银行":"002807"}
stocks_test = {"长沙银行":"601577","紫金银行":"601860","上海银行":"601229","中信银行":"601998","成都银行":"601838","渝农商行":"601077"}

moment = ["20180101","20180201","20180301","20180401","20180501","20180601","20180701","20180801","20180901","20181001","20181101","20181201",
          "20190101","20190201","20190301","20190401","20190501","20190601","20190701","20190801","20190901","20191001","20191101","20191201",
          "20200101","20200201","20200301","20200401","20200501","20200601","20200701","20200801","20200901","20201001","20201101","20201201",
          "20210101","20210201","20210301","20210401","20210501","20210601","20210701","20210801","20210901","20211001","20211101","20211201",
          "20220101","20220201","20220301","20220401","20220501","20220601","20220701","20220801","20220901","20221001","20221101","20221201"]

#持仓 list
position = []


# 净值
result = 1

# 根据一年内的数据df, 计算过去 mouth 月内的净值变化 假设初始值为 1
def calc_chg(df, month):
    value = 1
    for i in range(12 - month, 12):
        chg = df.loc[i, ['涨跌幅']]
        value = value * (1 + float(chg / 100))
    return value

# 获取在时刻 t_index 时, 各只股票的净值变化
def get_all_data(t_index, last_n_month):
    value_dict={}
    for st in stocks.items():
        name = st[0]
        symbol = st[1]
        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=symbol, period="monthly", start_date=moment[t_index - 12],
                                                end_date = moment[t_index],
                                                adjust="qfq")
        # print(stock_zh_a_hist_df)
        # 如果没有获取到过去完整 12 个月的数据，说明是次新，排除掉
        if len(stock_zh_a_hist_df) < 12:
            print("%s 未上市超过 12 个月, 过滤掉" % name)
            continue

        # 保存过去3个月内的净值变化
        value_dict[name] = calc_chg(stock_zh_a_hist_df, last_n_month)

    print("当期银行股表现:")
    print(value_dict)
    return value_dict

# 对 data_dict 排序, 获取前 top 个元素
def get_top(data_dict, top):
    sorted_list = sorted(data_dict.items(), key=lambda item: item[1], reverse=True)
    return sorted_list[:top]

def get_name_list(data_list):
    name_list=[]
    for item in data_list:
        name_list.append(item[0])
    return name_list

# 更新净值变化
def update_result(data):
    global result
    old_dict = {}
    vector = 0
    num_position = len(position)
    if num_position == 0:
        return

    for s in position:
        old_dict[s] = data[s]

    print(old_dict)
    for st in old_dict.items():
        vector = vector + st[1]/num_position

    result = result * vector
    print("净值更新为 %f" % result);

def update_position(time, data):
    old_dict={}
    print("%s 调仓" % moment[time])
    print("上个周期持仓:")
    print(position)

    new_list = get_top(data, 2)
    print("上个周期表现最好的股票:")
    print(new_list)

    new_list_name = get_name_list(new_list)

    if len(position) > 0:
        for s in position:
            old_dict[s] = data[s]

        print("上个周期的持仓表现")
        print(old_dict)
        # 清空持仓
        position.clear()
        # 重新加入旧持仓的 Top 1 只股票
        position.append(get_top(old_dict, 1)[0][0])
        print("保留 %s" % position[0])
        if new_list_name[0] in position:
            # 移入上个周期表现 2nd 好的股票
            position.append(new_list_name[1])
        else:
            # 移入上个周期表现 1st 好的股票
            position.append(new_list_name[0])
    else:
        # 加入
        position.append(new_list[0][0])
        position.append(new_list[1][0])
    print("新持仓:")
    print(position)

def save2file(file, t_index, result):
    file.write(moment[t_index])
    file.write(",")

    file.write(str(result))
    file.write(",")

    for s in position:
        file.write(s)
        file.write(",")

    file.write("\n")

def run():
    global result

    file = open('./work15.csv', 'w')
    for head in ["时刻","净值","持仓股票1","持仓股票2"]:
        file.write(head)
        file.write(",")
    file.write("\n")

    # 从 moment_index = 12 也就是 20190101 开始, 每 3 个月进行调仓
    interval = 3
    for t in range(12, 56, interval):
        print("-------------------")
        print(moment[t])
        # 获取上个周期数据
        data = get_all_data(t, interval)
        # 计算上个周期净值变化
        update_result(data)
        # 调仓
        update_position(t, data)
        # 保存到文件
        save2file(file, t, result)

    file.close()
    print("==================================")
    print ("最终净值 %f" % result)

if __name__ == "__main__":
    run()
