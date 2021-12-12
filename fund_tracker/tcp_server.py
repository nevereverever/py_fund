import socket
from threading import Thread
from fund_tracker.service import fund_search
from fund_tracker.utils import file_helper
from fund_tracker.pojo.fund_properties import FundProperties
from fund_tracker.pojo.request import Request
from fund_tracker.view import fund_view
import hashlib

# 用户文件
user_file_name = "user.properties"
# 用户数据
file_dir = "fund_data/"
file_name = ".properties"
cookie_dict = {}


def handle_client(c_socket: socket):
    """
    处理客户端请求
    :param c_socket
    :return:
    """
    request_data = c_socket.recv(1024)
    request_data_json_str = request_data.decode()
    request = Request.analyse_request(Request(), request_data_json_str)

    # 非登录请求且Cookie为空，需要跳转登录
    if request.url.startswith("/login") is False and "Cookie" not in request.request_header_params:
        login_page(c_socket)
        return

    # 目前暂时只处理GET方法的请求
    if request.method == "GET":
        router_handler(c_socket, request)
    else:
        print("暂未实现")


def router_handler(c_socket: socket, request: Request):
    """
    地址路由处理器
    :param c_socket:
    :param request: 请求对象
    :return:
    """
    # 处理登录请求
    if request.url.startswith("/login"):
        request_params = request.url.split("/login")[1:]
        login(c_socket, request_params[0])
        return

    # 非登录的权限需要进行鉴权
    try:
        cookie = request.request_header_params["Cookie"].split("; ")[1].split("=")[1]
    except Exception:
        login_page(c_socket)
        return
    if login_handler(cookie) is False:
        login_page(c_socket)
        return
    current_login_user = get_login_user(cookie)
    if request.url == "/list":
        refund_list(c_socket, current_login_user)
    elif request.url.startswith("/updateFund"):
        refund_update_page(c_socket, current_login_user)
    elif request.url.startswith("/deleteFund"):
        request_params = request.url.split("/deleteFund")[1:]
        refund_delete(c_socket, current_login_user, request_params[0])
    elif request.url.startswith("/update"):
        # 获取update后的请求参数
        request_params = request.url.split("/update")[1:]
        refund_update(c_socket, current_login_user, request_params[0])
    elif request.url.startswith("/logout"):
        logout(c_socket, cookie)


def refund_list(client_socket: socket, current_login_user: str):
    """
    获取基金列表
    :param client_socket:
    :param current_login_user: 当前登录用户
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
                    <button onclick="logout()">登出</button>
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
    codes = file_helper.read_properties_to_dict(file_dir + current_login_user + file_name)
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
        
        function logout() {
            const url = "http://"+hostAndPort+"/logout"
            const request = new XMLHttpRequest();
            request.onload = function() {
                if (request.status == 200) {
                    alert("退出登录");
                    window.location.reload();
                }
            }
            request.open("GET", url);
            request.send(null);
        }
    </script>
    """

    # 向客户端返回响应数据
    client_socket.send(bytes(response_body + content, "gbk"))
    # 关闭客户端连接
    client_socket.close()


def save_fund(current_login_user: str, fundcode: str, share: str):
    """
    保存并返回基金对象
    :param current_login_user
    :param fundcode: 基金编码
    :param share: 基金净值
    :return:
    """
    fund = fund_search.get_fund_detail(fundcode, share)
    if fund is None:
        raise Exception("未成功获取到基金详情，基金库中可能尚未维护该基金！")
    else:
        fund_properties = FundProperties(fund.code, fund.share, fund.name)
        file_helper.write_fund_properties_to_file(file_dir + current_login_user + file_name, fund_properties)
        return fund


def login(client_socket: socket, request_params: str):
    """
    登录方法
    :param client_socket:
    :param request_params:
    :return:
    """
    username = ""
    password = ""
    request_params = request_params.split("?")[1]
    # 解析请求参数
    request_param_arr = request_params.split("&")
    for param in request_param_arr:
        param_arr = param.split("=")
        param_name = param_arr[0]
        if param_name == "username":
            username = param_arr[1]
        elif param_name == "password":
            password = param_arr[1]
        else:
            print("错误的参数，忽略")

    users = file_helper.read_properties_to_dict(user_file_name)
    if username in users:
        if password == users[username]:
            cookie = get_cookie(username, password)
            # 构造响应数据
            response_start_line = "HTTP/1.1 302 JUMP\r\n"
            response_headers = "Server: My server\r\n"
            response_headers += "Set-Cookie: JSESSIONID={}; HttpOnly\r\n".format(cookie)
            response_headers += "Location: {}\r\n".format("/list")
            response_body = response_start_line + response_headers + "\r\n"
            # 向客户端返回响应数据
            client_socket.send(bytes(response_body + "登录成功", "gbk"))
            # 用户登录成功后放入缓存
            global cookie_dict
            cookie_dict[cookie] = username
            # 关闭客户端连接
            client_socket.close()
        else:
            # 构造响应数据
            response_start_line = "HTTP/1.1 500 ERROR\r\n"
            response_headers = "Server: My server\r\n"
            response_body = response_start_line + response_headers + "\r\n"
            # 向客户端返回响应数据
            client_socket.send(bytes(response_body + "登录失败，密码错误", "gbk"))
            # 关闭客户端连接
            client_socket.close()
    else:
        # 构造响应数据
        response_start_line = "HTTP/1.1 500 ERROR\r\n"
        response_headers = "Server: My server\r\n"
        response_body = response_start_line + response_headers + "\r\n"
        # 向客户端返回响应数据
        client_socket.send(bytes(response_body + "无此账号", "gbk"))
        # 关闭客户端连接
        client_socket.close()


def logout(client_socket: socket, cookie: str):
    """
    移除cookie
    :param client_socket:
    :param cookie:
    :return:
    """
    if cookie in cookie_dict:
        del cookie_dict[cookie]

    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: My server\r\n"
    response_headers += "Set-Cookie: \r\n"
    response_body = response_start_line + response_headers + "\r\n"

    # 向客户端返回响应数据
    client_socket.send(bytes(response_body + "用户已退出", "gbk"))
    # 关闭客户端连接
    client_socket.close()


def login_handler(cookie: str):
    """
    登录拦截器
    :param cookie: cookie
    :return: 是否登录成功
    """
    if len(cookie) == 0:
        return False
    global cookie_dict
    return cookie in cookie_dict


def get_cookie(username: str, password: str):
    """
    获取cookie信息
    :param username: 用户名
    :param password: 密码
    :return:
    """
    md5 = hashlib.md5()
    md5.update(bytes(username + password, "utf-8"))
    return md5.hexdigest()


def get_login_user(cookie: str):
    global cookie_dict
    if cookie in cookie_dict:
        return cookie_dict[cookie]
    return None


def refund_update(client_socket: socket, current_login_user: str, request_params: str):
    """
    修改基金净值方法
    :param client_socket:
    :param current_login_user: 当前登录用户
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
            fund = save_fund(current_login_user, fundcode, share)
            content = fund_view.update_success_page(fund)
        except Exception as e:
            content = fund_view.update_failed_page(str(e))

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


def refund_delete(client_socket: socket, current_login_user: str, request_params: str):
    """
    基金删除方法
    :param client_socket:
    :param current_login_user: 当前登录用户
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
    file_helper.remove_fund_properties_from_file(file_dir + current_login_user + file_name, fundcode)
    # 构造响应数据
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: My server\r\n"
    response_body = response_start_line + response_headers + "\r\n"
    # 向客户端返回响应数据
    client_socket.send(bytes(response_body, "gbk"))
    # 关闭客户端连接
    client_socket.close()


def login_page(client_socket: socket):
    """
    登录界面请求
    :param client_socket:
    :return:
    """
    # 构造响应数据
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: My server\r\n"
    response_body = response_start_line + response_headers + "\r\n"
    # 构造html内容
    content = fund_view.login_page()

    # 向客户端返回响应数据
    client_socket.send(bytes(response_body + content, "gbk"))
    # 关闭客户端连接
    client_socket.close()


def refund_update_page(client_socket: socket, current_login_user: str):
    """
    基金修改页面
    :param client_socket:
    :param current_login_user: 当前登录用户
    :return:
    """
    # 构造响应数据
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: My server\r\n"
    response_body = response_start_line + response_headers + "\r\n"
    # 构造html内容
    content = fund_view.fund_update_page(current_login_user)

    # 向客户端返回响应数据
    client_socket.send(bytes(response_body + content, "gbk"))
    # 关闭客户端连接
    client_socket.close()


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", 8000))
    server_socket.listen(128)

    while True:
        c_socket, client_address = server_socket.accept()
        thread = Thread(target=handle_client, args=(c_socket,))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()
