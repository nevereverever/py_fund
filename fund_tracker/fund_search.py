import json
import requests
import time
import datetime
from fund_tracker import fund
from fund_tracker import file_helper

# 基金url请求前缀
url = "https://fundgz.1234567.com.cn/js/";


# 将jsonp结构转换json字符串
def jsonp_to_json(jsonp):
    content_str = jsonp.decode();
    return content_str.replace("jsonpgz(", "").replace(");", "");


# 获取指定基金详细数据
def get_content(session, url, fundcode):
    response = session.get(url + fundcode + ".js?_=" + str(datetime.datetime.now().timetuple()))
    if response.status_code != 200:
        return None;
    return response.content;


def get_fund_detail(fundcode, share):
    # 请求头
    headers = {
        "Host": "fundgz.1234567.com.cn",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Accept": "*/*",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Dest": "script",
        "Referer": "https://favor.fund.eastmoney.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    headers_dict = {
        **headers
    }
    session = requests.Session();
    session.headers = headers_dict;
    content = get_content(session, url, fundcode)
    # 基金详情
    content_str = jsonp_to_json(content);
    i = 1
    # 对于没有得到基金详细数据的，重试2次
    while content_str == '':
        print("------数据为空，重试中------")
        if i > 2:
            break
        time.sleep(1)
        content = get_content(session, url, fundcode);
        content_str = jsonp_to_json(content);
        i = i + 1;
    # 将基金详情转换为json对象
    funds_json = json.loads(content_str)
    funds_json["share"] = share
    # 将json对象转换为python中基金Fund对象方便后续处理
    return fund.Fund(funds_json["fundcode"], funds_json["name"], funds_json["gsz"], funds_json["gztime"],
                     funds_json["dwjz"], funds_json["jzrq"], funds_json["gszzl"], funds_json["share"]);


# 请求并解析得到所有买入基金数据的dict key为基金的code value为基金详情对象
def get_fund_dict(codes=file_helper.read_properties_to_dict("myfund.properties")):
    fund_dict = {}
    # 遍历要查询的所有基金
    for k, v in codes.items():
        fund_dict[k] = get_fund_detail(k, v);
    return fund_dict;


def get_code_name_dict(fund_dict):
    code_name_dict = {}
    for k, v in fund_dict.items():
        code_name_dict[k] = v.name;
    return code_name_dict;
