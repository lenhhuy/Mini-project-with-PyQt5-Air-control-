# 🌬️ Acoustic Air Dashboard

## Hệ Thống Giám Sát & Điều Khiển Chất Lượng Không Khí Thông Minh

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

> **Đồ án môn học** | Trường Đại học Sư phạm Kỹ thuật TP.HCM (HCMUTE)  
> **Sinh viên:** Lê Nhật Huy | **MSSV:** 23119064  
> **Ngành:** Kỹ thuật Máy tính

---

## 📋 Mục Lục

- [Giới Thiệu](#-giới-thiệu)
- [Tính Năng](#-tính-năng)
- [Kiến Trúc Hệ Thống](#-kiến-trúc-hệ-thống)
- [Công Nghệ Sử Dụng](#-công-nghệ-sử-dụng)
- [Cài Đặt](#-cài-đặt)
- [Hướng Dẫn Sử Dụng](#-hướng-dẫn-sử-dụng)
- [Cấu Trúc Dự Án](#-cấu-trúc-dự-án)
- [API Integration](#-api-integration)
- [Ảnh Chụp Màn Hình](#-ảnh-chụp-màn-hình)
- [Phát Triển Trong Tương Lai](#-phát-triển-trong-tương-lai)
- [Tác Giả](#-tác-giả)

---

## 🎯 Giới Thiệu

**Acoustic Air Dashboard** là ứng dụng desktop thông minh được phát triển bằng PyQt5, cung cấp giải pháp toàn diện cho việc giám sát chất lượng không khí và điều khiển thiết bị môi trường trong nhà. Hệ thống tích hợp trí tuệ nhân tạo (AI) để phân tích dữ liệu và đưa ra khuyến nghị tự động, giúp người dùng duy trì môi trường sống lành mạnh.

### Vấn Đề Giải Quyết

- 🏭 Ô nhiễm không khí ngày càng nghiêm trọng tại các đô thị lớn
- 🔊 Tiếng ồn môi trường ảnh hưởng đến sức khỏe và năng suất làm việc
- 💧 Độ ẩm không phù hợp gây ra các vấn đề về hô hấp và nấm mốc
- ⚡ Thiếu hệ thống giám sát tập trung và tự động hóa

---

## ✨ Tính Năng

### 🔧 Điều Khiển Thiết Bị

| Thiết Bị | Chức Năng |
|----------|-----------|
| **Máy Lọc Không Khí** | 4 chế độ hoạt động (Save Energy → Power Boost), điều khiển qua slider |
| **Máy Hút Ẩm** | Bật/Tắt với hiển thị trạng thái trực quan |
| **Cửa Sổ Thông Minh** | Điều khiển đóng/mở tự động theo điều kiện môi trường |

### 📊 Giám Sát Thời Gian Thực

- **PM2.5**: Nồng độ bụi mịn (µg/m³) với chỉ báo trạng thái GOOD/POOR
- **CO**: Nồng độ Carbon Monoxide (ppm)
- **Noise Level**: Mức độ ồn môi trường (dB) - dữ liệu mô phỏng
- **Biểu đồ động**: Hiển thị lịch sử độ ồn với cảnh báo ngưỡng nguy hiểm

### 🤖 Trí Tuệ Nhân Tạo

- **Clean Score**: Tính toán điểm chất lượng không khí tổng hợp (0-100%)
- **Sound Classification**: Phân loại âm thanh môi trường
  - Quiet/Background Noise (< 45 dB)
  - Indoor Conversation (45-75 dB)
  - Loud Noise/Traffic (> 75 dB)
- **Smart Recommendations**: Đề xuất hành động tự động dựa trên phân tích dữ liệu

### 🌐 Tích Hợp Web

- **Dự báo thời tiết**: Nhúng các trang AccuWeather, Zoom Earth, Windy
- **QWebEngineView**: Hiển thị web trực tiếp trong ứng dụng
- **Multi-source**: Hỗ trợ nhiều nguồn dữ liệu thời tiết

### 🎵 Tính Năng Bổ Sung

- **Ambient Music**: Phát nhạc nền tạo không gian thư giãn
- **Animated Menu**: Menu điều hướng với hiệu ứng mượt mà
- **Real-time Clock**: Hiển thị thời gian hệ thống

---

## 🏗 Kiến Trúc Hệ Thống

```
┌─────────────────────────────────────────────────────────────┐
│                    ACOUSTIC AIR DASHBOARD                    │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   UI Layer  │  │ Logic Layer │  │    Data Layer       │  │
│  │  (PyQt5)    │◄─┤  (Python)   │◄─┤ (Weatherbit API)    │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    MODULES                               ││
│  ├──────────────┬──────────────┬──────────────┬────────────┤│
│  │ Device       │ Data         │ AI           │ Web        ││
│  │ Control      │ Visualization│ Analytics    │ Integration││
│  │ • Air Purifier│ • QChart    │ • Clean Score│ • Weather  ││
│  │ • Dehumidifier│ • Real-time │ • Sound Class│ • Forecast ││
│  │ • Smart Window│ • Animation │ • Recommend  │ • Multi-src││
│  └──────────────┴──────────────┴──────────────┴────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠 Công Nghệ Sử Dụng

### Core Framework
- **Python 3.8+**: Ngôn ngữ lập trình chính
- **PyQt5**: Framework GUI cho ứng dụng desktop

### Thư Viện PyQt5
| Module | Chức năng |
|--------|-----------|
| `QtWidgets` | Các widget giao diện người dùng |
| `QtCore` | Timer, Animation, Signal/Slot |
| `QtGui` | Đồ họa, Font, Color, Brush |
| `QtChart` | Biểu đồ thời gian thực |
| `QtMultimedia` | Phát nhạc nền |
| `QtWebEngineWidgets` | Nhúng trang web |

### External APIs
- **Weatherbit API**: Dữ liệu chất lượng không khí thời gian thực
- **AccuWeather/Windy/Zoom Earth**: Dự báo thời tiết

### Tools
- **Qt Designer**: Thiết kế giao diện (.ui files)
- **pyuic5**: Chuyển đổi UI sang Python code
- **pyrcc5**: Biên dịch resource files

---

## 📦 Cài Đặt

### Yêu Cầu Hệ Thống
- Python 3.8 trở lên
- Windows 10/11 (khuyến nghị) hoặc Linux/macOS
- RAM: 4GB+ (khuyến nghị 8GB)
- Kết nối Internet (cho API calls)

### Bước 1: Clone Repository
```bash
git clone https://github.com/your-username/acoustic-air-dashboard.git
cd acoustic-air-dashboard
```

### Bước 2: Tạo Virtual Environment (khuyến nghị)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### Bước 3: Cài Đặt Dependencies
```bash
pip install PyQt5
pip install PyQtWebEngine
pip install PyQtChart
pip install requests
```

Hoặc sử dụng requirements.txt:
```bash
pip install -r requirements.txt
```

### Bước 4: Biên Dịch Resource Files (nếu cần)
```bash
pyrcc5 aircondi_rc.qrc -o aircondi_rc.py
pyrcc5 humid_rc.qrc -o humid_rc.py
pyrcc5 window_rc.qrc -o window_rc.py
pyrcc5 logohcmuteimg_rc.qrc -o logohcmuteimg_rc.py
```

### Bước 5: Chạy Ứng Dụng
```bash
python final_main.py
```

---

## 📖 Hướng Dẫn Sử Dụng

### Điều Hướng Menu

1. **CONTROL DEVICE**: Điều khiển thiết bị
   - AIR PURIFIER: Máy lọc không khí
   - DEHUMIDIFIER: Máy hút ẩm
   - SMART WINDOW: Cửa sổ thông minh

2. **DATA AND ANALYTICS**: Dữ liệu và phân tích
   - REAL-TIME DATA: Dữ liệu thời gian thực
   - ANALYTICS: Biểu đồ phân tích
   - AI: Trí tuệ nhân tạo

### Điều Khiển Máy Lọc Không Khí

```
Slider Value    Chế Độ              Mô Tả
0               OFF                 Tắt máy
1-24            SAVE ENERGY         Tiết kiệm điện
25-49           MEDIUM              Chế độ trung bình
50-74           TURBO/BOOST         Chế độ mạnh
75-100          POWER BOOST         Công suất tối đa
```

### Đọc Hiểu Clean Score

| Điểm | Trạng Thái | Màu Sắc |
|------|------------|---------|
| 80-100% | Tuyệt vời | 🟢 Xanh lá |
| 50-79% | Chấp nhận được | 🟡 Vàng |
| 0-49% | Cần cải thiện | 🔴 Đỏ |

---

## 📁 Cấu Trúc Dự Án

```
acoustic-air-dashboard/
│
├── 📄 main.py                 # Phiên bản cơ bản
├── 📄 final_main.py           # Phiên bản hoàn chỉnh (CHẠY FILE NÀY)
├── 📄 uiair_dashboard.py      # UI class được generate từ Qt Designer
├── 📄 weather_window_ui.py    # UI cho cửa sổ thời tiết
│
├── 📁 resources/              # Tài nguyên
│   ├── 🖼️ icons/              # Icon thiết bị
│   ├── 🎵 music.wav           # Nhạc nền
│   └── 📄 *.qrc               # Qt Resource files
│
├── 📁 ui_files/               # Qt Designer files
│   ├── airpurifierdevice.ui
│   └── weather_window.ui
│
├── 📄 aircondi_rc.py          # Compiled resources
├── 📄 humid_rc.py
├── 📄 window_rc.py
├── 📄 logohcmuteimg_rc.py
│
├── 📄 requirements.txt        # Dependencies
├── 📄 README.md               # Tài liệu này
└── 📄 LICENSE                 # Giấy phép MIT
```

---

## 🔌 API Integration

### Weatherbit Air Quality API

**Endpoint:**
```
https://api.weatherbit.io/v2.0/current/airquality
```

**Parameters:**
| Param | Giá trị | Mô tả |
|-------|---------|-------|
| lat | 10.850301 | Vĩ độ TP.HCM |
| lon | 106.772024 | Kinh độ TP.HCM |
| key | YOUR_API_KEY | API key |

**Response Data:**
```json
{
  "data": [{
    "pm25": 35,
    "pm10": 50,
    "co": 250.5,
    "so2": 2.1,
    "no2": 15.3,
    "o3": 45.2,
    "aqi": 85
  }]
}
```

### Xử Lý Lỗi API
```python
try:
    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    # Fallback to mock data
    self.lbl_pm25_value_2.setText("PM2.5: CONNECTION FAILED")
```

---

## 📸 Ảnh Chụp Màn Hình

### Giao Diện Chính
```
<img width="1920" height="1080" alt="Screenshot 2025-12-31 110245" src="https://github.com/user-attachments/assets/4bd74332-8962-40c4-8ba6-4dc1720e3290" />

```

---

## 🚀 Phát Triển Trong Tương Lai

- [ ] **IoT Integration**: Kết nối với cảm biến thực tế qua MQTT/HTTP
- [ ] **Mobile App**: Phát triển ứng dụng Android/iOS companion
- [ ] **Cloud Storage**: Lưu trữ dữ liệu lịch sử trên cloud
- [ ] **Machine Learning**: Dự đoán chất lượng không khí bằng ML models
- [ ] **Voice Control**: Tích hợp điều khiển bằng giọng nói
- [ ] **Multi-room Support**: Hỗ trợ giám sát nhiều phòng
- [ ] **Energy Analytics**: Phân tích tiêu thụ điện năng

---

## 🧪 Testing

```bash
# Chạy ứng dụng ở chế độ debug
python final_main.py

# Kiểm tra log trong terminal
# Các thông báo LOG: sẽ hiển thị trạng thái hoạt động
```

---

## 🤝 Đóng Góp

Mọi đóng góp đều được hoan nghênh! Vui lòng:

1. Fork dự án
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

---

## 📄 License

Dự án này được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.

---

## 👨‍💻 Tác Giả

<div align="center">

**Lê Nhật Huy**

[![Student](https://img.shields.io/badge/MSSV-23119064-blue?style=flat-square)](https://hcmute.edu.vn)
[![Major](https://img.shields.io/badge/Ngành-Kỹ_thuật_Máy_tính-green?style=flat-square)](https://hcmute.edu.vn)
[![University](https://img.shields.io/badge/Trường-HCMUTE-red?style=flat-square)](https://hcmute.edu.vn)

*Trường Đại học Sư phạm Kỹ thuật TP. Hồ Chí Minh*

</div>

---

<div align="center">

**⭐ Nếu dự án hữu ích, hãy cho một star nhé! ⭐**

Made with ❤️ in Ho Chi Minh City, Vietnam

</div>
