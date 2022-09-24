#!/usr/bin/python
# -*- coding: UTF-8 -*-
import akshare as ak

stocks = {"成都银行":"601838","兖矿能源":"600188","江苏银行":"600919","陕西煤业":"601225","中国神华":"601088","中煤能源":"601898",
          "南京银行":"601009","锦浪科技":"300763","长安汽车":"000625","TCL中环":"002129","容百科技":"688005","兴业银行":"601166",
          "中国石油":"601857","中国中铁":"601390","中科曙光":"603019","紫金矿业":"601899","藏格矿业":"000408","宝钢股份":"600019",
          "北方稀土":"600111","德赛西威":"002920","东鹏饮料":"605499","国电电力":"600795","杭州银行":"600926","合盛硅业":"603260",
          "绿地控股":"600606","上港集团":"600018","上机数控":"603185","特变电工":"600089","天合光能":"688599","天齐锂业":"002466",
          "通威股份":"600438","万泰生物":"603392","新城控股":"601155","盐湖股份":"000792","邮储银行":"601658","中国东航":"600115",
          "中国建筑":"601668","中国交建":"601800"}

def do_fetch():
    file = open('./temp.csv', 'w')
    for head in ["股票名称","1月末","2月末","3月末","4月末","5月末","6月末","7月末","8月末"]:
        file.write(head)
        file.write(",")
    file.write("\n")

    for st in stocks.items():
        name = st[0]
        symbol = st[1]
        result={}
        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=symbol, period="monthly", start_date="20220101",
                                                end_date='20220901',
                                                adjust="qfq")
        for i in range(1,9):
            result[str(i)] = round(stock_zh_a_hist_df['涨跌幅'].head(i).sum(),2)

        file.write(name)
        file.write(",")
        for i in range(1, 9):
            file.write(str(result[str(i)]))
            file.write(",")
        file.write("\n")
        print(name, result)
    file.close()

if __name__ == "__main__":
    do_fetch()
