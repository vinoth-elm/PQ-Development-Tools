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
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from core.browser_manager import BrowserManager
from core.excel_manager import ExcelManager


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.browser_manager = BrowserManager()
        self.excel_manager = ExcelManager()

        self.test_cases = []

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
        # Test Case Excel
        # -------------------------------------------------

        excel_group = QGroupBox("Test Case Excel")

        excel_layout = QVBoxLayout()

        self.upload_excel_button = QPushButton(
            "UPLOAD TEST CASES"
        )

        self.upload_excel_button.setMinimumHeight(40)

        self.upload_excel_button.clicked.connect(
            self.upload_excel
        )

        excel_layout.addWidget(
            self.upload_excel_button
        )

        excel_group.setLayout(excel_layout)

        main_layout.addWidget(excel_group)

        # -------------------------------------------------
        # Test Case Table
        # -------------------------------------------------

        self.test_case_table = QTableWidget()

        self.test_case_table.setColumnCount(9)

        self.test_case_table.setHorizontalHeaderLabels([
            "ID",
            "Page",
            "Action",
            "Locator Type",
            "Locator",
            "Input",
            "Expected Result",
            "Validation",
            "Enabled"
        ])

        self.test_case_table.setAlternatingRowColors(True)

        self.test_case_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.test_case_table.horizontalHeader().setStretchLastSection(
            True
        )

        main_layout.addWidget(
            self.test_case_table
        )

        self.run_tests_button = QPushButton("RUN TESTS")
        self.run_tests_button.setMinimumHeight(40)
        self.run_tests_button.setEnabled(False)
        self.run_tests_button.clicked.connect(self.run_tests)

        main_layout.addWidget(self.run_tests_button)

        # -------------------------------------------------
        # Test Execution
        # -------------------------------------------------

        test_group = QGroupBox("Test Execution")

        test_layout = QVBoxLayout()

        self.test_execution_status = QLabel(
            "Test execution is ready."
        )

        self.test_execution_status.setWordWrap(True)

        test_layout.addWidget(
            self.test_execution_status
        )

        test_group.setLayout(test_layout)

        main_layout.addWidget(test_group)

        main_layout.addStretch()

    # -----------------------------------------------------
    # Upload Excel
    # -----------------------------------------------------

    def upload_excel(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Test Case Excel File",
            "",
            "Excel Files (*.xlsx)"
        )

        if not file_path:
            return

        success, result = self.excel_manager.load_test_cases(
            file_path
        )

        if not success:

            QMessageBox.critical(
                self,
                "Excel Error",
                result
            )

            return

        # Store the loaded test cases
        self.test_cases = result

        # Display test cases in the table
        self.display_test_cases(
            self.test_cases
        )

        # Enable test execution
        self.run_tests_button.setEnabled(True)

        # Update execution status
        self.test_execution_status.setText(
            f"{len(self.test_cases)} test steps loaded. "
            "Ready for execution."
        )

        QMessageBox.information(
            self,
            "Excel Loaded",
            f"{len(self.test_cases)} test steps loaded successfully."
        )

    def run_tests(self):

        if not self.browser_manager.page:
            self.show_message(
                "Error",
                "Browser is not connected."
            )
            return

        if not self.test_cases:
            self.show_message(
                "Error",
                "Please upload test cases first."
            )
            return

        from core.test_engine import TestEngine

        engine = TestEngine(
            self.browser_manager.page,
            self.ip_input.text().strip()
        )

        results = engine.execute_test_cases(
            self.test_cases
        )

        print("\n==============================")
        print("TEST EXECUTION COMPLETED")
        print("==============================")

        for result in results:
            print(result)

        self.test_execution_status.setText(
            "Test execution completed."
        )

    # -----------------------------------------------------
    # Display Test Cases
    # -----------------------------------------------------

    def display_test_cases(self, test_cases):

        self.test_case_table.setRowCount(0)

        columns = [
            "ID",
            "Page",
            "Action",
            "Locator Type",
            "Locator",
            "Input",
            "Expected Result",
            "Validation",
            "Enabled"
        ]

        for row_index, test_case in enumerate(test_cases):

            self.test_case_table.insertRow(row_index)

            for column_index, column_name in enumerate(columns):

                value = test_case.get(
                    column_name,
                    ""
                )

                item = QTableWidgetItem(
                    str(value)
                )

                self.test_case_table.setItem(
                    row_index,
                    column_index,
                    item
                )

    # -----------------------------------------------------
    # Login Button
    # -----------------------------------------------------

    def login_clicked(self):

        ip = self.ip_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text()

        # Validate input
        if not ip:
            QMessageBox.warning(
                self,
                "Input Error",
                "Please enter Meter IP."
            )
            return

        if not username:
            QMessageBox.warning(
                self,
                "Input Error",
                "Please enter Username."
            )
            return

        if not password:
            QMessageBox.warning(
                self,
                "Input Error",
                "Please enter Password."
            )
            return

        try:

            # Start browser
            page = self.browser_manager.start()

            # Meter login URL
            url = f"http://{ip}/login.html"

            # Open login page
            page.goto(
                url,
                wait_until="domcontentloaded"
            )

            # Enter username
            page.locator(
                'input[placeholder="Username"]'
            ).fill(username)

            # Enter password
            page.locator(
                'input[placeholder="Password"]'
            ).fill(password)

            # Click LOGIN
            page.get_by_role(
                "button",
                name="LOGIN"
            ).click()

            # Wait for page to settle
            page.wait_for_load_state(
                "domcontentloaded"
            )

            # Update status
            self.status_label.setText(
                "● Login Successful"
            )

            QMessageBox.information(
                self,
                "Login",
                "Login successful."
            )

        except Exception as e:

            self.status_label.setText(
                "● Login Failed"
            )

            QMessageBox.critical(
                self,
                "Login Failed",
                str(e)
            )

    # -----------------------------------------------------
    # Message Box
    # -----------------------------------------------------

    def show_message(self, title, message, message_type="info"):

        if message_type == "error":
            QMessageBox.critical(
                self,
                title,
                message
            )

        elif message_type == "warning":
            QMessageBox.warning(
                self,
                title,
                message
            )

        else:
            QMessageBox.information(
                self,
                title,
                message
            )

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

    # -----------------------------------------------------
    # Close Application
    # -----------------------------------------------------

    def closeEvent(self, event):

        try:
            self.browser_manager.stop()
        except Exception:
            pass

        event.accept()