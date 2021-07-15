class Fund:
    # 基金编码
    code = "";
    # 基金名称
    name = "";
    # 基金实时净值
    current_value = "";
    # 实时净值更新时间
    current_time = "";
    # 上次更新净值
    last_value = "";
    # 上次净值更新日期
    last_time = "";
    # 净值估算
    value = "";
    # 份额
    share = "";
    # 实时估算总金额
    total_amount = ""

    def __init__(self, code, name, current_value, current_time, last_value, last_time, value, share):
        self.code = code;
        self.name = name;
        self.current_value = current_value;
        self.current_time = current_time;
        self.last_value = last_value;
        self.last_time = last_time;
        self.value = value;
        self.share = share;
        self.total_amount = str(round(float(current_value) * float(share), 2));

    def __str__(self):
        return '基金编码：%s,基金名称：%s,基金当前净值：%s,基金净值更新时间：%s,' \
               '基金上次净值：%s,基金上次净值更新时间：%s, 净值估算: %s, 买入份额：%s, 实时估算总金额: %s' % (
               self.code, self.name, self.current_value, self.current_time, self.last_value, self.last_time, self.value,
               self.share, self.total_amount)
