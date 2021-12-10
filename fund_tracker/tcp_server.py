import socket
from fund_tracker.service import fund_search
from fund_tracker.utils import file_helper
from fund_tracker.pojo.fund_properties import FundProperties
from fund_tracker.view import fund_view
from multiprocessing import Process

# 基金份额文件
file_name = "myfund.properties"
client_socket = None


def refund_list():
    """
    获取基金列表
    :return:
    """
    # 构造响应数据
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: My server\r\n"
    response_body = response_start_line + response_headers + "\r\n"
    # 构造html内容
    content = """
    <html>
        <header>
            <title>基金</title>
        </header>
        <body>
            <div>
                <div>
                    <button onclick="javascript: start_stop_fresh()">开始/停止刷新</button>
                    <button onclick="javascript: window.location.reload()">手动刷新</button>
                    <button onclick="update_fund()">基金份额更新</button>
                </div>
                <table id="content" border="1px">
                    <thead>
                        <tr>
                            <td>基金编码</td>
                            <td>基金名称</td>
                            <td>上个交易日</td>
                            <td>上次净值</td>
                            <td>实时净值</td>
                            <td>净值更新时间</td>
                            <td>估算净值</td>
                            <td>买入份额</td>
                            <td>实时金额</td>
                            <td>估算盈亏</td>
                            <td>操作</td>
                        </tr>
                    </thead>
                    <tbody>
    """
    # 今日收入
    today_income = 0.0
    codes = file_helper.read_properties_to_dict(file_name)
    fund_dict = fund_search.get_fund_dict(codes)
    # 遍历拼接每行数据
    for k, v in fund_dict.items():
        # 收入大于0为红色，否则为绿色
        current_fund_income = round(float(v.value) * float(v.share) * float(v.current_value) / 100, 2)
        # 今日收入等于每个基金的估值*份额的累加
        today_income = today_income + current_fund_income
        content += "<tr id=" + v.code + "><td>" \
                   + v.code + "</td><td>" \
                   + v.name + "</td><td>" \
                   + v.last_time + "</td><td>" \
                   + v.last_value + "</td><td>" \
                   + v.current_value + "</td><td>" \
                   + v.current_time + "</td>"

        # 净值大于0为红色，否则为绿色
        if float(v.value) > 0.0:
            content += "<td><b style='color:red'>"
        else:
            content += "<td><b style='color:green'>"
        content += v.value + "</b></td>"
        content += "<td>" + v.share + "</td><td>" \
                   + v.total_amount + "</td>"

        if current_fund_income > 0.0:
            content += "<td><b style='color:red'>"
        else:
            content += "<td><b style='color:green'>"
        content += str(current_fund_income) + "</b></td><td><button onclick='del_fund(this)'>删除" + "</button></td></tr>"
    content += """</tbody>
    </table><div id="sum" style="float:left">"""

    if today_income > 0.0:
        content += "<b style='color:red'>"
    else:
        content += "<b style='color:green'>"

    content += "本日总收入：" + str(round(today_income, 2)) + "</b></div></div></body></html>"

    content += """
    <script>
        var hostAndPort = document.location.host;
        function update_fund(){
            window.open("http://"+hostAndPort+"/updateFund","_blank");
        }
        
        function del_fund(obj) {
            const fundcode = obj.parentNode.parentNode.id;
            const url = "http://"+hostAndPort+"/deleteFund?fundcode=" + fundcode
            const request = new XMLHttpRequest();
            request.onload = function() {
                if (request.status == 200) {
                    alert("删除成功");
                    obj.parentNode.parentNode.remove();
                }
            }
            request.open("GET", url);
            request.send(null);
        }
    
        var fresh = true;
        setTimeout(function (){
            console.log("定时任务开始");
            if (fresh) {
                console.log("刷新页面...");
                window.location.reload();
            }
        },60000);
        
        function start_stop_fresh () {
            fresh = !fresh;
            alert(fresh ? "开始自动刷新":"停止自动刷新");
            if (fresh) {
                setTimeout(function (){
                console.log("定时任务开始");
                if (fresh) {
                    console.log("刷新页面...");
                    window.location.reload();
                }
                },60000);
            }
        }
        
        
    </script>
    """

    # 向客户端返回响应数据
    client_socket.send(bytes(response_body + content, "gbk"))
    # 关闭客户端连接
    client_socket.close()


def save_fund(fundcode: str, share: str):
    """
    保存并返回基金对象
    :param fundcode: 基金编码
    :param share: 基金净值
    :return:
    """
    fund = fund_search.get_fund_detail(fundcode, share)
    if fund is None:
        raise Exception("未成功获取到基金详情，基金库中可能尚未维护该基金！")
    else:
        fund_properties = FundProperties(fund.code, fund.share, fund.name)
        file_helper.write_fund_properties_to_file(file_name, fund_properties)
        return fund


def refund_update(request_params: str):
    """
    修改基金净值方法
    :param request_params: 请求参数
    :return:
    """
    fundcode = ""
    share = ""
    request_params = request_params.split("?")[1]
    print(f"执行基金修改，请求参数为：{request_params}")
    # 解析请求参数
    request_param_arr = request_params.split("&")
    for param in request_param_arr:
        param_arr = param.split("=")
        param_name = param_arr[0]
        if param_name == "fundcode":
            fundcode = param_arr[1]
        elif param_name == "share":
            share = param_arr[1]
        else:
            print("错误的参数，忽略")

    if fundcode != '' and share != '':
        # 获取基金配置对象，并写入配置文件
        try:
            fund = save_fund(fundcode, share)
            content = fund_view.update_success_page(fund)
        except Exception as e:
            content = fund_view.update_failed_page(e)

        # 构造响应数据
        response_start_line = "HTTP/1.1 200 OK\r\n"
        response_headers = "Server: My server\r\n"
        response_body = response_start_line + response_headers + "\r\n"
        # 向客户端返回响应数据
        client_socket.send(bytes(response_body + content, "gbk"))
        # 关闭客户端连接
        client_socket.close()
    else:
        # 构造响应数据
        response_start_line = "HTTP/1.1 200 OK\r\n"
        response_headers = "Server: My server\r\n"
        response_body = response_start_line + response_headers + "\r\n"
        # 构造html内容
        content = fund_view.update_failed_page("未成功更新基金份额，基金编码或份额不可为空！")
        # 向客户端返回响应数据
        client_socket.send(bytes(response_body + content, "gbk"))
        # 关闭客户端连接
        client_socket.close()


def refund_delete(request_params: str):
    """
    基金删除方法
    :param request_params: 请求参数
    :return:
    """
    fundcode = ""
    request_params = request_params.split("?")[1]
    print(f"执行基金删除，请求参数为：{request_params}")
    # 解析请求参数
    request_param_arr = request_params.split("&")
    for param in request_param_arr:
        param_arr = param.split("=")
        param_name = param_arr[0]
        if param_name == "fundcode":
            fundcode = param_arr[1]
        else:
            print("错误的参数，忽略")
    file_helper.remove_fund_properties_from_file(file_name, fundcode)
    # 构造响应数据
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: My server\r\n"
    response_body = response_start_line + response_headers + "\r\n"
    # 向客户端返回响应数据
    client_socket.send(bytes(response_body, "gbk"))
    # 关闭客户端连接
    client_socket.close()


def refund_update_page():
    """
    基金修改页面
    :return:
    """
    # 构造响应数据
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: My server\r\n"
    response_body = response_start_line + response_headers + "\r\n"
    # 构造html内容
    content = fund_view.fund_update_page()

    # 向客户端返回响应数据
    client_socket.send(bytes(response_body + content, "gbk"))
    # 关闭客户端连接
    client_socket.close()


def router_handler(request_data_header_url: str):
    """
    地址路由处理器
    :param request_data_header_url: 请求路径
    :return:
    """
    if request_data_header_url == "/":
        refund_list()
    elif request_data_header_url.startswith("/updateFund"):
        refund_update_page()
    elif request_data_header_url.startswith("/deleteFund"):
        request_params = request_data_header_url.split("/deleteFund")[1:]
        refund_delete(request_params[0])
    elif request_data_header_url.startswith("/update"):
        # 获取update后的请求参数
        request_params = request_data_header_url.split("/update")[1:]
        refund_update(request_params[0])


def handle_client(c_socket: object):
    """
    处理客户端请求
    :return:
    """
    global client_socket
    client_socket = c_socket
    request_data = c_socket.recv(1024)
    request_data_json_str = request_data.decode()

    # 解析客户端请求，获取并处理请求
    for line in request_data_json_str.split("\r\n"):
        if line.startswith("GET"):
            request_data_header = line.split(" ")
            # 获取请求路径，作路由处理
            request_data_header_url = request_data_header[1]
            router_handler(request_data_header_url)
            break
        else:
            continue


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", 8000))
    server_socket.listen(128)

    while True:
        c_socket, client_address = server_socket.accept()
        handle_client_process = Process(target=handle_client, args=(c_socket,))
        handle_client_process.start()
        c_socket.close()
