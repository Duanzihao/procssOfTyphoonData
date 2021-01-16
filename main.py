import json
import datetime
import os
import re

if __name__ == '__main__':
    os.mkdir('./data')
    print("根目录datd创建完成\n")
    dir_path = "./CMABSTdata"  # 文件夹目录
    files = os.listdir(dir_path)  # 得到文件夹下的所有文件名称
    for file in files:
        # print(file)
        # 这里首先要创建相应年份的文件夹
        read_file = open(dir_path + "/" + file, "r")
        year = re.findall(r"\d+", file)
        dir_year = "./data/" + year[0]
        os.mkdir(dir_year)
        print("文件夹" + dir_year + "创建完成\n")
        lines = read_file.readlines()
        index = 0
        content_flag = 0
        content = {}
        point_list = []
        name = ''
        target_file = ''
        for line in lines:
            separate_data = line.split(' ')
            raw_separate_data = separate_data
            # 清除separate_data中间空的字符串，防止按位读取数据出现错误
            separate_data = [i for i in separate_data if i != '']
            if separate_data[0] == '66666':
                # 如果字典为空，说明内容还没被写入，此时需要将内容写到字典中
                if not content:
                    name = separate_data[7].split('\t')[0]
                    if raw_separate_data[9] == '':
                        name = "(nameless)"
                    new_file_name = dir_year + "/" + name + ".json"
                    target_file = open(new_file_name, "w+")
                    content["name"] = separate_data[7]
                    continue
                else:
                    content["rows"] = point_list
                    # 这里需要进行将字典转换为JSON再写入文件的操作
                    # 这里的dump会直接将dict转为json，并写入文件
                    json.dump(content, target_file)
                    print(target_file.name + "已经写好\n")
                    # 将之前的内容置空
                    content = {}
                    point_list = []
                    name = separate_data[7].split('\t')[0]
                    # 在调试的过程中发现，1994年的数据有奇怪的台风是没有名字的，就在Seth台风的下面一个，
                    # 所以这个时候需要手动加一个无名上去
                    if raw_separate_data[9] == '':
                        name = "(nameless)"
                    new_file_name = dir_year + "/" + name + ".json"
                    target_file = open(new_file_name, "w+")
                    content["name"] = separate_data[7]
                    continue
            # 这里就是对具体的信息进行处理
            else:
                point = {
                    "time": str(datetime.datetime.strptime(separate_data[0], "%Y%m%d%H")),
                    "power": int(separate_data[1]),
                    "lat": float(separate_data[2]) / 10,
                    "lng": float(separate_data[3]) / 10,
                    "PRES": float(separate_data[4]),
                    "WND": float(separate_data[5].split('\n')[0])
                }
                point_list.append(point)
        # 当进行过所有的for循环过后，应该还会剩余一个文件没有写入到json中，这个时候需要手动写入到json
        content["rows"] = point_list
        # 这里需要进行将字典转换为JSON再写入文件的操作
        json_content = json.dumps(content)
        json.dump(json_content, target_file)
