# ==============================================================================
# CẤU HÌNH HỆ THỐNG GIÀN PHƠI THÔNG MINH (WEMOS D1 R2 - ESP8266)
# ==============================================================================

# 1. Cấu hình WiFi
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

# 2. Cấu hình Firebase Realtime Database
# Định dạng: https://<your-project-id>-default-rtdb.firebaseio.com
FIREBASE_URL = "https://your-project-id-default-rtdb.firebaseio.com"
FIREBASE_AUTH = ""  # Để trống nếu Database ở chế độ test rules hoặc điền Database Secret

# 3. Cấu hình GitHub OTA
GITHUB_USER = "chuvitvang"
GITHUB_REPO = "Iot_smart_drying_rack"
GITHUB_BRANCH = "main"
GITHUB_RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}"
OTA_VERSION_URL = f"{GITHUB_RAW_BASE}/version.json"

# Phiên bản hiện hành của Firmware
CURRENT_VERSION = "1.0.0"

# 4. Sơ đồ chân GPIO (WeMos D1 R2)
PIN_I2C_SCL = 5   # D1 (GPIO 5) -> SCL ADS1115
PIN_I2C_SDA = 4   # D2 (GPIO 4) -> SDA ADS1115
PIN_DHT22   = 2   # D4 (GPIO 2) -> DATA DHT22
PIN_BUTTON  = 12  # D6 (GPIO 12) -> Nút nhấn SW1 (External Pull-up 10k)
PIN_SERVO   = 13  # D7 (GPIO 13) -> PWM Động cơ Servo SG90

# Kênh trên module ADS1115 (0x48)
ADC_CHANNEL_RAIN = 0  # A0: Cảm biến mưa (WATER_A0)
ADC_CHANNEL_LDR  = 1  # A1: Cảm biến quang trở (LDR_A1)

# 5. Ngưỡng mặc định điều khiển tự động
DEFAULT_RAIN_THRESHOLD  = 15000  # ADC < 15000 là có mưa (cần thu giàn phơi)
DEFAULT_LIGHT_THRESHOLD = 10000  # ADC > 10000 là đủ nắng (có thể phơi đồ)

# Góc quay Servo SG90 (Độ)
SERVO_ANGLE_OUT = 90  # Đưa giàn phơi ra ngoài
SERVO_ANGLE_IN  = 0   # Thu giàn phơi vào nhà

# Chu kỳ lặp vòng quét (giây)
LOOP_INTERVAL_SEC = 2.5
