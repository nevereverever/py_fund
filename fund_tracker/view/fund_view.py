from fund_tracker.pojo.fund import Fund


def login_page():
    """
    登录页面
    :return:
    """
    content = """
    <html lang="en">  
        <head>  
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no">
            <title>Login</title>  
            <style type="text/css">
                html{   
                    width: 100%;   
                    height: 100%;   
                    overflow: hidden;   
                    font-style: sans-serif;   
                }   
                body{   
                    width: 100%;   
                    height: 100%;   
                    font-family: 'Open Sans',sans-serif;   
                    margin: 0;   
                    background-color: #4A374A;   
                }   
                #login{   
                    position: absolute;   
                    top: 50%;   
                    left:50%;   
                    margin: -150px 0 0 -150px;   
                    width: 300px;   
                    height: 300px;   
                }   
                #login h1{   
                    color: #fff;   
                    text-shadow:0 0 10px;   
                    letter-spacing: 1px;   
                    text-align: center;   
                }   
                h1{   
                    font-size: 2em;   
                    margin: 0.67em 0;   
                }   
                input{   
                    width: 278px;
                    margin-bottom: 10px;   
                    outline: none;   
                    padding: 10px;   
                    font-size: 13px;   
                    color: #fff;   
                    text-shadow:1px 1px 1px;   
                    border-top: 1px solid #312E3D;   
                    border-left: 1px solid #312E3D;   
                    border-right: 1px solid #312E3D;   
                    border-bottom: 1px solid #56536A;   
                    border-radius: 4px;   
                    background-color: #2D2D3F;   
                }   
                .but{   
                    width: 300px;   
                    min-height: 20px;   
                    display: block;   
                    background-color: #4a77d4;   
                    border: 1px solid #3762bc;   
                    color: #fff;   
                    padding: 9px 14px;   
                    font-size: 15px;   
                    line-height: normal;   
                    border-radius: 5px;   
                    margin: 0;   
                }  
            </style>
        </head>  
        <body>  
            <div id="login">  
                <h1>搞基网</h1>  
                <form method="post" action="login">
                    <input type="text" required="required" placeholder="用户名" name="username"></input>  
                    <input type="password" required="required" placeholder="密码" name="password"></input>  
                    <button class="but" type="submit">登录</button>  
                </form>  
            </div>  
        </body>  
    </html>
    """
    return content


def fund_list(fund_dict: dict):
    """
    基金列表
    :param fund_dict:
    :return:
    """
    content = """
    <html>
        <head>
            <meta charset="UTF-8">
            <title>基金</title>
            <style type="text/css">
                table {
                    border-collapse: collapse;
                    margin: 0 auto;
                    text-align: center;
                }
                table td, table th {
                    border: 1px solid #cad9ea;
                    color: #666;
                    height: 30px;
                }
                table thead th {
                    background-color: #CCE8EB;
                    width: 100px;
                }
                table tr:nth-child(odd) {
                    background: #fff;
                }
                table tr:nth-child(even) {
                    background: #F5FAFA;
                }
            </style>
        </head>
        <body>
            <div style="display: flex;justify-content: center;">
                <div>
                    <div style="display: inline-block;margin-bottom: 5px;">
                        <button onclick="javascript: start_stop_fresh()">开始/停止刷新</button>
                        <button onclick="javascript: window.location.reload()">手动刷新</button>
                        <button onclick="update_fund()">基金份额更新</button>
                        <button onclick="logout()">登出</button>
                    </div>
                    
                    <table id="fund-table" border="1px">
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
    today_income = 0.0
    # 遍历拼接每行数据
    for v in fund_dict.values():
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
        </table>
    <div id="sum" style="float:left">
    """

    if today_income > 0.0:
        content += "<b style='color:red'>"
    else:
        content += "<b style='color:green'>"

    content += "本日总收入：" + str(round(today_income, 2)) + "</b></div></div></body></div></html>"

    content += """
    <script>
        var hostAndPort = document.location.host;
        function update_fund(){
            window.open("http://"+hostAndPort+"/update","_blank");
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
            request.open("post", url);
            request.send(null);
        }
    </script>
    """
    return content


def fund_update_page(current_login_user):
    """
    基金净值更新页面
    :return:
    """
    content = """
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no">
            <title>基金更新(
    """
    content += current_login_user
    content += """)</title>
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
        </head>
        <body>
            <form action="update" method="post">
            <div>
                <div>
                    <label>基金编码：</label><input type="text" name="fundcode" placeholder="请输入基金编码" maxlength="6">
                </div>
                <br />
                <div>
                    <label>基金份额：</label><input type="text" name="share" placeholder="请输入基金份额">
                </div>
                
                <div>
                    <input type="submit" class="ant-btn ant-btn-red" value="提交">
                </div>
            </div>
            </form>
        </body>
    </html>        
    """
    return content


def update_success_page(fund: Fund):
    """
    构建修改成功的页面
    :param fund:
    :return:
    """
    # 构造html内容
    content = """
        <html>
            <head>
                <meta charset="UTF-8">
                <title>更新成功</title>
            </head>
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
                <p>已成功更新基金份额，基金名称(name)为:
                """

    content += fund.name + "，基金编码(fundcode)为：" + fund.code + "，份额(share)为：" + fund.share + "</p>"
    content += """
                <input type="button" class="ant-btn ant-btn-red" onclick="javascript:history.back(-1)" value="返回"></button>
            </body>
        </html>
        """
    return content


def update_failed_page(reason: str):
    """
    修改失败页面
    :param reason:
    :return:
    """
    content = """
        <html>
            <head>
                <meta charset="UTF-8">
                <title>更新失败</title>
            </head>
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
                <h3>更新失败</h3>
                <p>
                """
    content += reason + "</p>"
    content += """
                <input type="button" class="ant-btn ant-btn-red" onclick="javascript:history.back(-1)" value="返回"></button>
            </body>
        </html>
        """
    return content


def un_support_method_page(method: str):
    """
    不支持的请求类型
    :param method:
    :return:
    """
    content = """
        <html>
            <head>
                <meta charset="UTF-8">
                <title>操作失败</title>
            </head>
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
                <h3>操作失败</h3>
                <p>不支持的请求类型：
                """
    content += method + "</p>"
    content += """
                <input type="button" class="ant-btn ant-btn-red" onclick="javascript:history.back(-1)" value="返回"></button>
            </body>
        </html>
        """
    return content


def error_msg_page(error_msg: str):
    """
    不支持的请求类型
    :param error_msg
    :return:
    """
    content = """
        <html>
            <head>
                <meta charset="UTF-8">
                <title>出错了</title>
            </head>
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
                <h3>出错了</h3>
                <p>：
                """
    content += error_msg + "</p>"
    content += """
                <input type="button" class="ant-btn ant-btn-red" onclick="javascript:history.back(-1)" value="返回"></button>
            </body>
        </html>
        """
    return content
