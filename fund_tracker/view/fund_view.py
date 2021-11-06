from fund_tracker.pojo.fund import Fund


def fund_update_page():
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
                    <label>基金编码：</label><input type="text" name="fundcode" placeholder="请输入基金编码" maxlength="6">
                </div>
                <br />
                <div>
                    <label>基金份额：</label><input type="text" name="share" placeholder="份额为0时代表删除该基金">
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
    content = """
        <html>
            <header>
                <title>更新失败</title>
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
