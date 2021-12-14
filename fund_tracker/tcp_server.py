import socket
from datetime import datetime, timedelta
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
    elif request.method == "POST":
        router_handler(c_socket, request)


def router_handler(c_socket: socket, request: Request):
    """
    地址路由处理器
    :param c_socket:
    :param request: 请求对象
    :return:
    """
    # 处理登录请求
    if request.url.startswith("/login"):
        if request.method == "POST":
            login(c_socket, request.request_body_params)
            return
        else:
            success_200_response(c_socket, fund_view.un_support_method_page(request.method))
            return

    # 非登录的权限需要进行鉴权
    try:
        cookie = request.request_header_params["Cookie"].split("=")[1]
    except Exception:
        login_page(c_socket)
        return
    # 登录拦截
    if login_handler(cookie) is False:
        login_page(c_socket)
        return
    # 从cookie获取登录用户
    current_login_user = get_login_user(cookie)
    if request.url == "/" or request.url == "/list":
        refund_list(c_socket, current_login_user)
    elif request.url.startswith("/deleteFund"):
        if request.method == "POST":
            refund_delete(c_socket, current_login_user, request.request_body_params)
        else:
            success_200_response(c_socket, fund_view.un_support_method_page(request.method))
    elif request.url.startswith("/update"):
        if request.method == "GET":
            refund_update_page(c_socket, current_login_user)
        elif request.method == "POST":
            refund_update(c_socket, current_login_user, request.request_body_params)
    elif request.url.startswith("/logout"):
        logout(c_socket)


def refund_list(client_socket: socket, current_login_user: str):
    """
    获取基金列表
    :param client_socket:
    :param current_login_user: 当前登录用户
    :return:
    """
    codes = file_helper.read_properties_to_dict(file_dir + current_login_user + file_name)
    fund_dict = fund_search.get_fund_dict(codes)
    success_200_response(client_socket, fund_view.fund_list(fund_dict))


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


def login(client_socket: socket, request_body_params: dict):
    """
    登录方法
    :param client_socket:
    :param request_body_params:
    :return:
    """
    username = request_body_params.get("username")
    password = request_body_params.get("password")

    if username is None or password is None:
        error_500_response(client_socket, fund_view.error_msg_page("用户名/密码不可为空！"))

    users = file_helper.read_properties_to_dict(user_file_name)
    if username in users:
        if password == users[username]:
            cookie = get_cookie(username, password)
            # 构造响应数据
            response_start_line = "HTTP/1.1 302 JUMP\r\n"
            response_headers = "Server: My server\r\n"
            expire_time = (datetime.now() + timedelta(hours=1)).strftime("%a, %d %b %Y %H:%M:%S GMT")
            response_headers += "Set-Cookie: JSESSIONID={}; expire={}; Max-Age={}; HttpOnly\r\n"\
                .format(cookie, expire_time, 3600)
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
            error_500_response(client_socket, fund_view.error_msg_page("登录失败，密码错误！"))
    else:
        error_500_response(client_socket, fund_view.error_msg_page("用户库无此账号，请联系管理员"))


def logout(client_socket: socket):
    """
    移除cookie
    :param client_socket:
    :return:
    """
    # if cookie in cookie_dict:
    #     del cookie_dict[cookie]

    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: My server\r\n"
    expire_time = (datetime.now() + timedelta(hours=-1)).strftime("%a, %d %b %Y %H:%M:%S GMT")
    response_headers += "Set-Cookie: JSESSIONID={}; expire={}; HttpOnly\r\n" \
        .format("", expire_time)
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
    """
    获取当前登录用户
    :param cookie: cookie
    :return:
    """
    global cookie_dict
    return cookie_dict.get(cookie)


def refund_update(client_socket: socket, current_login_user: str, request_body_params: dict):
    """
    修改基金净值方法
    :param request_body_params:
    :param client_socket:
    :param current_login_user: 当前登录用户
    :return:
    """
    fundcode = request_body_params.get("fundcode")
    share = request_body_params.get("share")

    if fundcode is None and share is None:
        success_200_response(client_socket, fund_view.update_failed_page("未成功更新基金份额，基金编码或份额不可为空！"))
        return

    # 获取基金配置对象，并写入配置文件
    try:
        fund = save_fund(current_login_user, fundcode, share)
        content = fund_view.update_success_page(fund)
    except Exception as e:
        content = fund_view.update_failed_page(str(e))

    success_200_response(client_socket, content)


def refund_delete(client_socket: socket, current_login_user: str, request_params: dict):
    """
    基金删除方法
    :param client_socket:
    :param current_login_user: 当前登录用户
    :param request_params: 请求参数
    :return:
    """
    fundcode = request_params.get("fundcode")
    file_helper.remove_fund_properties_from_file(file_dir + current_login_user + file_name, fundcode)
    success_200_response(client_socket, "")


def login_page(client_socket: socket):
    """
    登录界面请求
    :param client_socket:
    :return:
    """
    success_200_response(client_socket, fund_view.login_page())


def refund_update_page(client_socket: socket, current_login_user: str):
    """
    基金修改页面
    :param client_socket:
    :param current_login_user: 当前登录用户
    :return:
    """
    success_200_response(client_socket, fund_view.fund_update_page(current_login_user))


def success_200_response(client_socket: socket, content: str):
    """
    200响应
    :param client_socket:
    :param content:
    :return:
    """
    # 构造响应数据
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: My server\r\n"
    response_body = response_start_line + response_headers + "\r\n"
    # 向客户端返回响应数据
    client_socket.send(bytes(response_body + content, "utf-8"))
    # 关闭客户端连接
    client_socket.close()


def error_500_response(client_socket: socket, content: str):
    """
    500响应
    :param client_socket:
    :param content:
    :return:
    """
    # 构造响应数据
    response_start_line = "HTTP/1.1 500 ERROR\r\n"
    response_headers = "Server: My server\r\n"
    response_body = response_start_line + response_headers + "\r\n"
    # 向客户端返回响应数据
    client_socket.send(bytes(response_body + content, "utf-8"))
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
