import re, gzip, shutil
from typing import List
from loguru import logger

def decompress_gzip(input_file, output_file):
    with gzip.open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def header_check(csv_filename: str, header_list: List[str]) -> bool:
    try:
        with open(csv_filename, 'r', newline='') as file:
            first_line = file.readline().strip()
            headers = [header.strip() for header in first_line.split(',')]
        
        # 检查字段是否匹配
        if headers == header_list:
            return True
        else:
            logger.error(f"Header mismatch. Expected: {header_list}, Actual: {headers}")
            return False
    except FileNotFoundError:
        logger.error(f"{csv_filename} file NOT found!")
        return False



def account_check(account: str, is_prod: bool) -> bool:
    if is_prod:
        # TODO
        pass
    else:
        pattern = r'^[a-zA-Z0-9_]+$'
        if re.match(pattern, account):
            return True
        else:
            return False

def counterparty_check(counterparty: str, is_prod: bool) -> bool:
    # TODO: 应该为多少呢？'HRT' or 'FT'？？？
    return counterparty == "RSEC_PROP"

def price_check(price: str, is_prod: bool) -> bool:
    try:
        price_float = float(price)
        return True
    except ValueError:
        logger.error(f"Invalid price. price: {price}")
        return False

def int_check(input: str, is_prod: bool) -> bool:
    try:
        input_int = int(input)
        return True
    except ValueError:
        logger.error("Invalid int")
        return False

def side_check(side: str, is_prod: bool) -> bool:
    return side == '1' or side == '2'

def market_check(market: str, is_prod: bool) -> bool:
    return market == 'FDP'

def symbol_check(symbol: str, is_prod: bool) -> bool:
    # 定义正则表达式模式，匹配 9 位数字
    pattern = r'^\d{9}$'
    
    # 使用正则表达式进行匹配
    if re.match(pattern, symbol):
        return True
    else:
        logger.error("Invalid symbol. Symbol must be a 9-digit number.")
        return False

def time_check(time_str: str, is_prod: bool) -> bool:
    # 定义正则表达式模式，匹配指定的时间格式
    pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+$'
    
    # 使用正则表达式进行匹配
    if re.match(pattern, time_str):
        return True
    else:
        logger.error("Invalid time format. Time must be in the format: YYYY-MM-DD HH:MM:SS.sssssssss")
        return False

def primarypriceflag_check(primarypriceflag: str, is_prod: bool) -> bool:
    return primarypriceflag == '1'