from os import remove
from shutil import move
from tempfile import mkstemp

from fund_tracker.pojo import fund_properties
from fund_tracker.pojo.fund_properties import FundProperties


def replace_kv_properties(file_name: str, key: str, value: str):
    """
    替换文件中指定键值
    :param file_name: 文件名称
    :param key: 键
    :param value: 值
    :return:
    """
    # 创建临时文件
    fh, abs_path = mkstemp()

    with open(file_name, "r", encoding="utf-8") as f_r, open(fh, "w", encoding="utf-8") as new_file:
        for line in f_r:
            if key + "=" in line:
                line = key + "=" + value + "\n"
            new_file.write(line)
    remove(file_name)
    move(abs_path, file_name)


def read_properties_to_dict(file_name: str):
    """
    将文件读取到dict中
    :param file_name: 文件名称
    :return: dict
    """
    codes = {}
    try:
        f = open(file_name, "r", encoding="utf-8")
        for line in f:
            # 忽略注释
            if line.startswith("#") or line.strip() == '':
                continue
            line = line.rstrip("\n")
            codes[line.split("=")[0]] = line.split("=")[1]
        f.close()
    except FileNotFoundError:
        open(file_name, "w", encoding="utf-8")
    return codes


def read_properties_to_list(file_name: str):
    """
    将文件所有基金读取到list中
    :param file_name: 文件名称
    :return: fund
    """
    fund_list = []
    f = open(file_name, "r", encoding="utf-8")

    fund = None
    for line in f:
        if line.startswith("#"):
            fund = FundProperties()
            fund.annotation = line
            continue
        line = line.rstrip("\n")
        fund.code = line.split("=")[0]
        fund.share = line.split("=")[1]
        fund_list.append(fund)
    f.close()
    return fund_list


def write_fund_properties_to_file(file_name: str, fund_properties: fund_properties.FundProperties):
    """
    将基金配置对象写入指定文件
    :param file_name: 文件名称
    :param fund_properties: 基金配置对象
    :return:
    """
    # 将文件读取到dict
    kv_dict = read_properties_to_dict(file_name)

    # 是否在文件中找到指定的key
    found = False
    # 遍历所有键值，已有的键值执行更新，没有的键值执行新增
    for k, v in kv_dict.items():
        if k == fund_properties.code:
            found = True
            break

    if found:
        print(f"已找到需更新的键值：{fund_properties.code}-{fund_properties.share}，即将执行更新操作")
        replace_kv_properties(file_name, fund_properties.code, fund_properties.share)
    else:
        print(f"未找到需更新的键值：{fund_properties.code}-{fund_properties.share}，即将添加新的键值")
        f_w = open(file_name, "a", encoding="utf-8")
        f_w.write("# " + fund_properties.annotation + "\n")
        f_w.write(fund_properties.code + "=" + fund_properties.share + "\n")
        f_w.close()


def remove_fund_properties_from_file(file_name: str, code: str):
    """
    删除指定文件的基金
    :param code: 基金编码
    :param file_name: 文件名称
    :return:
    """

    fund_list = read_properties_to_list(file_name)
    rm_index = -1
    for i in range(len(fund_list)):
        if fund_list[i].code == code:
            rm_index = i
    if rm_index != -1:
        fund_list.pop(rm_index)

    # 创建临时文件
    fh, abs_path = mkstemp()
    with open(fh, "w") as new_file:
        for fund in fund_list:
            new_file.write(fund.annotation)
            line = fund.code + "=" + fund.share + "\n"
            new_file.write(line)
    remove(file_name)
    move(abs_path, file_name)
