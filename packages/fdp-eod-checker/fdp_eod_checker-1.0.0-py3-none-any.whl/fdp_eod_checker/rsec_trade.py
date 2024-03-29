import argparse
import csv
from loguru import logger
from fdp_eod_checker import utils

rsec_trade_headers = [
    "Account", "Counterparty", "OrderID", "OrderPrice", "OrderQty", 
    "Side", "Market", "Symbol", "VenueExecID", "TradePrice", "TradeQty", 
    "TradeTime", "PrimaryPriceFlag", "PrimaryLastPx", "PrimaryBidPx", 
    "PrimaryAskPx", "JNETOrderID", "JNETExecutionID", "JNETTransactionTime"
]

def check(rsec_trade_filename: str, is_prod: bool) -> bool:
    if not utils.header_check(rsec_trade_filename, rsec_trade_headers):
        logger.error(f"{rsec_trade_filename} failed")
        return False

    with open(rsec_trade_filename, 'r', newline='') as file:
        reader = csv.reader(file)
        # 跳过第一行（标题行）
        next(reader)

        for row in reader:
            if len(row) != len(rsec_trade_headers):
                logger.error(f"row: {row} , length != {len(rsec_trade_headers)}")
                continue

            row_dict = dict(zip(rsec_trade_headers, row))

            if not utils.account_check(row_dict['Account'], is_prod):
                logger.error(f"{row_dict['Account']} Account is wrong, {row}")

            if not utils.counterparty_check(row_dict['Counterparty'], is_prod):
                logger.error(f"{row_dict['Counterparty']} Counterparty is wrong, {row}")

            if not utils.price_check(row_dict['OrderPrice'], is_prod):
                logger.error(f"{row_dict['OrderPrice']} OrderPrice is wrong, {row}")
            
            if not utils.int_check(row_dict['OrderQty'], is_prod):
                logger.error(f"{row_dict['OrderQty']} OrderQty is wrong, {row}")
            
            if not utils.side_check(row_dict['Side'], is_prod):
                logger.error(f"{row_dict['Side']} Side is wrong, {row}")
            
            if not utils.market_check(row_dict['Market'], is_prod):
                logger.error(f"{row_dict['Market']} Market is wrong, {row}")
                
            if not utils.symbol_check(row_dict['Symbol'], is_prod):
                logger.error(f"{row_dict['Symbol']} Symbol is wrong, {row}")
                
            if not utils.price_check(row_dict['TradePrice'], is_prod):
                logger.error(f"{row_dict['TradePrice']} TradePrice is wrong, {row}")
            
            if not utils.int_check(row_dict['TradeQty'], is_prod):
                logger.error(f"{row_dict['TradeQty']} TradeQty is wrong, {row}")
            
            if not utils.time_check(row_dict['TradeTime'], is_prod):
                logger.error(f"{row_dict['TradeTime']} TradeTime is wrong, {row}")
            
            if not utils.primarypriceflag_check(row_dict['PrimaryPriceFlag'], is_prod):
                logger.error(f"{row_dict['PrimaryPriceFlag']} PrimaryPriceFlag is wrong, {row}")
            
            if not utils.price_check(row_dict['PrimaryLastPx'], is_prod):
                logger.error(f"{row_dict['PrimaryLastPx']} PrimaryLastPx is wrong, {row}")

            if not utils.price_check(row_dict['PrimaryBidPx'], is_prod):
                logger.error(f"{row_dict['PrimaryBidPx']} PrimaryBidPx is wrong, {row}")

            if not utils.price_check(row_dict['PrimaryAskPx'], is_prod):
                logger.error(f"{row_dict['PrimaryAskPx']} PrimaryAskPx is wrong, {row}")

            if not utils.time_check(row_dict['JNETTransactionTime'], is_prod):
                logger.error(f"{row_dict['JNETTransactionTime']} JNETTransactionTime is wrong, {row}")

    logger.info(f"{rsec_trade_filename} done")
    return True

def main():
    # 创建命令行解析器
    parser = argparse.ArgumentParser(description='RSec Trade Checker')
    parser.add_argument('rsec_trade_filename', type=str, help='Path to the RSec trade file')
    parser.add_argument('--prod', action='store_true', help='Enable production mode')

    # 解析命令行参数
    args = parser.parse_args()

    # 如果文件名以.gz结尾，先解压文件
    if args.rsec_trade_filename.endswith('.gz'):
        # 解压后的文件名
        output_filename = args.rsec_trade_filename[:-3]  # 去掉.gz后缀
        utils.decompress_gzip(args.rsec_trade_filename, output_filename)
        rsec_trade_filename = output_filename
    else:
        rsec_trade_filename = args.rsec_trade_filename

    # 调用 check 函数
    check(rsec_trade_filename, args.prod)

if __name__ == "__main__":
    main()