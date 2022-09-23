from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QWidget, QFrame, QSpacerItem, QSizePolicy
from PySide6.QtGui import QColor, QPixmap, QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtSvgWidgets import QSvgWidget

from gui.py.ui_main import Ui_MainWindow
from gui.py.ui_card_component import Ui_CardComponent

class CustomButton(QPushButton):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.setStyleSheet("""
                           min-height: 48px;
                           border: none;
                           border-bottom: 1px solid rgb(31, 31, 64);
                           text-align: left;
                           padding-left: 18px;
                           font-weight: 600;
                           """)
        self.setText(kwargs.get("text"))
        self.setIcon(QIcon(kwargs.get("icon")))
        self.setIconSize(QSize(20, 20))

class CardComponent(QWidget, Ui_CardComponent):
    def __init__(self, **kwargs):
        super().__init__()
        self.setupUi(self)
        
        if 'frame_svg_color_1' in kwargs and 'frame_svg_color_2' in kwargs:
            self.frame.setStyleSheet("QFrame#card_frame_svg{background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 %s, stop:1 %s);border-radius:10px}" % (kwargs.get('frame_svg_color_1'), kwargs.get('frame_svg_color_2')))

        self.svg  = QSvgWidget(kwargs.get('svg_path'))
        self.svg.setMaximumSize(35, 35)
        
        self.frame_svg_layout = QHBoxLayout()
        
        self.frame_svg_layout.addWidget(self.svg)
        self.card_frame_svg.setLayout(self.frame_svg_layout)
        
        self.card_text.setText(kwargs.get('title'))
        
        if not kwargs.get('button'):
            self.card_button.hide()
        else:
            self.card_button.setText(kwargs.get('button'))
        
        self.horizontalLayout = QHBoxLayout()
        self.frame.setLayout(self.horizontalLayout)
        

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.showMaximized()
        
        self.value = 0
        self.current_state = True
        self.updated_stylesheet = ""
        
        # Add a shadow on frame color black
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(80)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(10)
        self.shadow.setColor(QColor(0, 0, 0, 100))
        
        self.top_menu_frame.setGraphicsEffect(self.shadow)
        
        self.hamburger_menu.clicked.connect(self.toggle_menu)
        
        
        self.card_component = CardComponent(svg_path="resources/icons/pantone-outline.svg", title="Title of label card", button="Support")
        self.card_component_2 = CardComponent(svg_path="resources/icons/briefcase-outline.svg", title="Title of label card 2", button="Documentation")
        
        self.form_layout = QHBoxLayout()
        self.form_layout.addWidget(self.card_component)
        self.form_layout.addWidget(self.card_component_2)

        self.top_main_frame.setLayout(self.form_layout)
        self.top_main_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.top_main_frame.layout().setSpacing(30)
        
        
        self.card_component_3 = CardComponent(svg_path="resources/icons/bulb-outline.svg", title="Title of label card")
        self.card_component_4 = CardComponent(svg_path="resources/icons/loader-outline.svg", title="Title of label card 2", frame_svg_color_1="#00D68F", frame_svg_color_2="#2AE59A")
        self.card_component_5 = CardComponent(svg_path="resources/icons/speaker-outline.svg", title="Title of label card 3")
        self.card_component_6 = CardComponent(svg_path="resources/icons/mic-outline.svg", title="Title of label card 4", frame_svg_color_1="#FEAA01", frame_svg_color_2="#FEC84A")
        
        self.form_layout_2 = QHBoxLayout()
        self.form_layout_2.addWidget(self.card_component_3)
        self.form_layout_2.addWidget(self.card_component_4)
        self.form_layout_2.addWidget(self.card_component_5)
        self.form_layout_2.addWidget(self.card_component_6)

        self.middle_main_frame.setLayout(self.form_layout_2)
        self.middle_main_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.middle_main_frame.layout().setSpacing(30)
        
        self.temperature_button.clicked.connect(self.temperature_page)
        self.humidity_button.clicked.connect(self.humidity_page)
        
        down_layout = QHBoxLayout()
        up_layout = QHBoxLayout()
        power_layout = QHBoxLayout()
        
        down_layout.addWidget(QSvgWidget("resources/icons/arrow-downward-outline.svg"))
        up_layout.addWidget(QSvgWidget("resources/icons/arrow-upward-outline.svg"))
        power_layout.addWidget(QSvgWidget("resources/icons/power-outline.svg"))
        
        self.chart_frame_layout = QHBoxLayout()
        self.chart_frame_layout.addWidget(QSvgWidget("resources/images/visualization.svg"))
        
        self.frame_chart_main.setLayout(self.chart_frame_layout)
        
        self.down_button.setLayout(down_layout)
        self.up_button.setLayout(up_layout)
        self.power_button.setLayout(power_layout)
        
        self.up_button.clicked.connect(lambda: self.define_temperature("up"))
        self.down_button.clicked.connect(lambda: self.define_temperature("down"))
        
        self.power_button.clicked.connect(self.power)
        
        self.traffic_chart.setPixmap(QPixmap("resources/images/traffic.png"))
        self.eletricy_consumption_chart.setPixmap(QPixmap("resources/images/eletricity.png"))
        
        #Add custom buttons on menu
        
        self.buttons_layout = QVBoxLayout()
        
        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        self.iot_dashboard_button = CustomButton(
            icon="resources/icons/home-outline.svg",
            text="IoT Dashboard"
        )
        
        self.sound_devices_button = CustomButton(
            icon="resources/icons/music-outline.svg",
            text="Sound Devices"
        )
        
        self.wifi_devices_button = CustomButton(
            icon="resources/icons/wifi-outline.svg",
            text="Wifi Devices"
        )
        
        self.settings_button = CustomButton(
            icon="resources/icons/settings-2-outline.svg",
            text="Settings"
        )
        
        self.camera_devices_button = CustomButton(
            icon="resources/icons/video-outline.svg",
            text="Camera Devices"
        )
        
        self.lock_devices_button = CustomButton(
            icon="resources/icons/unlock-outline.svg",
            text="Eletronic Locks"
        )
        
        
        self.buttons_layout.addWidget(self.iot_dashboard_button) 
        self.buttons_layout.addWidget(self.sound_devices_button) 
        self.buttons_layout.addWidget(self.wifi_devices_button)
        self.buttons_layout.addWidget(self.lock_devices_button)
        self.buttons_layout.addWidget(self.camera_devices_button)
        self.buttons_layout.addWidget(self.settings_button) 
         
        
        self.buttons_layout.addItem(self.spacer)
        
        self.right_menu.setLayout(self.buttons_layout)
        self.right_menu.layout().setContentsMargins(0, 0, 0, 0)
        
    def temperature_page(self):
            self.stackedWidget.setCurrentIndex(0)
            self.temperature_button.setChecked(True)
            self.humidity_button.setChecked(False)

    def humidity_page(self):
            self.stackedWidget.setCurrentIndex(1)
            self.humidity_button.setChecked(True)
            self.temperature_button.setChecked(False)
            
    def power(self):
        if self.current_state:
            self.circular_prog.setStyleSheet("")
            self.temperature_label.setText('<html><head/><body><p><span style=" font-size:36pt; font-weight:700;"> -- </span></p></body></html>')
            self.down_button.setEnabled(False)
            self.up_button.setEnabled(False)
            self.current_state = False
            return
        else:
            self.text_base = '<html><head/><body><p><span style=" font-size:36pt; font-weight:700;">{}°</span></p></body></html>'.format(str(self.value))
            self.circular_prog.setStyleSheet(self.updated_stylesheet)
            self.temperature_label.setText(self.text_base)
            self.down_button.setEnabled(True)
            self.up_button.setEnabled(True)
            self.current_state = True
            return
        
    def define_temperature(self, direction):
        if direction == "up" and self.value < 100:
            self.value  += 10
        elif direction == "down" and self.value > 0:
            self.value -= 10
        
        self.stop_1 = (1 - ((self.value / 100)) - 0.01)
        self.stop_2 = (1 - ((self.value / 100)))
        
        stylesheet_base = """
        QFrame#circular_prog
        {
            background-color: qconicalgradient(cx:0.5, cy:0.5, angle:271, stop:{STOP_1} rgba(127, 169, 251, 0), stop:{STOP_2} rgba(238, 255, 0, 255));
            border-radius: 125px;
        }
        """
        
        self.updated_stylesheet = stylesheet_base.replace("{STOP_1}",str(self.stop_1)).replace("{STOP_2}", str(self.stop_2))
        
        self.circular_prog.setStyleSheet(self.updated_stylesheet)
        
        self.text_base = '<html><head/><body><p><span style=" font-size:36pt; font-weight:700;">{}°</span></p></body></html>'.format(str(self.value))
        self.temperature_label.setText(self.text_base)
        
    def toggle_menu(self):
        if self.right_menu.width() == 251:
            new_width = 56
        else:
            new_width = 251
            
        self.animation = QPropertyAnimation(self.right_menu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()
        
        
app = QApplication([])

window = MainWindow()
window.show()

app.exec()