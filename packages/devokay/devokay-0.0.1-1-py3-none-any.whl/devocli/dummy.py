# -*- coding: UTF-8 -*-
# python3

import argparse
import os

def cli():
    parser = argparse.ArgumentParser(description='CLI描述')
    subparsers = parser.add_subparsers(metavar='子命令')

    # 注册命令
    reg_one(subparsers)
    reg_two(subparsers)
    reg_find_big_files(subparsers)

    # 解析命令
    args = parser.parse_args()
    # 1.第一个命令会解析成handle，使用args.handle()就能够调用
    if hasattr(args, 'handle'):
        # 1.1.其他参数会被解析成args的属性，以命令全称为属性名
        args.handle(args)
    # 2.如果没有handle属性，则表示未输入子命令
    else:
        parser.print_help()

def reg_one(subparsers):
    # 添加子命令，演示没有参数
    one_parser = subparsers.add_parser('one', help='第一个命令')
    one_parser.set_defaults(handle=handle_one)

def handle_one(args):
    print('handle_one')

def reg_two(subparsers):
    # 添加子命令，演示有参数
    two_parser = subparsers.add_parser('two', help='第二个命令')
    # 参数(简写，全称，类型，是否必填，帮助说明)
    two_parser.add_argument('-s', '--str', type=str, required=True,
                            help='一个字符串类型参数')
    # 参数(简写，全称，类型，默认值，帮助说明)
    two_parser.add_argument('-d', '--default', type=str, default='默认值',
                            help='这个命令有默认值')
    # 参数(简写，全称，类型，帮助说明)
    two_parser.add_argument('-ts', '--the-str', type=str,
                            help='当全称有横线时，属性名转换为下划线，即 the_str')
    two_parser.set_defaults(handle=handle_two)

def handle_two(args):
    print('handle_two')
    print(f'str:{args.str}')
    print(f'default:{args.default}')
    print(f'the-str:{args.the_str}')


#################################################
    
def get_large_files(folder_path):
    large_files = []
    # 遍历文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            # 获取文件大小（以字节为单位）
            file_size = os.path.getsize(file_path)
            # 如果文件大小大于1M（1M = 1024*1024字节），则添加到列表中
            if file_size > 1024 * 1024:
                large_files.append((file_path, file_size))
    return large_files

def reg_find_big_files(subparsers):
    parser = subparsers.add_parser('find_big_files', help='寻找当前文件夹下的大文件')
    parser.set_defaults(handle=handle_find_big_files)

def handle_find_big_files(args):
    current_path = os.getcwd()
    print(f'current_path: {current_path}')

    big_files = get_large_files(current_path)

    # 输出文件列表
    if len(big_files) > 0:
        for file_path, file_size in big_files:
            print(f"File: {file_path}, Size: {file_size} bytes")
    else:
        print(f"No big deal")

# python cli.py one
# python cli.py two
# python cli.py two -h
if __name__ == '__main__':
    cli()
