# 将文件中内容读到dict中
def read_properties_to_dict(file_name):
    codes = {}
    f = open(file_name, "r")
    for line in f:
        # 忽略注释
        if line.startswith("#"):
            continue
        line = line.rstrip("\n")
        codes[line.split("=")[0]] = line.split("=")[1]
    f.close()
    return codes;


# 检索文件，替换指定键值
def set_properties_to_file(file_name, key, value, annotation):
    kv_dict = read_properties_to_dict(file_name);

    found = False;
    # 遍历文件所有行
    for k, v in kv_dict.items():
        # 找到以key开头的行，替换该行
        if k == key:
            found = True;
            break;
    if found:
        print(f"已找到需更新的键值：{key}-{value}，执行更新操作")
    else:
        print(f"未找到需更新的键值：{key}-{value}，已添加新的键值")
    kv_dict[key] = value
    write_dict_and_annotation_to_file(file_name, kv_dict, annotation)


# 遍历dict内容并写入文件
def write_dict_to_file(file_name, kv_dict):
    write_dict_and_annotation_to_file(file_name, kv_dict, None)


def write_dict_and_annotation_to_file(file_name, kv_dict, annotation):
    f_w = open(file_name, "w", encoding='utf-8')
    for k, v in kv_dict.items():
        if annotation:
            if k in annotation:
                f_w.write("# " + annotation[k] + "\n")
        f_w.write(k + "=" + v + "\n")
    f_w.close()
