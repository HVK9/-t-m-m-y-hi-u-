import os
import json
import subprocess
from fastapi import FastAPI, Request
from datetime import datetime

app = FastAPI()

# Cấu hình GitHub
REPO_PATH = "/home/ubuntu/project_data_access"
DATA_FOLDER = os.path.join(REPO_PATH, "collected_data")

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

def push_to_github(filename):
    """Sử dụng gh CLI để đẩy file lên GitHub"""
    try:
        # Thay đổi thư mục làm việc sang repo
        os.chdir(REPO_PATH)
        
        # Thêm file vào git
        subprocess.run(["git", "add", filename], check=True)
        
        # Commit với thông điệp thời gian thực
        commit_msg = f"Auto-update data at {datetime.now()}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        # Push lên GitHub sử dụng gh CLI hoặc git push (gh đã được cấu hình)
        subprocess.run(["git", "push"], check=True)
        
        print(f"Dữ liệu {filename} đã được đẩy lên GitHub thành công.")
        return True
    except Exception as e:
        print(f"Lỗi khi đẩy lên GitHub: {e}")
        return False

@app.post("/upload")
async def upload_data(request: Request):
    try:
        data = await request.json()
        
        # Tạo tên file theo thời gian
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data_{timestamp}.json"
        filepath = os.path.join(DATA_FOLDER, filename)
        
        # Lưu file cục bộ
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"Đã nhận dữ liệu và lưu vào {filename}")
        
        # Đẩy lên GitHub
        relative_path = os.path.join("collected_data", filename)
        if push_to_github(relative_path):
            return {"status": "success", "message": f"Dữ liệu đã được lưu và đẩy lên GitHub: {filename}"}
        else:
            return {"status": "partial_success", "message": "Dữ liệu đã lưu cục bộ nhưng lỗi khi đẩy lên GitHub"}
            
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("=== MÁY CHỦ CỤC BỘ ĐANG CHẠY TẠI PORT 8000 ===")
    uvicorn.run(app, host="0.0.0.0", port=8000)
