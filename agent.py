import os
import sqlite3
import json
import shutil
import time
import requests
from datetime import datetime, timedelta

# Cấu hình
SERVER_URL = "http://localhost:8000/upload"

def get_chrome_history():
    """Lấy lịch sử duyệt web của Chrome trong 24h qua"""
    history_path = os.path.expanduser('~/.config/google-chrome/Default/History')
    if not os.path.exists(history_path):
        return []
    
    # Copy file ra chỗ khác để tránh lỗi lock file khi trình duyệt đang mở
    temp_path = "/tmp/chrome_history_temp"
    shutil.copyfile(history_path, temp_path)
    
    conn = sqlite3.connect(temp_path)
    cursor = conn.cursor()
    
    # Lấy timestamp của 24h trước (Chrome dùng microseconds từ 1601-01-01)
    day_ago = (datetime.now() - timedelta(days=1) - datetime(1601, 1, 1)).total_seconds() * 1000000
    
    query = f"SELECT url, title, last_visit_time FROM urls WHERE last_visit_time > {day_ago} ORDER BY last_visit_time DESC"
    cursor.execute(query)
    results = cursor.fetchall()
    
    history = []
    for row in results:
        history.append({
            "url": row[0],
            "title": row[1],
            "time": str(datetime(1601, 1, 1) + timedelta(microseconds=row[2]))
        })
    
    conn.close()
    os.remove(temp_path)
    return history

def get_chrome_cookies():
    """Lấy cookies của Chrome (Lưu ý: Cookies trên Linux thường được mã hóa bằng keyring)"""
    cookie_path = os.path.expanduser('~/.config/google-chrome/Default/Cookies')
    if not os.path.exists(cookie_path):
        return []
    
    temp_path = "/tmp/chrome_cookies_temp"
    shutil.copyfile(cookie_path, temp_path)
    
    conn = sqlite3.connect(temp_path)
    cursor = conn.cursor()
    
    # Lấy cookies cơ bản (giá trị đã mã hóa encrypted_value)
    query = "SELECT host_key, name, path, expires_utc, value FROM cookies"
    cursor.execute(query)
    results = cursor.fetchall()
    
    cookies = []
    for row in results:
        cookies.append({
            "host": row[0],
            "name": row[1],
            "path": row[2],
            "expires": row[3],
            "value": row[4] # Trên Linux, giá trị thật thường nằm ở encrypted_value
        })
    
    conn.close()
    os.remove(temp_path)
    return cookies

def main():
    print("=== HỆ THỐNG TRUY XUẤT DỮ LIỆU TỐI ƯU ===")
    confirm = input("Bạn có đồng ý cho phép ứng dụng truy xuất cookie và lịch sử duyệt web trong 24h qua không? (y/n): ")
    
    if confirm.lower() != 'y':
        print("Truy cập bị từ chối bởi người dùng.")
        return

    print("Đang thu thập dữ liệu...")
    data = {
        "timestamp": str(datetime.now()),
        "history": get_chrome_history(),
        "cookies": get_chrome_cookies()
    }
    
    print(f"Đã thu thập {len(data['history'])} bản ghi lịch sử và {len(data['cookies'])} cookies.")
    
    try:
        response = requests.post(SERVER_URL, json=data)
        if response.status_code == 200:
            print("Dữ liệu đã được gửi về máy chủ cục bộ thành công.")
        else:
            print(f"Lỗi khi gửi dữ liệu: {response.status_code}")
    except Exception as e:
        print(f"Không thể kết nối tới máy chủ cục bộ: {e}")

if __name__ == "__main__":
    main()
