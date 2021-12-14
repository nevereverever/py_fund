from dataclasses import dataclass


@dataclass
class Request:
    """基金properties文件实体
    Attributes:
        method: 请求方式
        url: 请求路径
        protocol: 协议版本
        request_header: 请求头
        request_header_params: 请求头参数
        request_body: 请求体
        request_body_params: 请求体参数
    """
    method: str = ""
    url: str = ""
    protocol: str = ""
    request_header: str = ""
    request_header_params = dict()
    request_body: str = ""
    request_body_params = dict()

    def analyse_request(self, request_str: str):
        if request_str is None:
            return self
        # 得到请求头和请求体
        self.request_header, self.request_body = request_str.split("\r\n\r\n")
        # 请求头解析
        request_header_list = self.request_header.split("\r\n")
        first_line = True
        for request_header in request_header_list:
            if first_line:
                # 从第1行获取到请求方式，请求路径和请求协议版本
                self.method, self.url, self.protocol = request_header.split(" ")
                first_line = False
                continue
            key = request_header.split(": ")[0]
            value = request_header.split(": ")[1]
            self.request_header_params[key] = value

        # 请求体非空需要进行解析
        if self.request_body.strip() != "":
            request_body_list = self.request_body.split("&")
            for request_body in request_body_list:
                key = request_body.split("=")[0]
                value = request_body.split("=")[1]
                self.request_body_params[key] = value

        return self
