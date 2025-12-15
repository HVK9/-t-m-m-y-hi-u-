-- Lấy dịch vụ Players
local Players = game:GetService("Players")

-- Xác định người chơi hiện tại (Chính bản thân bạn)
local LocalPlayer = Players.LocalPlayer

-- --- CẤU HÌNH LÝ DO ---
-- Bạn hãy viết lý do muốn hiển thị vào bên trong dấu ngoặc kép bên dưới
local LyDoKick = " địt mẹ mày hiếu " 
-- ----------------------

-- Kiểm tra xem LocalPlayer có tồn tại không (để tránh lỗi) và thực hiện Kick
if LocalPlayer then
    LocalPlayer:Kick(LyDoKick)
end
