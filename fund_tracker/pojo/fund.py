class Fund:
    """基金实体
    Attributes:
        code: 基金编码
        name: 基金名称
        current_value: 基金实时净值
        current_time: 基金净值更新时间
        last_value: 上次更新净值
        last_time: 上次净值更新日期
        value: 估算净值盈亏百分比
        share: 基金购买份额
        total_amount: 实时估算总金额
    """
    code = ""
    name = ""
    current_value = ""
    current_time = ""
    last_value = ""
    last_time = ""
    value = ""
    share = ""
    total_amount = ""

    def __init__(self, code, name, current_value, current_time, last_value, last_time, value, share):
        self.code = code
        self.name = name
        self.current_value = current_value
        self.current_time = current_time
        self.last_value = last_value
        self.last_time = last_time
        self.value = value
        self.share = share
        self.total_amount = str(round(float(current_value) * float(share), 2))

    def __str__(self):
        return '基金编码：%s,基金名称：%s,基金当前净值：%s,基金净值更新时间：%s,' \
               '基金上次净值：%s,基金上次净值更新时间：%s, 净值估算: %s, 买入份额：%s, 实时估算总金额: %s' % (
                   self.code, self.name, self.current_value, self.current_time, self.last_value, self.last_time,
                   self.value,
                   self.share, self.total_amount)
