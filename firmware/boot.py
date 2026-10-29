# ==============================================================================
# boot.py - Khởi động hệ thống WeMos D1 (ESP8266) & Kết nối WiFi
# ==============================================================================
import gc
import network
import time
import config

gc.enable()

def connect_wifi():
    """Kết nối vào mạng WiFi theo cấu hình trong config.py"""
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    
    # Tắt Access Point để tiết kiệm RAM & tránh nhiễu
    if ap_if.active():
        ap_if.active(False)
        
    if not sta_if.isconnected():
        print(f"[*] Đang kết nối WiFi: {config.WIFI_SSID}...")
        sta_if.active(True)
        sta_if.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        
        timeout = 20  # Tối đa 20 giây
        while not sta_if.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
            print(".", end="")
        print()

    if sta_if.isconnected():
        print("[+] Kết nối WiFi thành công!")
        print("[+] Địa chỉ IP:", sta_if.ifconfig()[0])
    else:
        print("[!] Không thể kết nối WiFi. Vui lòng kiểm tra config.py")

# Thực hiện kết nối
connect_wifi()
gc.collect()
