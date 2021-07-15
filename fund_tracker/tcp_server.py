import socket
from fund_tracker import fund_search
from fund_tracker import file_helper
from multiprocessing import Process

file_name = "myfund.properties"


def refund_list(client_socket):
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
                            <td>上次净值更新日期</td>
                            <td>上次净值</td>
                            <td>实时净值</td>
                            <td>净值更新时间</td>
                            <td>净值估算</td>
                            <td>买入份额</td>
                            <td>实时估算总金额</td>
                            <td>估算盈亏</td>
                        </tr>
                    </thead>
                    <tbody>
    """
    # 今日收入
    today_income = 0.0
    fund_dict = fund_search.get_fund_dict()
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
        content += str(current_fund_income) + "</b></td></tr>"
    content += """</tbody>
    </table><div id="sum" style="float:left">"""

    if today_income > 0.0:
        content += "<b style='color:red'>"
    else:
        content += "<b style='color:green'>"

    content += "本日总收入：" + str(round(today_income, 2)) + "</b></div></div></body></html>"

    content += """
    <script>
        var hostAndPort=document.location.host;
        function update_fund(){
            window.open("http://"+hostAndPort+"/updateFund","_blank");
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


def refund_update(client_socket, request_params):
    fundcode = ""
    share = ""
    request_params = request_params.split("?")[1]
    print(f"请求参数为：{request_params}")
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
        annotation = fund_search.get_code_name_dict(fund_search.get_fund_dict())
        file_helper.set_properties_to_file(file_name, fundcode, share, annotation)

    # 构造响应数据
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: My server\r\n"
    response_body = response_start_line + response_headers + "\r\n"
    # 构造html内容
    content = """
    <html>
        <header>
            <title>更新成功</title>
        </header>
        <style type="text/css">
                        .ant-btn {
                            line-height: 1.499;
                            position: relative;
                            display: inline-block;
                            font-weight: 400;
                            white-space: nowrap;
                            text-align: center;
                            background-image: none;
                            border: 1px solid transparent;
                            -webkit-box-shadow: 0 2px 0 rgba(0,0,0,0.015);
                            box-shadow: 0 2px 0 rgba(0,0,0,0.015);
                            cursor: pointer;
                            -webkit-transition: all .3s cubic-bezier(.645, .045, .355, 1);
                            transition: all .3s cubic-bezier(.645, .045, .355, 1);
                            -webkit-user-select: none;
                            -moz-user-select: none;
                            -ms-user-select: none;
                            user-select: none;
                            -ms-touch-action: manipulation;
                            touch-action: manipulation;
                            height: 32px;
                            padding: 0 15px;
                            font-size: 14px;
                            border-radius: 4px;
                            color: rgba(0,0,0,0.65);
                            background-color: #fff;
                            border-color: #d9d9d9;
                        }
                        
                        .ant-btn-primary {
                            color: #fff;
                            background-color: #1890ff;
                            border-color: #1890ff;
                            text-shadow: 0 -1px 0 rgba(0,0,0,0.12);
                            -webkit-box-shadow: 0 2px 0 rgba(0,0,0,0.045);
                            box-shadow: 0 2px 0 rgba(0,0,0,0.045);
                        }
                        .ant-btn-red {
                            color: #fff;
                            background-color: #FF5A44;
                            border-color: #FF5A44;
                            text-shadow: 0 -1px 0 rgba(0,0,0,0.12);
                            -webkit-box-shadow: 0 2px 0 rgba(0,0,0,0.045);
                            box-shadow: 0 2px 0 rgba(0,0,0,0.045);
                        }
            </style>
        <body>
            <h3>更新成功</h3>
            <p>已成功更新基金份额，基金编码(fundcode)为：
            """

    content += fundcode + "，份额(share)为：" + share + "</p>"
    content += """
            <input type="button" class="ant-btn ant-btn-red" onclick="javascript:history.back(-1)" value="返回"></button>
        </body>
    </html>
    """
    # 向客户端返回响应数据
    client_socket.send(bytes(response_body + content, "gbk"))
    # 关闭客户端连接
    client_socket.close()


def refund_update_page(client_socket):
    # 构造响应数据
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: My server\r\n"
    response_body = response_start_line + response_headers + "\r\n"
    # 构造html内容
    content = """
    <html>
        <header>
            <title>基金更新</title>
            <style type="text/css">
                        .ant-btn {
                            line-height: 1.499;
                            position: relative;
                            display: inline-block;
                            font-weight: 400;
                            white-space: nowrap;
                            text-align: center;
                            background-image: none;
                            border: 1px solid transparent;
                            -webkit-box-shadow: 0 2px 0 rgba(0,0,0,0.015);
                            box-shadow: 0 2px 0 rgba(0,0,0,0.015);
                            cursor: pointer;
                            -webkit-transition: all .3s cubic-bezier(.645, .045, .355, 1);
                            transition: all .3s cubic-bezier(.645, .045, .355, 1);
                            -webkit-user-select: none;
                            -moz-user-select: none;
                            -ms-user-select: none;
                            user-select: none;
                            -ms-touch-action: manipulation;
                            touch-action: manipulation;
                            height: 32px;
                            padding: 0 15px;
                            font-size: 14px;
                            border-radius: 4px;
                            color: rgba(0,0,0,0.65);
                            background-color: #fff;
                            border-color: #d9d9d9;
                        }
                        
                        .ant-btn-primary {
                            color: #fff;
                            background-color: #1890ff;
                            border-color: #1890ff;
                            text-shadow: 0 -1px 0 rgba(0,0,0,0.12);
                            -webkit-box-shadow: 0 2px 0 rgba(0,0,0,0.045);
                            box-shadow: 0 2px 0 rgba(0,0,0,0.045);
                        }
                        .ant-btn-red {
                            color: #fff;
                            background-color: #FF5A44;
                            border-color: #FF5A44;
                            text-shadow: 0 -1px 0 rgba(0,0,0,0.12);
                            -webkit-box-shadow: 0 2px 0 rgba(0,0,0,0.045);
                            box-shadow: 0 2px 0 rgba(0,0,0,0.045);
                        }
            </style>
        </header>
        <body>
            <form action="update" method="GET">
            <div>
                <div>
                    <label>基金编码：</label><input type="text" name="fundcode">
                </div>
                <br />
                <div>
                    <label>基金份额：</label><input type="text" name="share">
                </div>
                <div>
                    <input type="submit" class="ant-btn ant-btn-red" value="提交">
                </div>
            </div>
            </form>
        </body>
    </html>        
    """

    # 向客户端返回响应数据
    client_socket.send(bytes(response_body + content, "gbk"))
    # 关闭客户端连接
    client_socket.close()


def router_handler(request_data_header_url, client_socket):
    if request_data_header_url == "/":
        refund_list(client_socket)
    elif request_data_header_url.startswith("/updateFund"):
        refund_update_page(client_socket)
    elif request_data_header_url.startswith("/update"):
        # 获取update后的请求参数
        request_params = request_data_header_url.split("/update")[1:]
        refund_update(client_socket, request_params[0])


def handle_client(client_socket):
    """
    处理客户端请求
    """
    request_data = client_socket.recv(1024)
    request_data_json_str = request_data.decode()

    # 解析客户端请求，获取并处理请求
    for line in request_data_json_str.split("\r\n"):
        if line.startswith("GET"):
            request_data_header = line.split(" ")
            # 获取请求路径，作路由处理
            request_data_header_url = request_data_header[1]
            router_handler(request_data_header_url, client_socket)
            break
        else:
            continue


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", 8000))
    server_socket.listen(128)

    while True:
        client_socket, client_address = server_socket.accept()
        handle_client_process = Process(target=handle_client, args=(client_socket,))
        handle_client_process.start()
        client_socket.close()
