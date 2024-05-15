import sys
from PyQt5.QtCore import QUrl, Qt, QTimer, QPropertyAnimation, QPoint, QEasingCurve
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QSizePolicy,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QTabWidget,
    QSplashScreen,
    QLabel,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__(QPixmap("C:/Users/4Dhes/OneDrive/Documents/phyton project/web/icons/Liminal.png"))

        desktop = QApplication.primaryScreen()
        screen_rect = desktop.availableGeometry()
        splash_rect = self.rect()
        self.move((screen_rect.width() - splash_rect.width()) // 2, (screen_rect.height() - splash_rect.height()) // 2)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close)
        self.timer.start(1000)  # Initial delay before animation starts

        self.show()

    def closeEvent(self, event):
        # Stop the timer when closing the splash screen
        self.timer.stop()
        super().closeEvent(event)

class Browser(QWidget):
    def __init__(self, tab_widget, main_browser=None):
        super().__init__()

        self.browser = QWebEngineView()
        self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.tab_widget = tab_widget
        self.main_browser = main_browser

        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap("C:/Users/4Dhes/OneDrive/Documents/phyton project/web/icons/Liminal.png"))
        self.logo_label.setAlignment(Qt.AlignTop)  # Set alignment to top
        self.logo_label.setScaledContents(True)  # Allow the label to scale the image

        self.logo_animation = QPropertyAnimation(self.logo_label, b"pos")
        self.logo_animation.setStartValue(self.logo_label.pos())
        self.logo_animation.setEndValue(QPoint(0, 0))
        self.logo_animation.setEasingCurve(QEasingCurve.OutQuad)
        self.logo_animation.setDuration(2000)  # Animation duration in milliseconds

        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Enter URL and press Enter")
        self.address_bar.returnPressed.connect(self.navigate_to_url)

        font_size = 14

        self.create_tab_button = QPushButton("New Tab")
        font = self.create_tab_button.font()
        font.setBold(True)
        font.setPointSize(font_size)
        self.create_tab_button.setFont(font)
        self.create_tab_button.clicked.connect(self.create_new_tab)

        self.back_button = QPushButton("Back")
        font = self.back_button.font()
        font.setPointSize(font_size)
        self.back_button.setFont(font)
        self.back_button.clicked.connect(self.browser.back)

        self.forward_button = QPushButton("Forward")
        font = self.forward_button.font()
        font.setPointSize(font_size)
        self.forward_button.setFont(font)
        self.forward_button.clicked.connect(self.browser.forward)

        self.reload_button = QPushButton("Reload")
        font = self.reload_button.font()
        font.setPointSize(font_size)
        self.reload_button.setFont(font)
        self.reload_button.clicked.connect(self.browser.reload)

        self.home_button = QPushButton("Home")
        font = self.home_button.font()
        font.setPointSize(font_size)
        self.home_button.setFont(font)
        self.home_button.clicked.connect(self.go_home)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button, 0, Qt.AlignTop)
        button_layout.addWidget(self.forward_button, 0, Qt.AlignTop)
        button_layout.addWidget(self.reload_button, 0, Qt.AlignTop)
        button_layout.addWidget(self.home_button, 0, Qt.AlignTop)

        logo_layout = QVBoxLayout()
        logo_layout.addWidget(self.logo_label, 0, Qt.AlignTop)  # Set alignment to top
        logo_layout.addWidget(self.create_tab_button, 0, Qt.AlignTop)

        self.layout = QVBoxLayout()
        self.layout.addLayout(logo_layout)
        self.layout.addWidget(self.address_bar, 0, Qt.AlignTop)
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.browser)
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(2, 2, 2, 2)

        self.setLayout(self.layout)

        self.logo_animation.start()  # Start logo animation
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        url = self.address_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def go_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def authenticate_with_google(self):
        # Add your authentication code here if needed
        pass

    def create_new_tab(self):
        if self.main_browser:
            new_browser = Browser(self.tab_widget, self.main_browser)
            new_browser.authenticate_with_google()
            self.tab_widget.addTab(new_browser, "New Tab")
            new_browser.browser.setUrl(QUrl("https://www.google.com"))
            self.tab_widget.setCurrentWidget(new_browser)

class AuthPopup(QWidget):
    pass

class MainBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        font_size = 14

        self.create_tab_button = QPushButton("New Tab")
        font = self.create_tab_button.font()
        font.setBold(True)
        font.setPointSize(font_size)
        self.create_tab_button.setFont(font)
        self.create_tab_button.clicked.connect(self.create_tab)

        self.close_tab_button = QPushButton("Close Tab")
        font = self.close_tab_button.font()
        font.setBold(True)
        font.setPointSize(font_size)
        self.close_tab_button.setFont(font)
        self.close_tab_button.clicked.connect(self.close_current_tab)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_tab_button, 0, Qt.AlignTop)
        button_layout.addWidget(self.close_tab_button, 0, Qt.AlignTop)

        self.layout = QVBoxLayout()
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.tab_widget)
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(2, 2, 2, 2)

        self.container = QWidget()
        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)
        self.setWindowTitle("LIMINAL")
        self.showMaximized()

    def create_tab(self):
        new_browser = Browser(self.tab_widget, self)
        new_browser.authenticate_with_google()
        self.tab_widget.addTab(new_browser, "New Tab")
        self.tab_widget.setCurrentWidget(new_browser)

    def close_current_tab(self):
        current_index = self.tab_widget.currentIndex()
        if current_index != -1:
            self.tab_widget.removeTab(current_index)

def run_browser():
    app = QApplication(sys.argv)
    splash = SplashScreen()
    app.processEvents()
    window = MainBrowser()
    splash.finish(window)
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_browser()
