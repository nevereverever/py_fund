import json
import requests
import datetime
from fund_tracker import fund
from fund_tracker import file_helper


#########################
# 将jsonp结构转换json字符串
#########################
def jsonp_to_json(jsonp):
    content_str = jsonp.decode()
    return content_str.replace("jsonpgz(", "").replace(");", "")


###############################
# 发送网络请求，获取指定基金详细数据
###############################
def get_fund_details(fundcode):
    # 基金url请求地址前缀
    url = "https://fundgz.1234567.com.cn/js/"
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
    session = requests.Session()
    session.headers = headers_dict

    response = session.get(url + fundcode + ".js?_=" + str(datetime.datetime.now().timetuple()))
    if response.status_code != 200:
        return None
    return response.content


#######################
# 获取指定基金编码的基金详情
#######################
def get_fund_detail(fundcode, share):
    # 获取基金详情，这里获取到的是jsonp结构的数据
    jsonp_content = get_fund_details(fundcode)
    if jsonp_content is None:
        return None
    # 将jsonp结构数据转换为json字符串
    fund_details_json_str = jsonp_to_json(jsonp_content)
    # 将基金详情转换为json对象
    funds_json = json.loads(fund_details_json_str)
    funds_json["share"] = share
    # 将json对象转换为python中基金Fund对象方便后续处理
    return fund.Fund(funds_json["fundcode"], funds_json["name"], funds_json["gsz"], funds_json["gztime"],
                     funds_json["dwjz"], funds_json["jzrq"], funds_json["gszzl"], funds_json["share"])


# 请求并解析得到所有买入基金数据的dict key为基金的code value为基金详情对象
def get_fund_dict(codes=file_helper.read_properties_to_dict("myfund.properties")):
    fund_dict = {}
    # 遍历要查询的所有基金
    for k, v in codes.items():
        retry_times = 0
        fund_detail = get_fund_detail(k, v)
        # 重试两次以后还是为空，跳过当前基金取下一个基金详情信息
        while fund_detail is None and retry_times < 2:
            retry_times = retry_times + 1
            fund_detail = get_fund_detail(k, v)
        if fund_detail is None:
            continue
        fund_dict[k] = fund_detail
    return fund_dict


#############################
# 获取基金编码和基金名称的映射关系
#############################
def get_code_name_dict(fund_dict):
    code_name_dict = {}
    for k, v in fund_dict.items():
        code_name_dict[k] = v.name
    return code_name_dict
