from os import remove
from shutil import move
from tempfile import mkstemp

from fund_tracker.pojo import fund_properties


def replace_kv_properties(file_name, key, value):
    """
    替换文件中指定键值
    :param file_name: 文件名称
    :param key: 键
    :param value: 值
    :return:
    """
    # 创建临时文件
    fh, abs_path = mkstemp()

    with open(file_name, "r") as f_r, open(fh, "w") as new_file:
        for line in f_r:
            if key + "=" in line:
                line = key + "=" + value + "\n"
            new_file.write(line)
    remove(file_name)
    move(abs_path, file_name)


def read_properties_to_dict(file_name):
    """
    将文件读取到dict中
    :param file_name: 文件名称
    :return: dict
    """
    codes = {}
    f = open(file_name, "r")
    for line in f:
        # 忽略注释
        if line.startswith("#") or line.strip() == '':
            continue
        line = line.rstrip("\n")
        codes[line.split("=")[0]] = line.split("=")[1]
    f.close()
    return codes


def write_fund_properties_to_file(file_name, fund_properties: fund_properties.FundProperties):
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
        f_w = open(file_name, "w", encoding='utf-8')
        f_w.write("# " + fund_properties.annotation + "\n")
        f_w.write(fund_properties.code + "=" + fund_properties.share + "\n")
        f_w.close()
