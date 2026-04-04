#include <iostream>
#include <windows.h>
#include <thread>
#include <chrono>

/**
 * @brief Chương trình Auto Click đơn giản sử dụng Windows API.
 * 
 * Lưu ý: Mã này được thiết kế để chạy trên hệ điều hành Windows.
 * Nó sử dụng thư viện windows.h để mô phỏng các sự kiện chuột.
 */

bool clicking = false;

void AutoClicker(int delay_ms) {
    while (true) {
        if (clicking) {
            // Nhấn chuột trái (Down)
            mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
            // Thả chuột trái (Up)
            mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
            
            // Nghỉ giữa các lần click
            std::this_thread::sleep_for(std::chrono::milliseconds(delay_ms));
        } else {
            // Nếu không ở trạng thái click, nghỉ một chút để giảm tải CPU
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
    }
}

int main() {
    int interval;
    std::cout << "--- Chuong trinh Auto Click C++ ---" << std::endl;
    std::cout << "Nhap khoang cach giua cac lan click (ms): ";
    std::cin >> interval;

    std::cout << "\nHuong dan:" << std::endl;
    std::cout << "- Nhan 'F7' de BAT DAU / TAM DUNG auto click." << std::endl;
    std::cout << "- Nhan 'F8' de THOAT chuong trinh." << std::endl;

    // Chạy thread auto clicker trong nền
    std::thread clickThread(AutoClicker, interval);
    clickThread.detach();

    while (true) {
        // Kiểm tra phím F7 (Bật/Tắt)
        if (GetAsyncKeyState(VK_F7) & 0x8000) {
            clicking = !clicking;
            if (clicking) {
                std::cout << "[STATUS] Dang bat dau click..." << std::endl;
            } else {
                std::cout << "[STATUS] Da tam dung click." << std::endl;
            }
            // Tránh việc phím bị nhấn giữ quá nhanh
            std::this_thread::sleep_for(std::chrono::milliseconds(300));
        }

        // Kiểm tra phím F8 (Thoát)
        if (GetAsyncKeyState(VK_F8) & 0x8000) {
            std::cout << "[STATUS] Dang thoat chuong trinh..." << std::endl;
            break;
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }

    return 0;
}
