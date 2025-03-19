# common/utils.py
import datetime

def format_date(date):
    """Chuyển datetime thành chuỗi định dạng DD/MM/YYYY"""
    return date.strftime("%d/%m/%Y")

def generate_greeting(name):
    """Tạo lời chào tùy chỉnh"""
    return f"Xin chào, {name}!"
