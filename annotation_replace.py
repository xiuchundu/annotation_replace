# -*- coding:utf8 -*-

import re
import os
import shutil
import chardet


# 创建目录，存储文件，若目录存在则删除目录
def create_outpout_dir():
    cur_path = os.path.abspath(os.curdir)
    set_file_path = cur_path + "\\" + "output_file"
    folder = os.path.exists(set_file_path)
    if not folder:
        os.mkdir(set_file_path)
    else:
        print(set_file_path + " 目录已经存在!")
        try:
            shutil.rmtree(set_file_path)
            os.mkdir(set_file_path)
        except OSError:
            print("权限错误，请再运行一次!")
            pass


# 创建输出文件子目录，存储文件
def mk_sub_dir(sub_dir_path):
    cur_path = os.path.abspath(os.curdir)
    path = cur_path + "\\output_file"
    if len(sub_dir_path) > len(cur_path):
        path = sub_dir_path[len(cur_path):]
        sub_file_path = cur_path + "\\" + "output_file" + path
        folder = os.path.exists(sub_file_path)
        if not folder:
            os.makedirs(sub_file_path)  # 创建多层目录
        path = sub_file_path
    return path


# 将行首的tab键转化为四个空格
def tab_to_space(lines_array):
    for i, each_line in enumerate(lines_array):
        cnt = 0
        buffer = each_line.split("\t")
        if len(buffer) > 1:
            for each_buffer in buffer:
                if each_buffer == '':
                    cnt += 4
        lines_array[i] = string_to_space(cnt) + lines_array[i].replace("\t", "")    # 去除行首的tab键
    return lines_array


# 判断文件编码格式
def file_encoding(path_file, file_name):
    f_test = open(path_file + "/" + file_name, 'rb')
    data_test = f_test.read()
    return chardet.detect(data_test).get("encoding")


# 将空格转化为字符串空格
def string_to_space(number_space):
    cnt = 0
    str_space = ""
    while cnt < number_space:
        str_space += " "
        cnt += 1
    return str_space


# 单行注释在行首位置处理方法
def replace_single(line, num):
    return string_to_space(num) + "/*" + line.strip()[2:] + " */\n"


# 单行注释在行末位置处理方法
def replace_single_end(line):
    position = line.index("//")
    return line[:position] + "/* " + line[position+2:].strip() + " */\n"


# 多个单行注释在行末位置处理方法
def replace_multi_end(strs, multi_index):
    position = lines[multi_index].index("//")
    next_position = strs[multi_index + 1].index("//")
    space = string_to_space(next_position)
    return strs[multi_index][:position] + "\n" + space + "/*" + "\n" + space + " *" + strs[multi_index][position+2:]


# 注释中存在"/*"、"*/"替换为"**",否则线上编译报错
def reolace_special_string(line):
    try:
        position = line.index("/*")
        if line[position - 1] != "/":
            line = line[0:position] + "**" + line[position + 2:]
    except ValueError:
        pass
    try:
        if line.strip()[-2:] == "*/":
            position = line.index("*/")
            line = line[0:position] + "**" + line[position + 2:]
    except ValueError:
        pass
    return line


# 处理函数
def deal_except(src_lines, except_str, order, bool):
    exception_flag = bool
    position = src_lines[order].index(except_str)
    len_except_str = len(except_str) + 2
    if src_lines[order][:position].find("//") == -1:    # ftp://的前面未找到"//"
        exception_flag = True
    elif src_lines[order][:position].find("//") != -1:
        if src_lines[order].strip()[:2] == "//":        # 行首找到"//"
            exception_flag = False
    if src_lines[order][position + len_except_str:].find("//") != -1:    # ftp://后面找到"//"
        tmp_str = replace_single_end(src_lines[order][position + len_except_str:])
        src_lines[order] = src_lines[order][:position+len_except_str] + tmp_str
        exception_flag = True
    return exception_flag


# 判断有无ftp://,http://,https://等等情况，若有则跳过
def remove_except(arrays, order):
    have_exception = False
    if arrays[order].find("ftp://") != -1 or arrays[order].find("http://") != -1 or arrays[order].find("https://") != -1:
        if arrays[order].find("ftp://") != -1:
            have_exception = deal_except(arrays, "ftp://", order, have_exception)
        elif arrays[order].find("http://") != -1:
            have_exception = deal_except(arrays, "http://", order, have_exception)
        elif arrays[order].find("https://") != -1:
            have_exception = deal_except(arrays, "https://", order, have_exception)
    if arrays[order].strip()[:2] == "/*" and arrays[order].strip()[-2:] == "*/":
        have_exception = True
    return have_exception


def multi_single_note(start_num, end_num, tmp_num, state_array, arrays, end_state):
    for index, item in enumerate(state_array):
        # 首先判断注释序号是否连贯
        if index <= tmp_num or end_state == 0:
            index += 1
            end_state = 1
        else:
            space = string_to_space(len(tmp_lines[start_num]) - len(tmp_lines[start_num].strip()) - 1)
            if index == 0:
                start_num = state_array[0][0]
            elif 1 <= index < len(state_array) - 1:
                if item[0] == (state_array[index - 1][0] + 1) and item[1] == state_array[index - 1][1]:  # 相同状态
                    end_num = item[0]
                else:  # 如果不相等，则修改注释
                    if state_array[index - 1][1] == 1:  # 注释行首状态
                        for k in range(start_num, end_num + 1):
                            if k == start_num and end_num > start_num:
                                tmp.append(
                                    space + "/*" + "\n" + space + " *" + arrays[k].strip()[2:] + "\n")
                            elif k == start_num and end_num == start_num:
                                space_str = len(tmp_lines[k]) - len(tmp_lines[k].strip()) - 1
                                tmp.append(replace_single(arrays[k], space_str))
                            elif start_num < k <= end_num:
                                if colon in arrays[start_num] and arrays[start_num].strip()[-1] != ":":
                                    tmp.append(space + " *           " + arrays[k].strip()[2:] + "\n")
                                else:
                                    tmp.append(space + " *" + arrays[k].strip()[2:] + "\n")
                            if k == end_num and end_num > start_num:
                                tmp.append(space + " */" + "\n")
                        start_num = item[0]
                        end_num = item[0]
                    else:  # 注释行尾状态，表明前面的所有注释都是行尾
                        tmp_num = index
                        while tmp_num < len(state_array) and state_array[tmp_num][1] == 1:
                            tmp_num += 1
                            end_num += 1
                        tmp_num -= 1

                        for k in range(start_num, end_num + 1):
                            next_line_note_position = arrays[start_num + 1].index("//")
                            space_replace = string_to_space(next_line_note_position)
                            if k == start_num:
                                tmp.append(replace_multi_end(arrays, k))
                            elif start_num < k <= end_num:
                                if colon in arrays[start_num]:
                                    tmp.append(space_replace + " *           " + arrays[k].strip()[2:] + "\n")
                                else:
                                    tmp.append(space_replace + " *" + arrays[k].strip()[2:] + "\n")
                            if k == end_num:
                                tmp.append(space_replace + " */" + "\n")
                        if start_num < state_array[-1][0]:
                            end_state = 0
                        start_num = k + 1
                        end_num = k + 1

            else:  # 多行注释的最后一行
                if item[0] == (state_array[index - 1][0] + 1) and item[1] == state_array[index - 1][1]:  # 连续且相同状态
                    end_num += 1
                    if state_array[index - 1][1] == 1:  # 注释行首状态
                        for k in range(start_num, end_num + 1):
                            if k == start_num:
                                tmp.append(
                                    space + "/*" + "\n" + space + " *" + arrays[k].strip()[2:] + "\n")
                            elif start_num < k <= end_num + 1:
                                if colon in arrays[start_num] and arrays[start_num].strip()[-1] != ":":
                                    tmp.append(space + " *           " + arrays[k].strip()[2:] + "\n")
                                else:
                                    tmp.append(space + " *" + arrays[k].strip()[2:] + "\n")
                            if k == end_num:
                                tmp.append(space + " */" + "\n")
                    elif state_array[index - 1][1] == 0:  # 注释行尾状态，表明前面的所有注释都是行尾
                        for k in range(start_num, end_num + 1):
                            tmp.append(replace_single_end(arrays[k]))

                elif item[0] == (state_array[index - 1][0] + 1) and item[1] != state_array[index - 1][1]:  # 连续但不同状态
                    # end_num += 1
                    if state_array[index - 1][1] == 1:  # 注释行首状态
                        for k in range(start_num, end_num + 1):
                            if k == start_num and end_num > start_num:
                                tmp.append(
                                    space + "/*" + "\n" + space + " *" + arrays[k].strip()[2:] + "\n")
                            elif k == start_num and end_num == start_num:
                                tmp.append(replace_single_end(arrays[k]))
                            elif start_num < k <= end_num:
                                if colon in arrays[start_num] and arrays[start_num].strip()[-1] != ":":
                                    tmp.append(space + " *           " + arrays[k].strip()[2:] + "\n")
                                else:
                                    tmp.append(space + " *" + arrays[k].strip()[2:] + "\n")
                            if k == end_num and end_num > start_num:
                                tmp.append(space + " */" + "\n")

                        if state_array[-1][0] == end_num + 1:
                            tmp.append(replace_single_end(arrays[end_num + 1]))

                    else:  # 注释行尾状态
                        end_num += 1
                        space = string_to_space(len(tmp_lines[start_num+1]) - len(tmp_lines[start_num+1].strip()) - 1)
                        for k in range(start_num, end_num + 1):
                            if k == start_num:
                                tmp.append(replace_multi_end(arrays, k))
                            elif start < k < end:
                                if colon in arrays[start_num]:
                                    tmp.append(space + " *           " + arrays[k].strip()[2:] + "\n")
                                else:
                                    tmp.append(space + " *" + arrays[k].strip()[2:] + "\n")
                            if k == end_num:
                                tmp.append(space + " */" + "\n")


create_outpout_dir()     # 创建用于存储修改注释文件的目录
sum_file_num = 0    # 替换的文件计数
for root, dirs, files in os.walk(os.path.abspath(os.curdir)):       # 遍历目录下所有文件夹
    if os.path.abspath(os.curdir) + "\output_file" not in root:         # 过滤掉输出文件的文件夹
        for filename in files:
            if filename[-2:] == ".c" or filename[-2:] == ".h":
                sum_file_num += 1
                print("正在替换文件:", root + '\\', filename, "的注释!")
                file_encode = file_encoding(root, filename)
                if file_encode == "GB2312":
                    # file_encode = "GB18030"
                    file_encode = "GBK"
                f = open(root + "/" + filename, 'r', encoding=file_encode)
                file_path = mk_sub_dir(root)
                f_out = open(file_path + '\\' + filename, 'w', encoding=file_encode)
                lines = f.readlines()
                tab_to_space(lines)
                tmp_lines = lines.copy()
                f.close()

                # 遍历所有行,进行注释替换
                pattern = r"//.*"  # 匹配"//"
                space_num = 0      # 空格数量
                tmp_index = 0      # 多行注释替换注释后的再次开始的下标
                colon = ":"  # 注释首行有无冒号,据此判断除首行外的缩进
                first_note_position = True  # 第一行注释位置，默认行首
                next_note_position = True  # 第一行外其它注释的位置，默认行首
                start = 0  # 注释开始位置
                end = 0    # 注释结束位置
                flag = 0   # 判断是否为多行注释标志位
                tmp = []
                end_flag = 1    # 替换的多行注释的结束标志

                for i in range(len(lines)):
                    match_obj = re.search(pattern, tmp_lines[i].strip())     # 对每行的内容进行匹配，若使用match则会从字符串首字符开始匹配
                    if match_obj and remove_except(lines, i) is False:
                        flag += 1
                        space_num = len(tmp_lines[i]) - len(tmp_lines[i].strip()) - 1
                    else:
                        if flag == 0:              # 0个单行注释,保存字符串
                            tmp.append(lines[i])
                            flag = 0
                            start = i + 1
                        elif flag == 1:            # 1个单行注释,保存字符串
                            lines[i - 1] = reolace_special_string(lines[i - 1])
                            first_note_position = True if (lines[i-1].strip()[0:2] == "//") else False   # 注释在行首/行末
                            if first_note_position:
                                tmp.append(replace_single(lines[i-1], space_num))
                            else:
                                tmp.append(replace_single_end(lines[i-1]))
                            tmp.append(lines[i])
                            flag = 0
                            start = i + 1
                        else:                       # 多个单行注释
                            end = i

                            # 判断注释在行首还是行末
                            state_list = []
                            for m in range(start, end):
                                lines[m] = reolace_special_string(lines[m])
                                if lines[m].strip()[0:2] == "//":   # 行首位置
                                    state_list.append((m, 1))
                                else:
                                    state_list.append((m, 0))
                            tmp_index = 0

                            # 遍历state_list，按注释位置，进行修改
                            start_index = state_list[0][0]
                            end_index = state_list[0][0]
                            multi_single_note(start_index, end_index, tmp_index, state_list, lines, end_flag)
                            tmp.append(lines[i])
                            flag = 0
                            start = i + 1

                for j in range(len(tmp)):
                    f_out.write(tmp[j])
                f_out.close()
                print(filename, "文件的注释替换完成!")
print("总共替换了", sum_file_num, "个文件!")
input("press enter to exit!")


