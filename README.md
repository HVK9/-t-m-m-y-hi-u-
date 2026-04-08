# Hệ thống Truy xuất Dữ liệu và Lưu trữ GitHub Tự động

Dự án này bao gồm hai thành phần chính để truy xuất lịch sử duyệt web và cookie (trong 24h qua) với sự đồng ý của người dùng, sau đó tự động lưu trữ lên GitHub.

## Thành phần

1.  **`server.py`**: Máy chủ cục bộ (FastAPI) nhận dữ liệu từ agent, lưu thành file JSON và tự động thực hiện `git push` lên repository này.
2.  **`agent.py`**: Công cụ chạy trên máy khách, xin phép người dùng và thu thập dữ liệu từ trình duyệt (Chrome/Edge/Firefox) rồi gửi về máy chủ.

## Yêu cầu hệ thống

- Python 3.10+
- Thư viện: `fastapi`, `uvicorn`, `requests`
- GitHub CLI (`gh`) đã đăng nhập hoặc Git đã cấu hình quyền push.

## Cách sử dụng

### Bước 1: Chạy máy chủ cục bộ
Máy chủ cần được chạy trước để sẵn sàng nhận dữ liệu.
```bash
python3 server.py
```

### Bước 2: Chạy Agent thu thập
Mở một terminal khác và chạy agent. Agent sẽ hỏi ý kiến bạn trước khi thu thập.
```bash
python3 agent.py
```

## Luồng hoạt động
1. Agent khởi chạy -> Người dùng nhập 'y' để đồng ý.
2. Agent đọc file SQLite của trình duyệt (Chrome) trong thư mục cấu hình người dùng.
3. Dữ liệu được lọc theo thời gian (24h qua).
4. Dữ liệu gửi tới `http://localhost:8000/upload`.
5. Server nhận dữ liệu -> Lưu vào thư mục `collected_data/`.
6. Server gọi lệnh Git để đẩy file mới lên GitHub.

## Lưu ý về bảo mật
- Dữ liệu cookie trên Linux/Windows thường được mã hóa bởi hệ điều hành. Agent này thu thập giá trị thô (encrypted). Để giải mã cần quyền truy cập vào Keyring của hệ thống.
- Luôn đảm bảo bạn chỉ chạy agent trên máy tính mà bạn có quyền sở hữu.
