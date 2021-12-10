from dataclasses import dataclass


@dataclass
class FundProperties:
    """基金properties文件实体
    Attributes:
        code: 基金编码
        share: 基金购买份额
        annotation: 注释
    """
    code: str = ""
    share: str = ""
    annotation: str = ""

    def __str__(self):
        return '基金编码：%s,买入份额：%s, 注释: %s' % (
            self.code, self.share, self.annotation)
