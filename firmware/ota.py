# ==============================================================================
# ota.py - Module Quản lý Cập nhật Firmware từ xa qua GitHub (OTA)
# ==============================================================================
import gc
import os
import machine
import urequests
import config

def update_firebase_ota_status(status, trigger_update=None, current_version=None):
    """Cập nhật trạng thái tiến trình OTA lên Firebase Realtime Database"""
    try:
        url = f"{config.FIREBASE_URL}/smart_clothesline/ota.json"
        if config.FIREBASE_AUTH:
            url += f"?auth={config.FIREBASE_AUTH}"
            
        payload = {"status": status}
        if trigger_update is not None:
            payload["trigger_update"] = trigger_update
        if current_version is not None:
            payload["current_version"] = current_version

        res = urequests.patch(url, json=payload)
        res.close()
    except Exception as e:
        print("[OTA] Lỗi khi cập nhật trạng thái Firebase:", e)
    finally:
        gc.collect()

def download_file(file_url, target_path):
    """Tải một file từ GitHub Raw và lưu vào hệ thống tệp Flash của ESP8266"""
    print(f"[OTA] Đang tải từ: {file_url} -> {target_path}...")
    temp_path = target_path + ".tmp"
    
    res = None
    try:
        res = urequests.get(file_url)
        if res.status_code != 200:
            print(f"[OTA] HTTP Error {res.status_code}")
            return False

        # Ghi nội dung vào file tạm
        with open(temp_path, "wb") as f:
            f.write(res.content)
            
        res.close()
        res = None
        gc.collect()

        # Kiểm tra kích thước file tải về
        stat = os.stat(temp_path)
        if stat[6] == 0:
            print("[OTA] File rỗng! Hủy bỏ.")
            try:
                os.remove(temp_path)
            except:
                pass
            return False

        # Thay thế file cũ an toàn
        try:
            os.remove(target_path)
        except OSError:
            pass # File đích chưa tồn tại
            
        os.rename(temp_path, target_path)
        print(f"[OTA] Đã cập nhật thành công: {target_path} ({stat[6]} bytes)")
        return True

    except Exception as e:
        print(f"[OTA] Lỗi trong quá trình tải {target_path}:", e)
        try:
            os.remove(temp_path)
        except:
            pass
        return False
    finally:
        if res:
            res.close()
        gc.collect()

def perform_ota(ota_data):
    """
    Thực hiện quy trình OTA:
    1. Đổi status thành DOWNLOADING
    2. Tải main.py (và các file cần thiết) từ GitHub
    3. Đổi status thành SUCCESS, cập nhật version
    4. Reset vi điều khiển
    """
    target_version = ota_data.get("target_version", config.CURRENT_VERSION)
    download_url = ota_data.get("download_url") or f"{config.GITHUB_RAW_BASE}/firmware/main.py"

    print(f"[*] Bắt đầu tiến trình OTA lên phiên bản {target_version}...")
    update_firebase_ota_status("DOWNLOADING")

    success = download_file(download_url, "main.py")

    if success:
        print("[+] Cập nhật thành công! Chuẩn bị khởi động lại thiết bị...")
        update_firebase_ota_status(
            status="SUCCESS",
            trigger_update=False,
            current_version=target_version
        )
        import time
        time.sleep(1)
        machine.reset()
    else:
        print("[-] Cập nhật OTA thất bại!")
        update_firebase_ota_status(
            status="FAILED",
            trigger_update=False
        )

