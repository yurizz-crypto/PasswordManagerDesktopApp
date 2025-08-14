from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLineEdit, QPushButton, QLabel, 
                               QMessageBox, QFormLayout)
from PySide6.QtCore import Qt, Signal
from controllers.api_client import APIClient
from ui.register_window import RegisterWindow
from ui.main_window import MainWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.register_window = None 
        self.main_window = None
        self.setWindowTitle("Password Manager - Login")
        self.setFixedSize(400, 300)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Password Manager")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        
        # Form
        form_layout = QFormLayout()
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        # Allow Enter key to login
        self.password_input.returnPressed.connect(self.login)
        
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Password:", self.password_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.login_btn = QPushButton("Login")
        self.register_btn = QPushButton("Register")
        
        self.login_btn.clicked.connect(self.login)
        self.register_btn.clicked.connect(self.show_register)
        
        button_layout.addWidget(self.login_btn)
        button_layout.addWidget(self.register_btn)
        
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        if not email or not password:
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return
        
        # Try to login
        result = self.api_client.login(email, password)
        
        if 'error' in result:
            QMessageBox.critical(self, "Login Failed", str(result['error']))
        else:
            # Login successful
            QMessageBox.information(self, "Success", "Login successful!")
            self.show_main_window()
    
    def show_register(self):
        self.register_window = RegisterWindow()
        self.register_window.registration_successful.connect(self.on_registration_success)
        self.register_window.show()
    
    def on_registration_success(self):
        QMessageBox.information(self, "Success", "Registration successful! Please login.")
    
    def show_main_window(self):
        self.main_window = MainWindow(self.api_client)
        self.main_window.show()
        self.hide()