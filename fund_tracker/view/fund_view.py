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
                    height: 18px;   
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
                <h1>Login</h1>  
                <form method="get" action="login">  
                    <input type="text" required="required" placeholder="UserName" name="username"></input>  
                    <input type="password" required="required" placeholder="Password" name="password"></input>  
                    <button class="but" type="submit">Login</button>  
                </form>  
            </div>  
        </body>  
    </html>
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
            <form action="update" method="GET">
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
