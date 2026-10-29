// ==============================================================================
// config.js - Cấu hình Firebase & GitHub cho WebApp
// Người dùng có thể thay đổi trực tiếp tại đây hoặc qua giao diện cài đặt trên Web
// ==============================================================================

export const DEFAULT_CONFIG = {
  // 1. Cấu hình Firebase Realtime Database
  // Hãy thay thế bằng thông tin Firebase của bạn
  firebase: {
    apiKey: "YOUR_API_KEY",
    databaseURL: "https://your-project-id-default-rtdb.firebaseio.com",
    projectId: "your-project-id"
  },

  // 2. Cấu hình GitHub Repository phục vụ OTA
  github: {
    user: "chuvitvang",
    repo: "Iot_smart_drying_rack",
    branch: "main"
  }
};

// Lưu và lấy cấu hình từ LocalStorage để thuận tiện thử nghiệm trực tiếp trên trình duyệt
export function loadUserConfig() {
  const saved = localStorage.getItem("clothesline_config");
  if (saved) {
    try {
      return JSON.parse(saved);
    } catch (e) {
      console.error("Lỗi đọc cấu hình LocalStorage:", e);
    }
  }
  return DEFAULT_CONFIG;
}

export function saveUserConfig(cfg) {
  localStorage.setItem("clothesline_config", JSON.stringify(cfg));
}

