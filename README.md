# 🌤️ Hệ Thống Giàn Phơi Thông Minh IoT (Smart Clothesline IoT System)

[![MicroPython](https://img.shields.io/badge/MicroPython-v1.20+-blue?logo=python&logoColor=white)](https://micropython.org/)
[![Hardware](https://img.shields.io/badge/Board-WeMos%20D1%20R2%20(ESP8266)-red?logo=espressif&logoColor=white)](https://www.espressif.com/)
[![Database](https://img.shields.io/badge/Database-Firebase%20Realtime-orange?logo=firebase&logoColor=white)](https://firebase.google.com/)
[![Frontend](https://img.shields.io/badge/Frontend-SPA%20Vanilla%20JS%20%2B%20Chart.js-yellow?logo=javascript&logoColor=white)](https://www.chartjs.org/)
[![Version](https://img.shields.io/badge/Version-v3.2.0-green.svg)](version.json)
[![Security](https://img.shields.io/badge/Security-Protected%20Secrets-brightgreen)](#-7-bảo-mật--quản-lý-khóa-kết-nối-secrets--api-keys)

Hệ thống **Giàn Phơi Thông Minh IoT** là giải pháp tự động hóa gia đình toàn diện, kết hợp giữa vi điều khiển nhúng **WeMos D1 R2 (ESP8266)** chạy **MicroPython**, dịch vụ điện toán đám mây **Google Firebase Realtime Database**, và bảng điều khiển người dùng **Web Dashboard SPA**. 

Hệ thống tự động bảo vệ quần áo trước các hình thái thời tiết cực đoan (mưa rào, sương đêm, độ ẩm cao), tận dụng tối đa năng lượng mặt trời để phơi đồ, đồng thời hỗ trợ giám sát, phân tích số liệu và điều khiển từ xa theo thời gian thực.

---

## 📑 Mục Lục
1. [Tính Năng Nổi Bật](#-1-tính-năng-nổi-bật)
2. [Kiến Trúc Hệ Thống](#-2-kiến-trúc-hệ-thống)
3. [Sơ Đồ Phần Cứng & Đấu Nối Chân (Pinout)](#-3-sơ-đồ-phần-cứng--đấu-nối-chân-pinout)
4. [Cấu Trúc Thư Mục Dự Án](#-4-cấu-trúc-thư-mục-dự-án)
5. [Kiến Trúc Dữ Liệu Firebase (Schema V2.0)](#-5-kiến-trúc-dữ-liệu-firebase-schema-v20)
6. [Giao Diện Bảng Điều Khiển Web Dashboard](#-6-giao-diện-bảng-điều-khiển-web-dashboard)
7. [Bảo Mật & Quản Lý Khóa Kết Nối (Secrets & API Keys)](#-7-bảo-mật--quản-lý-khóa-kết-nối-secrets--api-keys)
8. [Hướng Dẫn Triển Khai & Cài Đặt](#-8-hướng-dẫn-triển-khai--cài-đặt)
9. [Cổng Cấu Hình Wi-Fi (Captive Portal)](#-9-cổng-cấu-hình-wi-fi-captive-portal)
10. [Cập Nhật Từ Xa Over-The-Air (GitHub OTA)](#-10-cập-nhật-từ-xa-over-the-air-github-ota)
11. [Xử Lý Sự Cố Thường Gặp (Troubleshooting)](#-11-xử-lý-sự-cố-thường-gặp-troubleshooting)

---

## ✨ 1. Tính Năng Nổi Bật

- 🌧️ **Cảm biến thời tiết đa tầng:** Tích hợp bộ chuyển đổi ADC 16-bit ADS1115 đọc cảm biến giọt nước (`WATER_A2`) và quang trở đo nắng (`LDR_A1`) với độ chính xác cao; kết hợp cảm biến DHT11 đo nhiệt độ và độ ẩm môi trường.
- ⚙️ **Chấp hành Servo SG90 an toàn:** Điều khiển góc quay sào phơi (0°: Mở phơi, 90°: Thu sào). Cơ chế tự động ngắt xung PWM sau khi quay giúp triệt tiêu hiện tượng rung giật (jitter), chống nóng động cơ và ngăn ngừa sụt áp nguồn.
- 🧠 **Cơ chế điều khiển FSM thông minh:**
  - **Chế độ Tự động (AUTO):** Tự động mở/thu sào theo lịch trình cài đặt sẵn (`open_time` - `close_time`) kết hợp quy tắc an toàn ưu tiên mưa/ẩm cao (`rain_priority_override`).
  - **Chế độ Thủ công (MANUAL):** Cho phép người dùng can thiệp đóng/mở tức thì từ nút nhấn vật lý hoặc nút bấm trên Web Dashboard mà không bị lịch trình ghi đè.
  - **Fail-safe chống ướt:** Nếu mất kết nối với module ADC ADS1115, hệ thống tự động nhận diện thời tiết xấu và thu sào vào nhà.
- 📡 **Wi-Fi Captive Portal thông minh:** Cho phép đổi mạng Wi-Fi dễ dàng qua điện thoại (kết nối vào AP `SaoPhoi-Setup` tại `192.168.4.1`) mà không cần cắm cáp nạp lại code.
- ⏰ **Đồng bộ thời gian thực NTP (UTC+7):** Tự động lấy giờ chuẩn Internet, tính toán tổng số phút phơi nắng thực tế trong ngày (`sun_minutes_today`) và tự động đặt lại bộ đếm vào đúng nửa đêm `00:00`.
- 🚀 **Cập nhật Firmware từ xa (GitHub OTA):** Tải trực tiếp mã nguồn từ GitHub Repository mà không cần tháo lắp thiết bị; cơ chế nạp file tạm `.tmp` chống hỏng hóc vi điều khiển (anti-brick).
- 📊 **Bảng điều khiển Web Dashboard 4 Phân khu:** Thiết kế giao diện trực quan, responsive, tích hợp Chart.js vẽ biểu đồ thời gian thực, dự báo thời tiết Open-Meteo và thanh giả lập Dev Simulator Bar.

---

## 🏛️ 2. Kiến Trúc Hệ Thống

```text
               +-------------------------------------------------------------+
               |                    GOOGLE FIREBASE CLOUD                    |
               |             Realtime Database (JSON Schema V2.0)            |
               +-----------------------------+-------------------------------+
                                             ^
                                             | REST / JSON (Polling & Patch)
                                             v
+--------------------------+    I2C    +-------------------+    PWM (D7)   +------------------+
| ADS1115 (16-bit ADC)     | --------> |                   | ------------> | Servo SG90       |
| - Cảm biến mưa (A2)      |           |   WeMos D1 R2     |               | (Kéo / Thu sào)  |
| - Quang trở LDR (A1)     |           |   (ESP8266 MCU)   |               +------------------+
+--------------------------+           |                   |    GPIO (D4)  +------------------+
                                       |   MicroPython     | <-----------+ | Cảm biến DHT11   |
+--------------------------+    IRQ    |   Firmware V3.2   |               | (Nhiệt & Độ ẩm)  |
| Nút nhấn cơ học SW1 (D6) | --------> |                   |               +------------------+
+--------------------------+           +---------+---------+
                                                 ^
                                                 | Wi-Fi 802.11 b/g/n
                                                 v
                               +-----------------+-----------------+
                               |   WEB DASHBOARD (SPA HTML5/JS)    |
                               | - Trang 1: Giám sát tổng quan     |
                               | - Trang 2: Biểu đồ & Lịch sử      |
                               | - Trang 3: Cài đặt & Hẹn giờ      |
                               | - Trang 4: Bảo trì & GitHub OTA   |
                               | - Dev Simulator Bar (Kiểm thử)    |
                               +-----------------+-----------------+
                                                 |
                                                 v
                               +-----------------+-----------------+
                               |    Open-Meteo Weather API         |
                               |    (Dự báo thời tiết ngoài trời)  |
                               +-----------------------------------+
```

---

## 🔌 3. Sơ Đồ Phần Cứng & Đấu Nối Chân (Pinout)

Hệ thống được thiết kế trên kit **WeMos D1 R2** dựa trên chip ESP8266. Toàn bộ sơ đồ mạch nguyên lý chi tiết được lưu trữ tại file [schematic.pdf](schematic.pdf).

| Thành phần linh kiện | Tín hiệu kết nối | Chân trên WeMos D1 R2 | Chân GPIO (ESP8266) | Mô tả chức năng & Ghi chú kỹ thuật |
| :--- | :--- | :--- | :--- | :--- |
| **Module ADC ADS1115** | `SCL` (Clock)<br>`SDA` (Data)<br>`ADDR` nối `GND` | `D1`<br>`D2`<br>`GND` | `GPIO 5`<br>`GPIO 4`<br>- | Giao tiếp I2C tốc độ cao, địa chỉ I2C mặc định `0x48`, độ phân giải 16-bit. |
| **Cảm biến Mưa / Nước (SEN1)** | Tín hiệu `S` (Analog) | Chân `A2` của ADS1115 | Kênh `A2` ADS1115 | Đọc độ dẫn điện khi mặt cảm biến có nước mưa. Giá trị cao hơn ngưỡng báo trời mưa. |
| **Quang trở LDR (LDR1)** | Cầu phân áp trở $10\text{ k}\Omega$ | Chân `A1` của ADS1115 | Kênh `A1` ADS1115 | Đo cường độ ánh sáng môi trường. Giá trị cao hơn ngưỡng xác định trời nắng. |
| **Cảm biến DHT11** | Chân `Data` (Out) | `D4` | `GPIO 2` | Đo nhiệt độ và độ ẩm không khí. Tích hợp trở kéo lên nội bộ. |
| **Nút nhấn vật lý (SW1)** | Chân tín hiệu ngắt | `D6` | `GPIO 12` | Kèm trở kéo xuống $10\text{ k}\Omega$ (Active HIGH). Ngắt ngoài IRQ: Nhấn nhanh đổi trạng thái, nhấn giữ $\ge 3\text{s}$ reset chip. |
| **Động cơ Servo SG90 (M1)** | Dây tín hiệu xung (Cam) | `D7` | `GPIO 13` | Điều khiển độ rộng xung PWM tần số 50 Hz. Nguồn cấp 5V kèm tụ hóa lọc nguồn $100\mu\text{F}$ chống sụt áp. |
| **Nguồn cấp hệ thống** | `VCC` & `GND` | `5V` & `GND` | - | Nguồn Adapter ổn áp 5V - 2A đảm bảo dòng khởi động cho Servo và sóng Wi-Fi. |

> [!NOTE]
> **Biện pháp chống rung & sụt áp Servo:** Động cơ Servo SG90 khi giữ vị trí liên tục có thể sinh nhiệt và gây nhiễu nguồn. Trong `main_setup.py`, firmware kích xung dịch chuyển 500ms rồi ngắt xung PWM (`servo_pwm.duty(0)`), giúp sào phơi giữ nguyên vị trí cơ học mà động cơ hoàn toàn mát mẻ.

---

## 📁 4. Cấu Trúc Thư Mục Dự Án

```text
Iot_smart_drying_rack/
├── .env.example             # Mẫu cấu hình biến môi trường chuẩn cho toàn bộ dự án
├── .gitignore               # Bộ lọc bỏ qua file nhạy cảm, secrets, config.ini và cache
├── schematic.pdf            # Sơ đồ mạch nguyên lý phần cứng
├── version.json             # Định danh phiên bản firmware V3.2.0 phục vụ GitHub OTA
│
├── firmware/                # Mã nguồn MicroPython tối ưu bộ nhớ chạy trên WeMos D1 R2
│   ├── boot.py              # Safe Boot: Xử lý nút SW1 kích hoạt Captive Portal & kết nối Wi-Fi
│   ├── config.py            # Quản lý cấu hình chân GPIO, ngưỡng cảm biến & đọc env/ini
│   ├── config.ini.example   # File mẫu cấu hình Wi-Fi & Firebase cho ESP8266
│   ├── wifi_manager.py      # Cổng cấu hình Captive Portal thông minh (AP SaoPhoi-Setup 192.168.4.1)
│   ├── ads1x15.py           # Driver I2C điều khiển ADC 16-bit ADS1115
│   ├── ota.py               # Quản lý cập nhật Firmware từ xa qua GitHub Raw an toàn
│   ├── main.py              # Loader nạp tuần tự các module nhằm tối ưu RAM ESP8266
│   ├── main_setup.py        # Khởi tạo ngoại vi, ngắt IRQ nút nhấn, PWM và đồng bộ NTP
│   ├── main_io.py           # Thuật toán chống dội phím SW1 và đọc dữ liệu cảm biến (DHT11, ADS1115)
│   ├── main_sync.py         # Đồng bộ lệnh điều khiển, cấu hình lịch và cờ bảo trì từ Firebase
│   ├── main_control.py      # Bộ máy trạng thái FSM: AUTO/MANUAL, lịch phơi, ưu tiên mưa
│   ├── main_periodic.py     # Định kỳ đẩy telemetry lên Firebase và ghi lịch sử mỗi 5 phút
│   └── main_loop.py         # Vòng lặp điều phối chính (Main Loop) của hệ thống
│
├── webapp/                  # Bảng điều khiển Web Dashboard SPA (HTML5/CSS3/ES6+)
│   ├── index.html           # Khung giao diện SPA 4 phân khu + Dev Simulator Bar
│   ├── style.css            # Giao diện responsive hiện đại, chế độ thẻ và nút bấm trực quan
│   ├── config.js            # Module nạp cấu hình Firebase/GitHub từ LocalStorage và .env
│   ├── .env.example         # File mẫu cấu hình cục bộ cho Web Dashboard
│   └── app.js               # Logic điều khiển Firebase v10 Modular, Chart.js, Open-Meteo & OTA
│
└── README.md                # Tài liệu kỹ thuật dự án & Hướng dẫn sử dụng chi tiết
```

---

## 🗄️ 5. Kiến Trúc Dữ Liệu Firebase (Schema V2.0)

Cơ sở dữ liệu **Firebase Realtime Database** được phân cấp rõ ràng thành các nhánh độc lập. Firmware chỉ tải từng nhánh nhỏ cần thiết để tránh tình trạng tràn bộ nhớ RAM (Out Of Memory) trên chip ESP8266.

```json
{
  "smart_clothesline": {
    "telemetry": {
      "temperature": 32.4,
      "humidity": 62.0,
      "water_a0": 340,
      "is_raining": false,
      "ldr_a1": 2450,
      "is_sunny": true,
      "is_humid": false,
      "clothesline_state": "OPEN",
      "sun_minutes_today": 185,
      "firmware_version": "3.2.0",
      "last_updated": 1730530000
    },
    "control": {
      "mode": "AUTO",
      "manual_command": "NONE",
      "servo_angle": 0,
      "rain_threshold": 2000,
      "sun_threshold": 2000,
      "humidity_threshold": 80.0
    },
    "schedule": {
      "auto_schedule_enabled": true,
      "open_time": "07:00",
      "close_time": "18:00",
      "rain_priority_override": true
    },
    "maintenance": {
      "current_version": "3.2.0",
      "target_version": "3.2.0",
      "trigger_ota": false,
      "trigger_reset": false,
      "ota_status": "IDLE"
    },
    "history": {
      "1730526400": {
        "temp": 31.0,
        "hum": 65.0,
        "water_a0": 320,
        "ldr_a1": 2100
      }
    }
  }
}
```

### Ý nghĩa các trường dữ liệu chính:

| Nhánh dữ liệu | Khóa (Key) | Kiểu | Mô tả |
| :--- | :--- | :--- | :--- |
| `telemetry` | `clothesline_state` | string | Trạng thái hiện tại của sào phơi: `"OPEN"` (Đang mở) hoặc `"CLOSED"` (Đang thu). |
| `telemetry` | `is_raining` | bool | `true` nếu giá trị `water_a0` vượt quá ngưỡng mưa `rain_threshold`. |
| `telemetry` | `is_sunny` | bool | `true` nếu quang trở `ldr_a1` vượt quá ngưỡng nắng `sun_threshold`. |
| `telemetry` | `is_humid` | bool | `true` nếu độ ẩm không khí vượt quá `humidity_threshold` (sương/ẩm ướt). |
| `telemetry` | `sun_minutes_today` | int | Tổng số phút phơi nắng thực tế tích lũy trong ngày. |
| `control` | `mode` | string | Chế độ vận hành: `"AUTO"` (Theo lịch & cảm biến) hoặc `"MANUAL"` (Thủ công). |
| `control` | `manual_command` | string | Lệnh thủ công từ Web/Nút bấm: `"OPEN"`, `"CLOSE"` hoặc `"NONE"`. |
| `schedule` | `rain_priority_override`| bool | `true`: Tự động thu sào khi gặp mưa hoặc độ ẩm cao dù đang trong khung giờ phơi. |
| `maintenance` | `trigger_ota` | bool | Đặt thành `true` để kích hoạt firmware tải và nạp bản cập nhật mới từ GitHub. |
| `maintenance` | `trigger_reset` | bool | Đặt thành `true` để ra lệnh khởi động lại vi điều khiển từ xa. |
| `history` | `<timestamp>` | object | Điểm dữ liệu ghi định kỳ 5 phút/lần phục vụ vẽ đồ thị phân tích. |

---

## 🖥️ 6. Giao Diện Bảng Điều Khiển Web Dashboard

Giao diện Web Dashboard được xây dựng theo mô hình Single Page Application (SPA), trực quan hóa dữ liệu theo 4 tab chuyên biệt:

```text
+-----------------------------------------------------------------------------------+
|  🌤️ HỆ THỐNG SÀO PHƠI THÔNG MINH IoT                         [Trạng thái kết nối]  |
|  [Tab 1: Tổng quan]  [Tab 2: Biểu đồ & Lịch sử]  [Tab 3: Cài đặt]  [Tab 4: Bảo trì]  |
+-----------------------------------------------------------------------------------+
```

### 1. Tab 1: Trang Tổng quan (Overview Dashboard)
- **Trạng thái Sào phơi:** Hiển thị trực quan sào đang MỞ hay THU, kèm nút chuyển đổi chế độ **Tự động / Thủ công** và nút đóng/mở nhanh.
- **Xác thực thời tiết tại chỗ:** Thẻ trạng thái Mưa (`WATER_A2`), Quang trở Nắng (`LDR_A1`) và Độ ẩm không khí (`DHT11`).
- **Dự báo thời tiết ngoài trời:** Tích hợp trực tiếp từ **Open-Meteo API** (nhiệt độ, lượng mưa, tốc độ gió và độ ẩm theo định vị địa lý).
- **Thẻ cảm biến Realtime:** Đo lường 4 đại lượng môi trường cập nhật tức thì.

### 2. Tab 2: Biểu đồ & Lịch sử (Charts & Analytics)
- **Thống kê thời gian phơi trong ngày:** Đồng hồ hiển thị tổng số giờ và phút quần áo được phơi dưới nắng.
- **Bộ lọc khung thời gian:** Xem nhanh dữ liệu 12 mốc (~1 giờ), 36 mốc (~3 giờ), hoặc 72 mốc (~6 giờ).
- **Biểu đồ kép Chart.js:** 
  - Biểu đồ biến thiên Nhiệt độ - Độ ẩm.
  - Biểu đồ cảm biến giọt nước A2 và quang trở ánh sáng A1.

### 3. Tab 3: Cài đặt & Hẹn giờ (Settings & Schedule)
- **Lịch trình phơi đồ:** Cài đặt giờ mở sào (`open_time`, mặc định `07:00`) và giờ thu sào (`close_time`, mặc định `18:00`). Hỗ trợ khung giờ xuyên qua nửa đêm.
- **Công tắc ưu tiên mưa/ẩm (`rain_priority_override`):** Bật chế độ tự động thu sào khẩn cấp khi phát hiện mưa hoặc độ ẩm vượt chuẩn.
- **Hiệu chuẩn ngưỡng cảm biến:** Tinh chỉnh ngưỡng mưa, ngưỡng nắng và ngưỡng độ ẩm trực tiếp từ giao diện.
- **Cấu hình kết nối:** Nhập Firebase Database URL, API Key (có tính năng che/hiện bảo mật) và thông tin GitHub Repository.

### 4. Tab 4: Bảo trì Hệ thống (Maintenance & OTA)
- **Quản lý phiên bản:** Kiểm tra phiên bản firmware hiện tại so với bản phát hành mới nhất trên GitHub.
- **Kích hoạt OTA:** Ra lệnh cho thiết bị tự động cập nhật qua mạng chỉ với 1 cú click.
- **Khởi động lại từ xa:** Gửi lệnh `trigger_reset = true` để khởi động lại mạch từ xa.

### 🛠️ Dev Simulator Bar (Công cụ Mô Phỏng Dành Cho Nhà Phát Triển)
Nằm ở góc dưới giao diện, cung cấp môi trường kiểm thử không cần phần cứng:
- **Kịch bản nhanh (Quick Scenarios):** ☀️ Nắng to (Phơi đồ), 🌧️ Đổ mưa (Thu sào khẩn cấp), 🌥️ Râm mát / Tối, 🌙 Đêm khuya.
- **Thanh trượt thủ công:** Tự do điều chỉnh giá trị cảm biến Nước A2, Quang trở A1, Nhiệt độ và Độ ẩm.
- **Chế độ kiểm thử:**
  - `Local Mock`: Thử nghiệm giao diện và biểu đồ hoàn toàn trên trình duyệt.
  - `Firebase Sync`: Đẩy dữ liệu mô phỏng trực tiếp lên Firebase để kiểm thử toàn diện cả mạch thực tế từ xa.
- **Tự động sinh dao động (Auto-drift):** Tự động phát sinh thay đổi nhỏ mỗi 3 giây để kiểm tra tính mượt mà của biểu đồ Chart.js.

---

## 🔒 7. Bảo Mật & Quản Lý Khóa Kết Nối (Secrets & API Keys)

Để ngăn ngừa triệt để nguy cơ rò rỉ khóa API, thông tin đăng nhập Wi-Fi và đường dẫn cơ sở dữ liệu lên các kho lưu trữ công khai (GitHub), dự án áp dụng các tiêu chuẩn an ninh nghiêm ngặt sau:

### 1. Quy tắc `.gitignore` & Loại bỏ tệp bí mật
- Các tệp cấu hình thực tế như `.env`, `firmware/config.ini`, `webapp/.env` **được đưa vào danh sách loại trừ của Git** và tuyệt đối không bao giờ được commit lên repository.
- Dự án cung cấp các tệp mẫu an toàn:
  - [`.env.example`](.env.example): Mẫu biến môi trường chung.
  - [`firmware/config.ini.example`](firmware/config.ini.example): Mẫu thông số Wi-Fi và Firebase cho ESP8266.
  - [`webapp/.env.example`](webapp/.env.example): Mẫu cấu hình cục bộ cho giao diện Web.

### 2. Bảo vệ hiển thị API Key trên giao diện (Masked Input)
- Tại tab **Cài đặt & Hẹn giờ** trên Web Dashboard, trường nhập **Firebase API Key** được thiết lập mặc định ở dạng `type="password"`.
- Bổ sung nút bấm ẩn/hiện (`👁️` / `🙈`) cho phép người dùng kiểm tra khi cần thiết, đồng thời tránh lộ thông tin nhạy cảm khi thuyết trình, quay video demo hoặc chia sẻ màn hình.

### 3. Cấu hình Luật An Toàn Firebase (Firebase Security Rules)
Khi triển khai dự án thực tế, không nên để cơ sở dữ liệu ở chế độ công khai hoàn toàn (`read: true, write: true`). Hãy áp dụng luật xác thực an toàn trong Firebase Console:

```json
{
  "rules": {
    "smart_clothesline": {
      ".read": true,
      ".write": "auth != null || (newData.child('telemetry').exists() || newData.child('control').exists())",
      "history": {
        ".indexOn": [".key"]
      }
    }
  }
}
```

---

## 🚀 8. Hướng Dẫn Triển Khai & Cài Đặt

### Bước 1: Chuẩn bị phần cứng & Môi trường nạp mã
1. Chuẩn bị kit **WeMos D1 R2 (ESP8266)**, cảm biến mưa, quang trở LDR, DHT11, module ADS1115 và Servo SG90 theo đúng [bảng đấu nối chân](#-3-sơ-đồ-phần-cứng--đấu-nối-chân-pinout).
2. Cài đặt Driver cổng giao tiếp nạp (CH340 hoặc CP2102) trên máy tính.
3. Cài đặt phần mềm lập trình MicroPython: **Thonny IDE** hoặc **uPyCraft IDE**.
4. Nạp firmware MicroPython bản mới nhất (khuyến nghị phiên bản MicroPython ESP8266 v1.20+) vào kit.

### Bước 2: Thiết lập thông số cấu hình Firmware
1. Trong thư mục `firmware/`, sao chép tệp mẫu `config.ini.example` thành `config.ini`:
   ```bash
   cp firmware/config.ini.example firmware/config.ini
   ```
2. Mở file `firmware/config.ini` và điền thông tin mạng Wi-Fi và Firebase của bạn:
   ```ini
   WIFI_SSID="Tên_WiFi_Nha_Ban"
   WIFI_PASSWORD="Mat_Khau_WiFi"
   FIREBASE_URL="https://your-project-id-default-rtdb.asia-southeast1.firebasedatabase.app"
   FIREBASE_AUTH=""
   ```
3. Nạp toàn bộ các file trong thư mục `firmware/` vào bộ nhớ Flash của ESP8266.

### Bước 3: Khởi chạy Web Dashboard
Giao diện Web là ứng dụng tĩnh (Static Web), không yêu cầu cài đặt Node.js hay build phức tạp:
1. Mở file `webapp/index.html` trực tiếp trên trình duyệt web bất kỳ.
2. Hoặc sử dụng extension **Live Server** trong VS Code để khởi chạy máy chủ cục bộ:
   ```bash
   cd webapp
   # Chạy máy chủ đơn giản với Python:
   python -m http.server 8080
   ```
3. Truy cập tab **Cài đặt & Hẹn giờ**, nhập URL Firebase Realtime Database của bạn và bấm **Lưu cài đặt**.

---

## 📡 9. Cổng Cấu Hình Wi-Fi (Captive Portal)

Hệ thống hỗ trợ cổng cấu hình mạng không dây thông minh, rất hữu ích khi mang thiết bị đến vị trí mới mà không cần cắm cáp vào máy tính:

```text
+------------------+       1. Kết nối Wi-Fi       +---------------------+
|   Smartphone /   | --------------------------> |    WeMos D1 R2      |
|     Laptop       |                             |   (Access Point)    |
|                  | <-------------------------- |   SSID: SaoPhoi-    |
|                  |     2. Tự động mở Portal    |         Setup       |
|                  |     (IP: 192.168.4.1)       |                     |
|                  | --------------------------> | 3. Lưu vào config   |
|                  |     Nhập SSID & Password    |    và khởi động lại |
+------------------+                             +---------------------+
```

1. **Kích hoạt chủ động:** Cấp nguồn cho mạch hoặc nhấn nút RST, sau đó **nhấn nút SW1 (D6) trong vòng 3 giây đầu** khởi động.
2. **Kích hoạt tự động:** Nếu mạch không kết nối được mạng Wi-Fi đã lưu sau 20 giây, chế độ Access Point sẽ tự động được kích hoạt trong 3 phút.
3. **Thao tác cấu hình:**
   - Dùng điện thoại kết nối vào mạng Wi-Fi mở: `SaoPhoi-Setup` (không cần mật khẩu).
   - Trình duyệt sẽ tự động bật trang cấu hình tại địa chỉ `http://192.168.4.1` (nhờ máy chủ Tiny DNS nội bộ).
   - Chọn tên Wi-Fi nhà bạn hoặc nhập SSID và mật khẩu.
   - Bấm **"Lưu cấu hình & Khởi động lại"**. Thiết bị sẽ tự động ghi đè thông tin mới vào `config.ini` và kết nối mạng.

---

## 🔄 10. Cập Nhật Từ Xa Over-The-Air (GitHub OTA)

Hệ thống tích hợp quy trình cập nhật mã nguồn từ xa an toàn qua GitHub:

1. **Cơ chế hoạt động:**
   - Firmware đọc tệp [`version.json`](version.json) từ nhánh `main` của kho lưu trữ GitHub để kiểm tra phiên bản mới.
   - Khi có phiên bản mới hoặc nhận lệnh `trigger_ota = true` từ Web Dashboard, tiến trình nạp sẽ tải từng tệp nguồn về bộ nhớ Flash dưới dạng file tạm `.tmp`.
   - Chỉ khi tệp tạm được tải đầy đủ và kiểm tra kích thước thành công, hệ thống mới tiến hành ghi đè lên tệp cũ.
   - Tệp cấu hình nhạy cảm (`config.ini`, `.env`) luôn được giữ nguyên vẹn trong suốt quá trình cập nhật.
2. **Khởi động lại sau cập nhật:** Sau khi nạp hoàn tất toàn bộ danh sách tệp, hệ thống cập nhật trạng thái `ota_status = "SUCCESS"` lên Firebase và tự động gọi `machine.reset()` để nạp firmware mới.

---

## ❓ 11. Xử Lý Sự Cố Thường Gặp (Troubleshooting)

### 1. Board ESP8266 liên tục khởi động lại khi cắm Servo SG90?
- **Nguyên nhân:** Động cơ Servo khi khởi động rút dòng tức thời lớn (có thể lên tới 500mA - 1A), gây sụt áp đường nguồn 5V/3.3V của ESP8266 dẫn đến Reset nguồn (Brownout).
- **Khắc phục:** Đấu một tụ hóa $100\mu\text{F}$ (16V hoặc 25V) song song giữa chân `5V` và `GND` gần nhất với chân nguồn của Servo như sơ đồ nguyên lý. Sử dụng củ sạc nguồn ngoài có dòng tối thiểu $1.5\text{A} - 2\text{A}$.

### 2. Thiết bị không đồng bộ được thời gian hoặc báo lỗi NTP?
- **Nguyên nhân:** Mạng Wi-Fi bị chặn cổng UDP 123 hoặc kết nối Internet bị gián đoạn.
- **Khắc phục:** Kiểm tra modem Wi-Fi xem có bật tường lửa chặn cổng NTP không. Mạch sẽ tự động thử đồng bộ lại NTP định kỳ mỗi 10 phút trong vòng lặp chính.

### 3. Web Dashboard hiển thị "Lỗi kết nối Firebase" hoặc không nhận dữ liệu?
- **Nguyên nhân:** Đường dẫn Firebase Database URL chưa chính xác hoặc Firebase Rules đang chặn quyền đọc/ghi.
- **Khắc phục:** 
  - Đảm bảo URL có dạng `https://<ten-du-an>-default-rtdb.firebaseio.com` hoặc `https://<ten-du-an>-default-rtdb.asia-southeast1.firebasedatabase.app`.
  - Mở Firebase Console > Realtime Database > Rules và kiểm tra xem quyền đọc/ghi đã được mở hay chưa.

### 4. Nút bấm SW1 (D6) không nhận lệnh hoặc bị dội phím?
- **Nguyên nhân:** Nhiễu cơ học của tiếp điểm nút bấm.
- **Khắc phục:** Firmware đã tích hợp thuật toán chống dội phần mềm (debounce 80ms) và phân tách sự kiện: nhấn ngắn ($<1\text{s}$) để đổi trạng thái sào, giữ lâu ($\ge 3\text{s}$) để reset vi điều khiển. Đảm bảo đã gắn trở kéo xuống $10\text{ k}\Omega$ vào chân D6.

---

## 📄 Bản Quyền & Giấy Phép
Dự án được phát triển phục vụ mục đích học tập, nghiên cứu và ứng dụng thực tế trong lĩnh vực IoT & Nhà thông minh. Mọi đóng góp (Pull Request), báo lỗi (Issues) đều được hoan nghênh!
