import sys
import random
import requests
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QPushButton, QWidget, QLabel, QFrame, QMessageBox)
from PyQt5.QtCore import QTimer, QPointF, Qt, QDateTime
from PyQt5.QtGui import QPainter, QPen, QLinearGradient, QGradient, QColor, QBrush, QFont, QIcon
# Thư viện cho Biểu đồ
from PyQt5.QtChart import (QChart, QChartView, QLineSeries, QValueAxis)
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

# Import UI Class từ file đã được sinh ra bởi pyuic5
from uiair_dashboard import Ui_MainWindow

# =============================================================================
# QUAN TRỌNG: Import QWebEngineView (cần cài PyQtWebEngine)
# Chạy lệnh: pip install PyQtWebEngine
# =============================================================================
try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView

    WEB_ENGINE_AVAILABLE = True
except ImportError:
    WEB_ENGINE_AVAILABLE = False
    print("⚠️ WARNING: PyQtWebEngine chưa được cài đặt!")
    print("   Chạy lệnh: pip install PyQtWebEngine")

# =============================================================================
# Import Weather Window UI (từ file weather_window_ui.py)
# File này được tạo bằng lệnh: pyuic5 -x weather_window.ui -o weather_window_ui.py
# =============================================================================
try:
    from weather_window_ui import Ui_WeatherWindow

    WEATHER_UI_AVAILABLE = True
except ImportError:
    WEATHER_UI_AVAILABLE = False
    print("⚠️ WARNING: weather_window_ui.py chưa tồn tại!")
    print("   Tạo file bằng lệnh: pyuic5 -x weather_window.ui -o weather_window_ui.py")

# Định nghĩa các hằng số API
WEATHERBIT_API_KEY = "a3d871d078f5487ea20dbce5cfa901bd"
LATITUDE = "10.850301"  # Vĩ độ (HCM City)
LONGITUDE = "106.772024"  # Kinh độ

# Danh sách các trang web thời tiết
WEATHER_URLS = {
    'accuweather': "https://www.accuweather.com/vi/vn/ho-chi-minh-city/353981/weather-forecast/353981",
    'weathercom': "https://zoom.earth/places/vietnam/ho-chi-minh-city/",
    'windy': "https://www.windy.com/10.850/106.772?10.850,106.772,11",
    'openweather': "https://bongda24h.vn/bong-da-anh/bang-xep-hang-1.html"
}


# =============================================================================
# LỚP CỬA SỔ WEATHER WEB (Sử dụng UI từ Qt Designer)
# =============================================================================
class WeatherWebWindow(QMainWindow):
    """
    Cửa sổ hiển thị trang web dự báo thời tiết.
    Sử dụng UI từ weather_window.ui (nếu có) hoặc tạo bằng code.
    """
    MU_JOKES = [
        "MU là vô đối... ở giữa bảng xếp hạng",
        "Đang kiểm tra xem hang đã đóng chưa...",
        "10 khó vẫn đang ổn, đừng lo!",
        "Gáy lên anh em ơi, 1-0 cho đối thủ!"
    ]

    def load_openweather(self):
        """Tải OpenWeather với status đặc biệt"""
        # Đánh dấu đang ở OpenWeather
        self.is_openweather = True

        # Hiển thị câu joke ngẫu nhiên
        if hasattr(self, 'lbl_status'):
            joke = random.choice(self.MU_JOKES)
            self.lbl_status.setText(f"⚽ {joke}")
            self.lbl_status.setStyleSheet("color: #E74C3C; font-size: 12px; padding: 5px; font-weight: bold;")

        # Load URL
        if hasattr(self, 'web_view'):
            self.web_view.setUrl(QUrl(WEATHER_URLS['openweather']))
    def __init__(self, parent=None):
        super().__init__(parent)

        # Kiểm tra xem có UI file không
        if WEATHER_UI_AVAILABLE and WEB_ENGINE_AVAILABLE:
            self.setup_from_ui_file()
        elif WEB_ENGINE_AVAILABLE:
            self.setup_from_code()
        else:
            self.setup_fallback()

    def setup_from_ui_file(self):
        """Thiết lập từ file UI (weather_window_ui.py)"""
        # Áp dụng UI
        self.ui = Ui_WeatherWindow()
        self.ui.setupUi(self)

        # Nhúng WebView vào web_container
        self.setup_web_view(self.ui.web_container)

        # Kết nối các nút
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_refresh.clicked.connect(self.refresh_page)
        self.ui.btn_accuweather.clicked.connect(lambda: self.load_url(WEATHER_URLS['accuweather']))
        self.ui.btn_weathercom.clicked.connect(lambda: self.load_url(WEATHER_URLS['weathercom']))
        self.ui.btn_windy.clicked.connect(lambda: self.load_url(WEATHER_URLS['windy']))
        self.ui.btn_openweather.clicked.connect(self.load_openweather)

        # Lưu reference đến status label
        self.lbl_status = self.ui.lbl_status

        print("LOG: Weather Window đã được khởi tạo từ UI file.")
        self.is_openweather = False

    def setup_from_code(self):
        """Thiết lập bằng code Python (backup nếu không có UI file)"""
        self.setWindowTitle("🌤️ Dự Báo Thời Tiết - Weather Forecast")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)

        # Widget trung tâm
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # ===== HEADER =====
        frame_header = QFrame()
        frame_header.setStyleSheet("background-color: #34495E; border-radius: 10px;")
        frame_header.setFixedHeight(60)
        header_layout = QHBoxLayout(frame_header)

        lbl_title = QLabel("🌤️ DỰ BÁO THỜI TIẾT")
        lbl_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        header_layout.addWidget(lbl_title)
        header_layout.addStretch()

        self.btn_refresh = QPushButton("🔄 Làm mới")
        self.btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #3498DB; color: white; font-size: 14px;
                font-weight: bold; padding: 8px 20px; border-radius: 8px;
            }
            QPushButton:hover { background-color: #2980B9; }
        """)
        self.btn_refresh.clicked.connect(self.refresh_page)
        header_layout.addWidget(self.btn_refresh)

        self.btn_close = QPushButton("❌ Đóng")
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C; color: white; font-size: 14px;
                font-weight: bold; padding: 8px 20px; border-radius: 8px;
            }
            QPushButton:hover { background-color: #C0392B; }
        """)
        self.btn_close.clicked.connect(self.close)
        header_layout.addWidget(self.btn_close)

        main_layout.addWidget(frame_header)

        # ===== URL BAR =====
        frame_url_bar = QFrame()
        frame_url_bar.setStyleSheet("background-color: #ECF0F1; border-radius: 8px;")
        frame_url_bar.setFixedHeight(50)
        url_layout = QHBoxLayout(frame_url_bar)

        url_label = QLabel("Chọn nguồn:")
        url_label.setStyleSheet("font-weight: bold; color: #2C3E50;")
        url_layout.addWidget(url_label)

        # Các nút chọn trang web
        websites = [
            ("AccuWeather", 'accuweather'),
            ("Zoom Earth", 'weathercom'),
            ("Windy", 'windy'),
            ("Giải cứu MU", 'openweather')
        ]

        for name, key in websites:
            btn = QPushButton(name)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498DB; color: white; font-size: 12px;
                    padding: 6px 15px; border-radius: 5px;
                }
                QPushButton:hover { background-color: #2980B9; }
            """)
            # Xử lý riêng cho OpenWeather
            if key == 'openweather':
                btn.clicked.connect(self.load_openweather)
            else:
                btn.clicked.connect(lambda checked, k=key: self.load_url(WEATHER_URLS[k]))
            url_layout.addWidget(btn)

        url_layout.addStretch()
        main_layout.addWidget(frame_url_bar)

        # ===== WEB CONTAINER =====
        web_container = QWidget()
        web_container.setStyleSheet("background-color: white; border-radius: 10px; border: 2px solid #BDC3C7;")
        self.setup_web_view(web_container)
        main_layout.addWidget(web_container)

        # ===== STATUS BAR =====
        self.lbl_status = QLabel("✅ Sẵn sàng")
        self.lbl_status.setStyleSheet("color: #27AE60; font-size: 12px; padding: 5px;")
        main_layout.addWidget(self.lbl_status)

        print("LOG: Weather Window đã được khởi tạo bằng code.")

    def setup_fallback(self):
        """Thiết lập fallback khi không có WebEngine"""
        self.setWindowTitle("⚠️ Cần Cài Đặt PyQtWebEngine")
        self.setGeometry(200, 200, 500, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Thông báo lỗi
        lbl_error = QLabel("⚠️ PyQtWebEngine chưa được cài đặt!")
        lbl_error.setStyleSheet("font-size: 18px; font-weight: bold; color: #E74C3C;")
        lbl_error.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_error)

        lbl_instruction = QLabel("Chạy lệnh sau để cài đặt:\n\npip install PyQtWebEngine")
        lbl_instruction.setStyleSheet("font-size: 14px; color: #2C3E50;")
        lbl_instruction.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_instruction)

        btn_close = QPushButton("Đóng")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)

        self.lbl_status = QLabel("❌ WebEngine không khả dụng")

    def setup_web_view(self, container):
        """Nhúng QWebEngineView vào container"""
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl(WEATHER_URLS['accuweather']))

        # Kết nối tín hiệu loading
        self.web_view.loadStarted.connect(self.on_load_started)
        self.web_view.loadFinished.connect(self.on_load_finished)

        # Thêm vào container
        layout = QVBoxLayout(container)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.web_view)

    def load_url(self, url):
        """Tải URL mới"""
        # Reset flag khi chuyển sang trang khác
        self.is_openweather = False

        if hasattr(self, 'web_view'):
            self.web_view.setUrl(QUrl(url))
            print(f"LOG: Đang tải: {url}")

    def refresh_page(self):
        """Làm mới trang"""
        if hasattr(self, 'web_view'):
            self.web_view.reload()
            print("LOG: Đang làm mới trang...")

    def on_load_started(self):
        """Khi bắt đầu tải"""
        if hasattr(self, 'lbl_status'):
            self.lbl_status.setText("⏳ Đang tải trang...")
            self.lbl_status.setStyleSheet("color: #F39C12; font-size: 12px; padding: 5px;")

    def on_load_finished(self, ok):
        """Khi tải xong"""
        if hasattr(self, 'lbl_status'):
            # Nếu đang ở OpenWeather -> giữ nguyên status joke
            if self.is_openweather:
                joke = random.choice(self.MU_JOKES)
                self.lbl_status.setText(f"⚽ {joke}")
                self.lbl_status.setStyleSheet("color: #E74C3C; font-size: 12px; padding: 5px; font-weight: bold;")
                return

            # Các trang khác -> hiển thị bình thường
            if ok:
                self.lbl_status.setText("✅ Tải trang thành công!")
                self.lbl_status.setStyleSheet("color: #27AE60; font-size: 12px; padding: 5px;")
            else:
                self.lbl_status.setText("❌ Lỗi khi tải trang!")
                self.lbl_status.setStyleSheet("color: #E74C3C; font-size: 12px; padding: 5px;")

    def closeEvent(self, event):
        """Khi đóng cửa sổ"""
        print("LOG: Đã đóng cửa sổ Weather Web.")
        event.accept()


# =============================================================================
# LỚP ỨNG DỤNG CHÍNH
# =============================================================================
class AcousticAirApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # ==========================================================
        # 1. KHỞI TẠO CÁC BIẾN
        # ==========================================================
        self.noise_history = []
        self.MAX_DATA_POINTS = 60
        self.weather_window = None  # Lưu reference đến cửa sổ Weather

        # 2. GỌI CÁC HÀM KHỞI TẠO
        self.setup_chart()
        self.setup_logic()

        # 3. Khởi tạo QMediaPlayer
        self.player = QMediaPlayer()

        # 4. Thiết lập logic kết nối nút bấm
        self.setup_music_logic()

        # 5. THÊM MỚI: Thiết lập nút Weather
        self.setup_weather_button()

    # =========================================================================
    # PHẦN MỚI: WEATHER BUTTON
    # =========================================================================
    def setup_weather_button(self):
        """Thiết lập nút mở cửa sổ Weather Web"""

        # Tạo nút Weather
        self.btn_weather = QPushButton("🌤️")
        self.btn_weather.setToolTip("Mở Dự báo Thời tiết")
        self.btn_weather.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                font-size: 16px;
                padding: 5px 10px;
                border-radius: 8px;
                border: none;
                min-width: 40px;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #2ECC71;
            }
            QPushButton:pressed {
                background-color: #1E8449;
            }
        """)

        # Kết nối sự kiện click
        self.btn_weather.clicked.connect(self.open_weather_window)

        # Thêm nút vào frame_12 (thanh header)
        if hasattr(self, 'frame_12') and self.frame_12.layout():
            self.frame_12.layout().insertWidget(0, self.btn_weather)
            print("LOG: Đã thêm nút Weather vào giao diện.")
        else:
            print("WARNING: Không tìm thấy frame_12!")

    def open_weather_window(self):
        """Mở cửa sổ Weather Web"""
        if self.weather_window is None or not self.weather_window.isVisible():
            self.weather_window = WeatherWebWindow(self)
            self.weather_window.show()
            print("LOG: Đã mở cửa sổ Weather Web.")
        else:
            self.weather_window.raise_()
            self.weather_window.activateWindow()
            print("LOG: Cửa sổ Weather Web đã được kích hoạt.")

    # =========================================================================
    # CÁC HÀM CŨ (GIỮ NGUYÊN)
    # =========================================================================
    def on_btn_open_web_clicked(self):
        self.stackedWidget.setCurrentIndex(6)

    def setup_music_logic(self):
        self.btn_play_music.setCheckable(True)
        self.btn_play_music.clicked.connect(self.toggle_music)

    def toggle_music(self):
        if self.btn_play_music.isChecked():
            url = QUrl.fromLocalFile("music.wav")
            content = QMediaContent(url)
            self.player.setMedia(content)
            self.player.play()
            self.btn_play_music.setText("⏸ Dừng nhạc")
            self.btn_play_music.setStyleSheet("background-color: #E67E22; color: white; border-radius: 10px;")
            print("LOG: Đang phát nhạc")
        else:
            self.player.stop()
            self.btn_play_music.setText("▶ Phát nhạc")
            self.btn_play_music.setStyleSheet("background-color: #3498DB; color: white; border-radius: 10px;")
            print("LOG: Đã dừng nhạc.")

    def setup_logic(self):
        """Khởi tạo các kết nối tín hiệu và Timer"""

        # --- 1. KẾT NỐI CONTROLS ---
        self.chk_air_purifier_2.setCheckable(True)
        self.chk_air_purifier_2.toggled.connect(self.control_air_purifier)
        self.chk_air_purifier_2.setText("MÁY LỌC")
        self.sld_purifier_mode_2.valueChanged.connect(self.change_purifier_mode)
        self.chk_dehumidifier_2.toggled.connect(self.control_dehumidifier)
        self.chk_smart_windows_2.toggled.connect(self.control_smart_windows)
        self.chk_dehumidifier_2.setText("Máy hút ẩm: OFF")
        self.chk_smart_windows_2.setText("Cửa sổ: ĐÓNG")

        # Menu
        self.btn_toggle_menu.clicked.connect(self.toggle_side_menu)

        # --- 2. TIMER CẬP NHẬT DỮ LIỆU ---
        self.data_timer = QTimer(self)
        self.data_timer.timeout.connect(self.update_live_data)
        self.data_timer.start(5000)

        # --- 3. TIMER CẬP NHẬT ĐỒNG HỒ ---
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

        # --- KẾT NỐI CÁC NÚT BẤM ---
        self.nut1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.nut2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.nut3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.nut4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.nut5.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.nut6.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))

        self.stackedWidget.setCurrentIndex(0)

        self.menu_buttons = [self.nut1, self.nut2, self.nut3, self.nut4, self.nut5, self.nut6]

        for i, btn in enumerate(self.menu_buttons):
            btn.clicked.connect(lambda checked, index=i, button=btn: self.switch_page(index, button))

        self.update_live_data()
        self.update_clock()

    def switch_page(self, index, clicked_button):
        """Chuyển trang và đổi màu nút"""
        self.stackedWidget.setCurrentIndex(index)

        for btn in self.menu_buttons:
            btn.setStyleSheet("background-color: transparent; color: black; border: none;")

        clicked_button.setStyleSheet("""
            background-color: #3498DB; 
            color: white; 
            font-weight: bold; 
            border-radius: 5px;
        """)

    def toggle_side_menu(self):
        """Ẩn/hiện thanh menu với animation"""
        width = self.frame.width()
        new_width = 200 if width == 0 else 0

        self.animation = QPropertyAnimation(self.frame, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def get_mock_data(self):
        """Mô phỏng dữ liệu cảm biến"""
        return {
            'pm25': random.randint(10, 60),
            'co': round(random.uniform(0.1, 8.0), 1),
            'noise': random.randint(35, 75),
            'humidity': random.randint(30, 80),
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }

    def calculate_clean_score(self, pm25, co, noise, humidity):
        """Tính Clean Score"""
        score = 100
        if pm25 > 50:
            score -= 40
        elif pm25 > 25:
            score -= 20
        if co > 5.0:
            score -= 30
        elif co > 2.0:
            score -= 15
        if noise > 60:
            score -= 15
        elif noise > 45:
            score -= 8
        if humidity < 40 or humidity > 70:
            score -= 10
        elif humidity < 45 or humidity > 65:
            score -= 5
        return max(0, min(100, score))

    def get_air_icon_style(self, is_checked, slider_value):
        """Trả về stylesheet cho icon"""
        PATH_OFF = "image: url(:/air/power-on.png);"
        PATH_LV1 = "image: url(:/air/airconditionercool.png)"
        PATH_LV2 = "image: url(:/air/wind.png);"
        PATH_LV3 = "image: url(:/air/mode2.png);"
        PATH_LV4 = "image: url(:/air/mode3.png);"

        if not is_checked or slider_value == 0:
            return PATH_OFF
        elif 0 < slider_value <= 24:
            return PATH_LV1
        elif 25 <= slider_value <= 49:
            return PATH_LV2
        elif 50 <= slider_value <= 74:
            return PATH_LV3
        else:
            return PATH_LV4

    def control_air_purifier(self, checked):
        """Điều khiển Máy lọc không khí"""
        current_slider_value = self.sld_purifier_mode_2.value()

        if checked:
            print("LOG: Máy Lọc Không Khí ĐÃ BẬT.")
            if current_slider_value == 0:
                self.sld_purifier_mode_2.setValue(25)
                current_slider_value = 25
            self.chk_air_purifier_2.setText("MÁY LỌC: ON")
            self.chk_air_purifier_2.setStyleSheet("""
                QPushButton {
                    background-color: #27AE60; color: white; font-weight: bold; 
                    border-radius: 10px; border: 2px solid #8E44AD;
                }
            """)
        else:
            print("LOG: Máy Lọc Không Khí ĐÃ TẮT.")
            self.sld_purifier_mode_2.setValue(0)
            current_slider_value = 0
            self.chk_air_purifier_2.setText("MÁY LỌC: OFF")
            self.chk_air_purifier_2.setStyleSheet("""
                QPushButton {
                    background-color: #95A5A6; color: white; 
                    border-radius: 10px; border: 2px solid #7F8C8D;
                }
            """)

        try:
            new_style = self.get_air_icon_style(checked, current_slider_value)
            self.airicon.setStyleSheet(new_style)
        except AttributeError:
            print("Lỗi: Không tìm thấy 'airicon'.")

    def control_dehumidifier(self, checked):
        """Điều khiển Máy hút ẩm"""
        if checked:
            self.chk_dehumidifier_2.setText("Máy hút ẩm: ON")
            self.chk_dehumidifier_2.setStyleSheet(
                "background-color: #2ECC71; color: white; font-weight: bold; border-radius: 8px;")
            self.label_5.setStyleSheet("image: url(:/humid/doamon.png);")
            print("LOG: Đã bật Máy hút ẩm.")
        else:
            self.chk_dehumidifier_2.setText("Máy hút ẩm: OFF")
            self.chk_dehumidifier_2.setStyleSheet("background-color: #E74C3C; color: white; border-radius: 8px;")
            self.label_5.setStyleSheet("image: url(:/humid/doamoff.png);")
            print("LOG: Đã tắt Máy hút ẩm.")

    def change_purifier_mode(self, mode_value):
        """Điều khiển chế độ Máy lọc"""
        is_checked = (mode_value > 0)

        if mode_value == 0:
            self.chk_air_purifier_2.setChecked(False)
            current_mode = "OFF"
        else:
            self.chk_air_purifier_2.setChecked(True)
            if 0 < mode_value <= 24:
                current_mode = "MỨC 1: SAVE ENERGY"
            elif 25 <= mode_value <= 49:
                current_mode = "MỨC 2: MEDIUM"
            elif 50 <= mode_value <= 74:
                current_mode = "MỨC 3: TURBO"
            else:
                current_mode = "MỨC 4: POWER BOOST"

        print(f"LOG: Chế độ: {current_mode} (Value: {mode_value})")

        try:
            new_style = self.get_air_icon_style(is_checked, mode_value)
            self.airicon.setStyleSheet(new_style)
        except AttributeError:
            pass

    def control_smart_windows(self, checked):
        """Điều khiển Cửa sổ thông minh"""
        if checked:
            self.chk_smart_windows_2.setText("Cửa sổ: MỞ")
            self.chk_smart_windows_2.setStyleSheet(
                "background-color: #3498DB; color: white; font-weight: bold; border-radius: 5px;")
            self.label.setStyleSheet("image: url(:/window/windows.png);")
            print("LOG: Đã mở cửa sổ.")
        else:
            self.chk_smart_windows_2.setText("Cửa sổ: ĐÓNG")
            self.chk_smart_windows_2.setStyleSheet("background-color: #7F8C8D; color: white; border-radius: 5px;")
            self.label.setStyleSheet("image: url(:/window/window.png);")
            print("LOG: Đã đóng cửa sổ.")

    def update_clock(self):
        """Cập nhật đồng hồ"""
        current_time = QDateTime.currentDateTime()
        time_display = current_time.toString("hh:mm:ss\nddd dd/MM/yyyy")
        try:
            self.lbl_current_time.setText(time_display)
        except AttributeError:
            pass

    def update_live_data(self):
        """Cập nhật dữ liệu thời gian thực"""
        air_data = self.get_mock_data()

        pm25 = air_data.get('pm25', 0)
        co = air_data.get('co', 0.0)
        noise = air_data.get('noise', 0)
        humidity = air_data.get('humidity', 0)

        clean_score = self.calculate_clean_score(pm25, co, noise, humidity)

        try:
            self.lbl_clean_score_value.setText(f"{clean_score}%")
            if clean_score >= 80:
                score_color = "color: #388e3c;"
            elif clean_score >= 50:
                score_color = "color: #fdd835;"
            else:
                score_color = "color: #d32f2f;"
            self.lbl_clean_score_value.setStyleSheet(f"font-weight: bold; {score_color}")
        except AttributeError:
            pass

        # Gọi API
        API_URL = "https://api.weatherbit.io/v2.0/current/airquality"
        params = {'lat': LATITUDE, 'lon': LONGITUDE, 'key': WEATHERBIT_API_KEY}

        try:
            response = requests.get(API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data and data.get('data'):
                air_data = data['data'][0]
                pm25 = int(air_data.get('pm25', 0))
                co = float(air_data.get('co', 0)) / 1000
                noise_level = random.randint(35, 90)

                self.lbl_pm25_value_2.setText(f"PM2.5: {pm25} µg/m³")
                self.lbl_noise_value_2.setText(f"NOISE: {noise_level} dB\n(Random)")
                self.lbl_voc_value_2.setText(f"CO: {co:.2f} ppm")

                status_text = "GOOD"
                status_color = "color: #388e3c;"
                if pm25 > 50:
                    status_text = "POOR"
                    status_color = "color: #d32f2f;"

                self.lbl_pm25_status_2.setText(status_text)
                self.lbl_pm25_status_2.setStyleSheet(f"{status_color} border-radius: 5px; padding: 2px;")

                self.update_chart_data(noise_level)
                self.run_ai_analytics(noise_level, pm25)

        except requests.exceptions.RequestException as e:
            print(f"Lỗi API: {e}")
            self.lbl_pm25_value_2.setText("PM2.5: CONNECTION FAILED")
        except Exception as e:
            print(f"Lỗi: {e}")

    def run_ai_analytics(self, noise, pm25):
        """Phân tích AI"""
        if noise < 45:
            sound_class = "QUIET / BACKGROUND NOISE"
        elif 45 <= noise < 75:
            sound_class = "INDOOR CONVERSATION"
        else:
            sound_class = "LOUD NOISE / TRAFFIC"

        self.lbl_ai_sound_class_2.setText(f"CURRENT SOUND:\n{sound_class}")

        recommendation = "ALL SYSTEMS OPTIMAL."
        if pm25 > 50 and not self.chk_air_purifier_2.isChecked():
            recommendation = "HIGH PM2.5!\nTURN ON AIR PURIFIER!"
        elif noise > 75 and self.chk_smart_windows_2.isChecked():
            recommendation = "DANGER NOISE!\nCLOSE SMART WINDOWS."

        self.lbl_noise_value_4.setText(f"RECOMMENDATION:\n{recommendation}")

    def setup_chart(self):
        """Khởi tạo biểu đồ"""
        self.series = QLineSeries()

        self.pen_safe = QPen(QColor("#2ECC71"))
        self.pen_safe.setWidth(3)
        self.pen_danger = QPen(QColor("#E74C3C"))
        self.pen_danger.setWidth(4)

        self.series.setPen(self.pen_safe)

        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.addSeries(self.series)
        self.chart.setTitle("HỆ THỐNG GIÁM SÁT ĐỘ ỒN")
        self.chart.setBackgroundRoundness(15)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        self.axis_x = QValueAxis()
        self.axis_x.setRange(0, self.MAX_DATA_POINTS)
        self.axis_x.setLabelFormat("%i")
        self.axis_x.setGridLineVisible(False)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)

        self.axis_y = QValueAxis()
        self.axis_y.setRange(30, 100)
        self.axis_y.setGridLineColor(QColor("#EEEEEE"))
        self.axis_y.setTitleText("Mức độ âm thanh (dB)")
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setStyleSheet("background: transparent; border: none;")

        if self.chart_widget_2.layout() is None:
            layout = QVBoxLayout(self.chart_widget_2)
            layout.setContentsMargins(5, 5, 5, 5)
            layout.addWidget(self.chart_view)
        else:
            self.chart_widget_2.layout().addWidget(self.chart_view)

    def update_chart_data(self, new_noise_level):
        """Cập nhật dữ liệu biểu đồ"""
        self.noise_history.append(new_noise_level)
        if len(self.noise_history) > self.MAX_DATA_POINTS:
            self.noise_history.pop(0)

        self.series.clear()
        points = [QPointF(i, value) for i, value in enumerate(self.noise_history)]
        self.series.append(points)
        self.chart.axisX().setRange(0, len(self.noise_history))

        # Đổi màu theo ngưỡng
        if new_noise_level >= 80:
            self.series.setPen(self.pen_danger)
            self.chart.setTitleBrush(QBrush(QColor("#E74C3C")))
            self.chart.setTitle("⚠️ CẢNH BÁO: ĐỘ ỒN QUÁ CAO!")
        else:
            self.series.setPen(self.pen_safe)
            self.chart.setTitleBrush(QBrush(QColor("#2C3E50")))
            self.chart.setTitle("HỆ THỐNG GIÁM SÁT ĐỘ ỒN")


# =============================================================================
# CHẠY ỨNG DỤNG
# =============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AcousticAirApp()
    window.show()
    sys.exit(app.exec_())