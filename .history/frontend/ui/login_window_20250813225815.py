from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLineEdit, QPushButton, QLabel, 
                               QMessageBox, QFormLayout)
from PySide6.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
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
        
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Password:", self.password_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.login_btn = QPushButton("Login")
        self.register_btn = QPushButton("Register")
        
        self.login_btn.clicked.connect(self.login)
        self.register_btn.clicked.connect(self.register)
        
        button_layout.addWidget(self.login_btn)
        button_layout.addWidget(self.register_btn)
        
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        
        if not email or not password:
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return
        
        # TODO: Implement actual login logic
        QMessageBox.information(self, "Info", "Login functionality coming soon!")
    
    def register(self):
        # TODO: Open registration window
        QMessageBox.information(self, "Info", "Registration window coming soon!")