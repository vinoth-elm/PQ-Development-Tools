from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QGroupBox,
    QMessageBox,
)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Meter Webpage Test Automation")
        self.setMinimumSize(700, 500)

        self.setup_ui()
        self.apply_style()

    def setup_ui(self):

        # -------------------------------------------------
        # Central Widget
        # -------------------------------------------------

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(20)

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title = QLabel("Meter Webpage Test Automation")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("title")

        subtitle = QLabel("Browser-based meter testing tool")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName("subtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # -------------------------------------------------
        # Meter Configuration
        # -------------------------------------------------

        config_group = QGroupBox("Meter Configuration")

        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # IP Address
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Example: 192.168.1.100")

        form_layout.addRow("Meter IP:", self.ip_input)

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")

        form_layout.addRow("Username:", self.username_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Password:", self.password_input)

        config_group.setLayout(form_layout)

        main_layout.addWidget(config_group)

        # -------------------------------------------------
        # Login Button
        # -------------------------------------------------

        button_layout = QHBoxLayout()

        self.login_button = QPushButton("LOGIN")

        self.login_button.setMinimumHeight(45)
        self.login_button.clicked.connect(self.login_clicked)

        button_layout.addStretch()
        button_layout.addWidget(self.login_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        # -------------------------------------------------
        # Status
        # -------------------------------------------------

        status_group = QGroupBox("Connection Status")

        status_layout = QVBoxLayout()

        self.status_label = QLabel("● Not Connected")
        self.status_label.setObjectName("status")

        status_layout.addWidget(self.status_label)

        status_group.setLayout(status_layout)

        main_layout.addWidget(status_group)

        # -------------------------------------------------
        # Future Test Area
        # -------------------------------------------------

        test_group = QGroupBox("Test Execution")

        test_layout = QVBoxLayout()

        test_info = QLabel(
            "Test execution will be available after successful login."
        )

        test_info.setWordWrap(True)

        test_layout.addWidget(test_info)

        test_group.setLayout(test_layout)

        main_layout.addWidget(test_group)

        main_layout.addStretch()

    # -----------------------------------------------------
    # Login Button
    # -----------------------------------------------------

    def login_clicked(self):

        ip = self.ip_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not ip:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter the meter IP address."
            )
            return

        if not username:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter the username."
            )
            return

        if not password:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter the password."
            )
            return

        # Phase 1 only
        QMessageBox.information(
            self,
            "Phase 1",
            f"Configuration received.\n\n"
            f"IP: {ip}\n"
            f"Username: {username}\n\n"
            f"Browser login will be implemented in Phase 2."
        )

        self.status_label.setText("● Configuration Ready")

    # -----------------------------------------------------
    # Styling
    # -----------------------------------------------------

    def apply_style(self):

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6f8;
            }

            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                color: #111111;
            }

            QLabel#subtitle {
                font-size: 13px;
                color: #333333;
            }

            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #111111;
                border: 1px solid #b8bcc3;
                border-radius: 8px;
                margin-top: 12px;
                padding: 15px;
                background-color: #ffffff;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
                color: #111111;
            }

            QLabel {
                color: #222222;
            }

            QLineEdit {
                min-height: 34px;
                border: 1px solid #9da3aa;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
                color: #111111;
                background-color: #ffffff;
            }

            QLineEdit::placeholder {
                color: #777777;
            }

            QLineEdit:focus {
                border: 2px solid #3578c9;
            }

            QPushButton {
                min-width: 150px;
                min-height: 40px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                color: #111111;
                background-color: #e1e5ea;
                border: 1px solid #9da3aa;
            }

            QPushButton:hover {
                background-color: #d4d9df;
            }

            QPushButton:pressed {
                background-color: #c5cbd2;
            }

            QLabel#status {
                font-size: 14px;
                font-weight: bold;
                color: #222222;
            }

            /* Message Box */

            QMessageBox {
                background-color: #ffffff;
            }

            QMessageBox QLabel {
                color: #111111;
                font-size: 14px;
            }

            QMessageBox QPushButton {
                min-width: 90px;
                min-height: 32px;
                padding: 5px 15px;
                background-color: #e1e5ea;
                color: #111111;
                border: 1px solid #9da3aa;
                border-radius: 5px;
                font-weight: bold;
            }

            QMessageBox QPushButton:hover {
                background-color: #d4d9df;
            }
        """)