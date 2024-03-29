import argparse
import csv
from loguru import logger
from fdp_eod_checker import rsec_trade, utils

def check(mm_trade_filename: str, is_prod: bool) -> bool:
    return rsec_trade.check(mm_trade_filename, is_prod)

def main():
    # 创建命令行解析器
    parser = argparse.ArgumentParser(description='MM Trade Checker')
    parser.add_argument('mm_trade_filename', type=str, help='Path to the MM trade file')
    parser.add_argument('--prod', action='store_true', help='Enable production mode')

    # 解析命令行参数
    args = parser.parse_args()

    # 如果文件名以.gz结尾，先解压文件
    if args.mm_trade_filename.endswith('.gz'):
        # 解压后的文件名
        output_filename = args.mm_trade_filename[:-3]  # 去掉.gz后缀
        utils.decompress_gzip(args.mm_trade_filename, output_filename)
        mm_trade_filename = output_filename
    else:
        mm_trade_filename = args.mm_trade_filename

    print(mm_trade_filename)

    # 调用 check 函数
    check(mm_trade_filename, args.prod)

if __name__ == "__main__":
    main()